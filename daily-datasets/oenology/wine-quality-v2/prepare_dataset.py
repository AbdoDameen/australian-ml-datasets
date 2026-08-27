#!/usr/bin/env python3
"""
Wine Quality (Vinho Verde) — UCI ML Repository
Predict wine quality score (0-10) from physicochemical properties.
Combines red + white variants with a wine_type flag.
"""
import pandas as pd
import numpy as np
import json
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

DOMAIN = "oenology"
DATASET_NAME = "wine-quality-v2"
TARGET_COL = "quality"


def load_data():
    """Load red + white wine CSVs (semicolon-separated, quoted headers)."""
    print("Loading winequality-red.csv...")
    red = pd.read_csv(RAW / "winequality-red.csv", sep=';')
    print(f"  Red:   {red.shape}")

    print("Loading winequality-white.csv...")
    white = pd.read_csv(RAW / "winequality-white.csv", sep=';')
    print(f"  White: {white.shape}")

    red["wine_type"] = "red"
    white["wine_type"] = "white"

    df = pd.concat([red, white], ignore_index=True)
    print(f"  Combined: {df.shape}")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]:,} x {df.shape[1]}")
    print(f"\nData Types:\n{df.dtypes.to_string()}")
    missing = df.isnull().sum()
    print(f"\nMissing values total: {missing.sum()}")
    print(f"\nNumeric Stats:\n{df.select_dtypes(include=[np.number]).describe().to_string()}")
    print(f"\nTarget distribution:\n{df[TARGET_COL].value_counts().sort_index().to_string()}")
    print(f"\nWine type counts:\n{df['wine_type'].value_counts().to_string()}")
    print(f"\nDuplicate rows: {df.duplicated().sum():,}")


def clean_dataset(df):
    df_clean = df.copy()

    # 1. Standardize column names
    df_clean.columns = (df_clean.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^a-z0-9_]", "_", regex=True)
                        .str.replace(r"_+", "_", regex=True)
                        .str.strip("_"))

    # 2. Remove duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"\nRemoved {dupes:,} duplicate rows")

    # 3. Missing values (numeric -> median)
    for col in df_clean.select_dtypes(include=[np.number]).columns:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            print(f"  Numeric '{col}': filled {n:,} with median")

    # 4. Outlier capping (1.5x IQR) on physicochemical features only
    feat_cols = [c for c in df_clean.select_dtypes(include=[np.number]).columns
                 if c != TARGET_COL]
    for col in feat_cols:
        Q1, Q3 = df_clean[col].quantile(0.25), df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_capped = int((df_clean[col] < lower).sum() + (df_clean[col] > upper).sum())
        if n_capped > 0:
            df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
            print(f"  Capped {n_capped} outliers in '{col}'")

    print(f"Cleaning complete! Shape: {df_clean.shape[0]:,} x {df_clean.shape[1]}, "
          f"Missing: {df_clean.isnull().sum().sum()}")
    return df_clean


def engineer_features(df):
    """Add wine-chemistry derived features."""
    df_fe = df.copy()

    # 1. Total acidity (fixed + volatile + citric)
    df_fe["total_acidity"] = (df_fe["fixed_acidity"] + df_fe["volatile_acidity"]
                              + df_fe["citric_acid"]).round(3)

    # 2. Acidity balance — fixed vs volatile (higher = harsher)
    df_fe["fixed_to_volatile"] = (df_fe["fixed_acidity"]
                                  / (df_fe["volatile_acidity"] + 1e-6)).round(3)

    # 3. Sulfur dioxide ratio (free vs total) — preservative profile
    df_fe["so2_ratio"] = (df_fe["free_sulfur_dioxide"]
                          / (df_fe["total_sulfur_dioxide"] + 1e-6)).round(4)

    # 4. Sweetness (residual sugar) bands
    df_fe["sweetness"] = pd.cut(df_fe["residual_sugar"],
                                bins=[0, 1, 5, 20, 70],
                                labels=["dry", "off_dry", "medium", "sweet"])

    # 5. Alcohol bands
    df_fe["alcohol_band"] = pd.cut(df_fe["alcohol"],
                                   bins=[0, 9, 10.5, 12, 15],
                                   labels=["low", "medium", "high", "very_high"])
    df_fe["is_high_alcohol"] = (df_fe["alcohol"] >= 12).astype(int)

    # 6. Density-derived proxy for sugar load
    df_fe["sugar_per_density"] = (df_fe["residual_sugar"] / df_fe["density"]).round(3)

    # 7. Chloride-to-alcohol contrast (savory vs. strong)
    df_fe["chlorides_per_alcohol"] = (df_fe["chlorides"] / (df_fe["alcohol"] + 1e-6)).round(5)

    # 8. Binary target for classification use (quality >= 7 = good)
    df_fe["quality_label"] = (df_fe[TARGET_COL] >= 7).astype(int)

    print(f"\nFeature engineering complete! {df_fe.shape[1] - df.shape[1]} new features added")
    return df_fe


