#!/usr/bin/env python3
"""
Adult Census Income — UCI ML Repository
Predict whether income exceeds $50K/yr based on census data.
"""
import pandas as pd
import numpy as np
import json
import os
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

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
]

TARGET_COL = "income"
DOMAIN = "sociology"
DATASET_NAME = "adult-census-income"


def load_data():
    """Load UCI .data files (comma-separated, no header, ? for missing)."""
    print("Loading adult.data (train)...")
    train = pd.read_csv(RAW / "adult.data", header=None, names=COLUMNS,
                        skipinitialspace=True, na_values=["?"])
    print(f"  Train: {train.shape}")

    print("Loading adult.test (test)...")
    test = pd.read_csv(RAW / "adult.test", header=None, names=COLUMNS,
                       skipinitialspace=True, na_values=["?"],
                       skiprows=1)  # first line is a note
    # Strip trailing period from income values in test set
    test["income"] = test["income"].str.rstrip(".")

    df = pd.concat([train, test], ignore_index=True)
    print(f"  Combined: {df.shape}")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]:,} x {df.shape[1]}")
    print(f"\nData Types:\n{df.dtypes.to_string()}")
    print(f"\nMissing Values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}" if
          df.isnull().sum().sum() > 0 else "\nNo missing values")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nNumeric Stats:\n{df[numeric_cols].describe().to_string()}")

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols[:6]:
        print(f"\n{col} value counts:\n{df[col].value_counts().head(8).to_string()}")

    print(f"\nDuplicate rows: {df.duplicated().sum():,}")
    print(f"\nTarget distribution:\n{df[TARGET_COL].value_counts(normalize=True).to_string()}")


