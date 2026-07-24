#!/usr/bin/env python3
"""
Bushfire History (Australia 2016-2021) — Data Preparation Pipeline
Processes: Fire_For16-21_Attributes.csv from raw/ → cleaned + ML-ready files
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
RAW_FILE = "Fire_For16-21_Attributes.csv"
DOMAIN = "climate"
DATASET_NAME = "bushfire-history"


def load_data():
    df = pd.read_csv(RAW / RAW_FILE, encoding="utf-8")
    print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing values:\n{df.isnull().sum().to_string()}")
    print(f"\nDtypes:\n{df.dtypes.to_string()}")

    # Show blanks (spaces) as missing
    blank_cols = []
    for c in df.columns:
        blank_count = (df[c].astype(str).str.strip() == "").sum()
        if blank_count > 0:
            blank_cols.append((c, blank_count))
    if blank_cols:
        print(f"\nBlank/whitespace values:")
        for c, n in blank_cols:
            print(f"  {c}: {n} blank values")

    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"Numeric stats:\n{df.select_dtypes(include=[np.number]).describe().to_string()}")

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols[:5]:
        print(f"\n{col} value counts:\n{df[col].value_counts().head(10).to_string()}")


def clean_dataset(df):
    df_clean = df.copy()

    # 1. Standardize column names
    df_clean.columns = (df_clean.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^a-z0-9_]", "_", regex=True)
                        .str.replace(r"_+", "_", regex=True)
                        .str.strip("_"))

    # 2. Drop ID/index columns
    df_clean = df_clean.drop(columns=["oid", "value"], errors="ignore")

    # 3. Replace blank/whitespace values with NaN across all object columns
    for col in df_clean.select_dtypes(include=["object"]).columns:
        df_clean[col] = df_clean[col].astype(str).str.strip().replace("", np.nan)

    # 4. Remove duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {dupes} duplicate rows")

    # 5. Fill missing values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            print(f"  Numeric '{col}': filled {n} with median")

    cat_cols = df_clean.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna("Unknown")
            print(f"  Categorical '{col}': filled {n} with 'Unknown'")

    # 6. Fix FOR_BURNS: -9 means unknown → set to 0 (no burn info)
    if "for_burns" in df_clean.columns:
        n_neg9 = (df_clean["for_burns"] == -9).sum()
        df_clean["for_burns"] = df_clean["for_burns"].clip(lower=0)
        print(f"  FOR_BURNS: capped {n_neg9} values of -9 to 0")

    # 7. Outlier capping on numeric columns (skip count — it's area weights)
    for col in numeric_cols:
        if col in ["for_burns", "forest", "count"]:
            continue
        Q1, Q3 = df_clean[col].quantile(0.25), df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_capped = (df_clean[col] < lower).sum() + (df_clean[col] > upper).sum()
        if n_capped > 0:
            df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
            print(f"  Capped {n_capped} outliers in '{col}'")

    print(f"\nCleaning complete! Shape: {df_clean.shape}, Missing: {df_clean.isnull().sum().sum()}")
    return df_clean


def engineer_features(df):
    """Create domain-specific features from fire history columns."""
    df_feat = df.copy()

    # Fire year columns: fire_1617, fire_1718, fire_1819, fire_1920, fire_2021
    # Values: 'U' = unplanned fire, 'P' = planned/prescribed fire
    fire_year_cols = ["fire_1617", "fire_1718", "fire_1819", "fire_1920", "fire_2021"]

    for col in fire_year_cols:
        if col not in df_feat.columns:
            continue
        # Binary: had any fire that year
        df_feat[f"{col}_any_fire"] = df_feat[col].notna().astype(int)
        # Binary: unplanned fire
        df_feat[f"{col}_unplanned"] = (df_feat[col] == "U").astype(int)
        # Binary: planned fire
        df_feat[f"{col}_planned"] = (df_feat[col] == "P").astype(int)

    # Aggregate features
    fire_bool_cols = [c for c in df_feat.columns if c.endswith("_any_fire")]
    unplanned_cols = [c for c in df_feat.columns if c.endswith("_unplanned")]
    planned_cols = [c for c in df_feat.columns if c.endswith("_planned")]

    if fire_bool_cols:
        df_feat["total_years_burned"] = df_feat[fire_bool_cols].sum(axis=1)
        df_feat["total_unplanned_burns"] = df_feat[unplanned_cols].sum(axis=1)
        df_feat["total_planned_burns"] = df_feat[planned_cols].sum(axis=1)

    # Has it always burned? (all 5 years)
    if fire_bool_cols:
        df_feat["always_burned"] = (df_feat["total_years_burned"] == len(fire_bool_cols)).astype(int)

    # Binary: has this area experienced any unplanned fire?
    if "total_unplanned_burns" in df_feat.columns:
        df_feat["any_unplanned_fire"] = (df_feat["total_unplanned_burns"] > 0).astype(int)

    # Drop raw fire year columns (replaced by engineered features)
    for col in fire_year_cols:
        if col in df_feat.columns:
            df_feat = df_feat.drop(columns=[col])

    # Drop all_fire — it's a redundant concatenation of per-year codes
    if "all_fire" in df_feat.columns:
        df_feat = df_feat.drop(columns=["all_fire"])

    # Drop for_burn_t — redundant with for_burns+engineered features
    if "for_burn_t" in df_feat.columns:
        df_feat = df_feat.drop(columns=["for_burn_t"])

    # Encode categoricals
    low_card_cols = []
    for col in df_feat.select_dtypes(include=["object"]).columns:
        if df_feat[col].nunique() < 20:
            low_card_cols.append(col)

    df_feat = pd.get_dummies(df_feat, columns=low_card_cols, drop_first=True)
    # Convert bool dummies to int for sklearn compatibility
    for col in df_feat.select_dtypes(include=["bool"]).columns:
        df_feat[col] = df_feat[col].astype(int)

    print(f"\nFeature engineering complete!")
    print(f"  New features: fire year indicators, aggregate counts, one-hot encodings")
    print(f"  Shape after engineering: {df_feat.shape}")
    return df_feat


def prepare_ml_data(df, target_col):
    print(f"\n--- ML Prep (target: {target_col}) ---")

    # Convert any remaining bool columns
    for col in df.columns:
        if df[col].dtype == bool:
            df[col] = df[col].astype(int)

    # Select numeric features only
    X = df.select_dtypes(include=[np.number]).copy()
    feat_cols = [c for c in X.columns if c != target_col]

    if target_col not in df.columns:
        print(f"Target '{target_col}' not found — skipping ML prep")
        # Instead use for_burns or total_years_burned
        alt_targets = ["for_burns", "total_years_burned"]
        for t in alt_targets:
            if t in df.columns:
                target_col = t
                print(f"Falling back to target: {target_col}")
                break

    if target_col not in df.columns:
        print("No valid target found — saving features only")
        FEATURES.mkdir(exist_ok=True)
        X.to_csv(FEATURES / "features.csv", index=False)
        return

    y = df[target_col]
    X = X[feat_cols]

    # Handle remaining NaNs
    nan_cols = X.columns[X.isnull().any()].tolist()
    for c in nan_cols:
        X[c] = X[c].fillna(X[c].median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() <= 10 else None
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    FEATURES.mkdir(exist_ok=True)
    X_train_df = pd.DataFrame(X_train_scaled, columns=feat_cols)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feat_cols)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Save feature names
    with open(FEATURES / "feature_names.json", "w") as f:
        json.dump(feat_cols, f, indent=2)

    print(f"Saved ML files to {FEATURES}/")
    print(f"  X_train: {X_train_df.shape}")
    print(f"  X_test:  {X_test_df.shape}")
    print(f"  Target:  {target_col} ({y.nunique()} classes)")
    print(f"  Features: {len(feat_cols)}")


def save_documentation(df, target_col):
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "ml_task": "Multiclass Classification",
        "target_variable": target_col,
        "source": "Australian Government — National Forest Inventory",
        "source_url": "https://www.agriculture.gov.au/abares/forestsaustralia/forest-data",
        "description": "Forest fire history 2016-2021 across Australian states/territories. "
                        "Each row represents a forest polygon with tenure, category, state, "
                        "and annual fire occurrence (planned/unplanned burns).",
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_list": list(df.columns),
        "missing_values_remaining": int(df.isnull().sum().sum()),
        "created_date": str(datetime.now()),
        "transformations": [
            "Dropped OID and VALUE (index columns)",
            "Replaced blank values with NaN, filled with 'Unknown' or median",
            "Capped FOR_BURNS -9 to 0 (unknown burn status)",
            "Created per-year fire indicators (any_fire, unplanned, planned)",
            "Created aggregate: total_years_burned, total_unplanned_burns",
            "Created binary: any_unplanned_fire, always_burned",
            "One-hot encoded FOR_TEN, FOR_CATEGO, STATE, FOR_BURN_T",
            "StandardScaler normalization on training data",
            "Train/test split 80/20 with stratification"
        ]
    }
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata.json")


def main():
    print(f"{'='*60}")
    print(f"  BUSHFIRE HISTORY (Australia 2016-2021)")
    print(f"{'='*60}")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df_raw = load_data()
    run_eda(df_raw)
    df_clean = clean_dataset(df_raw)
    df_feat = engineer_features(df_clean)

    # Save cleaned dataset
    clean_csv = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df_feat.to_csv(clean_csv, index=False)
    print(f"\nSaved cleaned data: {clean_csv}")

    # ML prep — target: for_burns (0-5 multiclass)
    target = "for_burns"
    if target not in df_feat.columns:
        target = "total_years_burned"
    prepare_ml_data(df_feat, target)
    save_documentation(df_feat, target)

    print(f"\n{'='*60}")
    print(f"  DONE — all files in {BASE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