def prepare_ml_data(df):
    """One-hot encode categoricals, split, scale (regression on quality)."""
    print(f"\nPreparing ML data...")

    ml_df = df.drop(columns=["quality_label"], errors="ignore")

    # One-hot encode wine_type, sweetness, alcohol_band
    cat_cols = ml_df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        ml_df = pd.get_dummies(ml_df, columns=cat_cols, drop_first=False)
        for c in ml_df.select_dtypes(include=["bool"]).columns:
            ml_df[c] = ml_df[c].astype(int)

    ml_cols = [c for c in ml_df.columns if c != TARGET_COL]
    X = ml_df[ml_cols].select_dtypes(include=[np.number])
    y = ml_df[TARGET_COL]

    # Final NaN check
    for c in X.columns:
        n = X[c].isnull().sum()
        if n > 0:
            X[c] = X[c].fillna(X[c].median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_df = pd.DataFrame(X_test_scaled, columns=X.columns)

    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[TARGET_COL])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[TARGET_COL])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Train: {X_train_df.shape[0]:,} x {X_train_df.shape[1]}")
    print(f"Test:  {X_test_df.shape[0]:,} x {X_test_df.shape[1]}")
    print(f"Quality range — Train: {y_train.min()}..{y_train.max()} | Test: {y_test.min()}..{y_test.max()}")
    return X_train_df, X_test_df


def save_documentation(df, df_fe):
    metadata = {
        "dataset_name": DATASET_NAME,
        "dataset_number": 52,
        "domain": DOMAIN,
        "ml_task": "Regression (quality score 0-10)",
        "source": "UCI ML Repository — Wine Quality",
        "source_url": "https://archive.ics.uci.edu/dataset/186/wine+quality",
        "citation": "Cortez et al., 2009. Modeling wine preferences by data mining from physicochemical properties. Decision Support Systems, 47(4):547-553.",
        "description": "Physicochemical properties of Portuguese Vinho Verde wines (red + white). Predict the sensory quality score (median of expert ratings, 0-10).",
        "processing_date": str(datetime.now().date()),
        "total_rows": int(df.shape[0]),
        "red_rows": int((df["wine_type"] == "red").sum()),
        "white_rows": int((df["wine_type"] == "white").sum()),
        "features_original": 11,
        "features_engineered": 8,
        "features_after_encoding": int(df_fe.shape[1]) - 3,
        "target": "quality (0-10, regression)",
        "quality_distribution": {
            str(k): int(v) for k, v in df_fe[TARGET_COL].value_counts().sort_index().items()
        },
        "duplicates_removed": int(df.duplicated().sum()),
        "missing_values_after": 0,
        "transformations": [
            "Combined red + white CSVs with wine_type flag",
            "Standardized column names (lowercase, underscores)",
            "Removed duplicate rows",
            "Capped outliers at 1.5x IQR on physicochemical features",
            "Feature engineering: total_acidity, fixed_to_volatile, so2_ratio, sweetness bands,",
            "  alcohol bands, sugar_per_density, chlorides_per_alcohol, quality_label",
            "One-hot encoded: wine_type, sweetness, alcohol_band",
            "80/20 train/test split (random_state=42)",
            "StandardScaler (fit on train, transform test)"
        ],
        "licensing": "Public domain for research (Cortez et al., 2009)"
    }
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


def main():
    print(f"{'='*80}")
    print(f"  DATASET: {DATASET_NAME} (#52)  |  DOMAIN: {DOMAIN}")
    print(f"{'='*80}")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df_raw = load_data()
    run_eda(df_raw)
    df_clean = clean_dataset(df_raw)
    df_fe = engineer_features(df_clean)

    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df_fe.to_csv(clean_path, index=False)
    print(f"\nSaved: {clean_path}")

    prepare_ml_data(df_fe)
    save_documentation(df_raw, df_fe)

    print(f"\n{'='*80}")
    print(f"  DONE — Files in {BASE}")
    print(f"  Clean:   {df_fe.shape[0]:,} rows x {df_fe.shape[1]} cols")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