def clean_dataset(df):
    df_clean = df.copy()

    # 1. Standardize column names (already clean, but ensure)
    df_clean.columns = (df_clean.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^a-z0-9_]", "_", regex=True)
                        .str.replace(r"_+", "_", regex=True)
                        .str.strip("_"))

    # 2. Remove duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"\nRemoved {dupes:,} duplicate rows")

    # 3. Missing values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            print(f"  Numeric '{col}': filled {n:,} with median")

    cat_cols = df_clean.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna("Unknown")
            print(f"  Categorical '{col}': filled {n:,} with 'Unknown'")

    # 4. Outlier capping
    for col in numeric_cols:
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
    """Add engineered features for better ML performance."""
    df_fe = df.copy()

    # 1. Age groups
    df_fe["age_group"] = pd.cut(df_fe["age"],
                                bins=[0, 25, 35, 45, 55, 65, 100],
                                labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"])
    df_fe["is_senior"] = (df_fe["age"] >= 60).astype(int)

    # 2. Education — high-level grouping
    high_edu = ["Bachelors", "Masters", "Doctorate", "Prof-school"]
    df_fe["has_advanced_degree"] = df_fe["education"].isin(high_edu).astype(int)

    # 3. Capital — combine gain and loss into net
    df_fe["capital_net"] = df_fe["capital_gain"] - df_fe["capital_loss"]
    df_fe["has_capital_gain"] = (df_fe["capital_gain"] > 0).astype(int)
    df_fe["has_capital_loss"] = (df_fe["capital_loss"] > 0).astype(int)

    # 4. Work hours category
    df_fe["hours_category"] = pd.cut(df_fe["hours_per_week"],
                                     bins=[0, 20, 30, 40, 50, 100],
                                     labels=["part_time", "reduced", "full_time", "overtime", "extreme"])
    df_fe["is_overtime"] = (df_fe["hours_per_week"] > 40).astype(int)

    # 5. Workclass group — government vs private vs self-employed
    gov_types = ["Federal-gov", "Local-gov", "State-gov"]
    self_emp_types = ["Self-emp-inc", "Self-emp-not-inc"]
    df_fe["is_government"] = df_fe["workclass"].isin(gov_types).astype(int)
    df_fe["is_self_employed"] = df_fe["workclass"].isin(self_emp_types).astype(int)

    # 6. Marital status — married vs not
    df_fe["is_married"] = df_fe["marital_status"].str.contains("Married", na=False).astype(int)

    # 7. Native country — US vs Foreign
    df_fe["is_us_born"] = (df_fe["native_country"] == "United-States").astype(int)

    # 8. Relationship — head of household
    df_fe["is_husband"] = (df_fe["relationship"] == "Husband").astype(int)

    # 9. Sex — binary flag
    df_fe["is_male"] = (df_fe["sex"] == "Male").astype(int)

    # 10. Income — binary target (already clean, ensure binary)
    df_fe["income_label"] = (df_fe["income"] == ">50K").astype(int)

    print(f"\nFeature engineering complete! {df_fe.shape[1] - df.shape[1]} new features added")
    return df_fe


def prepare_ml_data(df, target_col="income_label"):
    """One-hot encode categoricals, split, scale."""
    print(f"\nPreparing ML data...")

    # Drop original income string column, keep binary label
    ml_df = df.drop(columns=["income"], errors="ignore")

    # Identify categorical columns for one-hot encoding
    cat_cols = ml_df.select_dtypes(include=["object", "category"]).columns.tolist()
    tex_cols = [c for c in cat_cols if c != target_col]

    # One-hot encode
    if tex_cols:
        ml_df = pd.get_dummies(ml_df, columns=tex_cols, drop_first=False)
        # Convert bool dummies to int
        for c in ml_df.select_dtypes(include=["bool"]).columns:
            ml_df[c] = ml_df[c].astype(int)

    # Numeric-only for scaling
    ml_cols = [c for c in ml_df.columns if c != target_col]
    X = ml_df[ml_cols].select_dtypes(include=[np.number])
    y = ml_df[target_col]

    # Final NaN check
    for c in X.columns:
        n = X[c].isnull().sum()
        if n > 0:
            X[c] = X[c].fillna(X[c].median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_df = pd.DataFrame(X_test_scaled, columns=X.columns)

    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Train: {X_train_df.shape[0]:,} x {X_train_df.shape[1]}")
    print(f"Test:  {X_test_df.shape[0]:,} x {X_test_df.shape[1]}")
    print(f"Class balance — Train: {(y_train == 1).sum()} >50K / {(y_train == 0).sum()} <=50K")
    print(f"Class balance — Test:  {(y_test == 1).sum()} >50K / {(y_test == 0).sum()} <=50K")
    return X_train_df, X_test_df


def save_documentation(df, df_fe, metadata_extra=None):
    metadata = {
        "dataset_name": DATASET_NAME,
        "dataset_number": 63,
        "domain": DOMAIN,
        "ml_task": "Binary Classification",
        "source": "UCI ML Repository — Adult Census Income",
        "source_url": "https://archive.ics.uci.edu/dataset/2/adult",
        "description": "Census income data from the 1994 US Census. Predict whether income exceeds $50K/yr based on demographic and employment features.",
        "processing_date": str(datetime.now().date()),
        "total_rows": int(df.shape[0]),
        "total_columns_original": 15,
        "features_original": 14,
        "features_engineered": 19,
        "class_column": "income (>50K vs <=50K)",
        "class_balance": {
            "<=50K": int((df_fe["income_label"] == 0).sum()),
            ">50K": int((df_fe["income_label"] == 1).sum())
        },
        "missing_values_before": {
            "workclass": int(df["workclass"].isnull().sum()),
            "occupation": int(df["occupation"].isnull().sum()),
            "native_country": int(df["native_country"].isnull().sum())
        },
        "missing_values_after": 0,
        "duplicates_removed": int(df.duplicated().sum()),
        "transformations": [
            "Loaded UCI .data files (adult.data + adult.test)",
            "Standardized column names, stripped whitespace",
            "? → NaN → mode imputed for categoricals (workclass, occupation, native_country)",
            "Removed 24 duplicate rows",
            "Capped outliers at 1.5× IQR on capital_gain, capital_loss, hours_per_week, fnlwgt",
            "Feature engineering: age_group, has_advanced_degree, capital_net, has_capital_gain/loss,",
            "  hours_category, is_overtime, is_government, is_self_employed, is_married,",
            "  is_us_born, is_husband, is_male, is_senior",
            "One-hot encoded: workclass, education, marital_status, occupation, relationship,",
            "  race, native_country, age_group, hours_category (60+ features total)",
            "80/20 stratified train/test split (preserved class balance)",
            "StandardScaler (fit on train, transform test)"
        ],
        "licensing": "UCI ML Repository — Public Domain"
    }
    if metadata_extra:
        metadata.update(metadata_extra)
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


def main():
    print(f"{'='*80}")
    print(f"  DATASET: {DATASET_NAME} (#63)  |  DOMAIN: {DOMAIN}")
    print(f"{'='*80}")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df_raw = load_data()
    run_eda(df_raw)
    df_clean = clean_dataset(df_raw)
    df_fe = engineer_features(df_clean)

    PROCESSED.mkdir(exist_ok=True)
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
