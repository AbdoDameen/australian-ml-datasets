#!/usr/bin/env python3
"""
Forest Fires — Data Preparation Pipeline
UCI ML Repository: https://archive.ics.uci.edu/ml/datasets/Forest+Fires
Target: burned area (hectares) — regression
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

RAW_FILE = "forestfires.csv"
TARGET_COL = "area"
DOMAIN = "forestry"
DATASET_NAME = "forest-fires"


def load_data():
    """Load the raw CSV."""
    path = RAW / RAW_FILE
    print(f"Loading: {path}")
    df = pd.read_csv(path, encoding="utf-8")
    print(f"Loaded: {df.shape[0]} rows x {df.shape[1]} cols")
    return df


def run_eda(df):
    """Print EDA summary."""
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]} x {df.shape[1]}")
    print(f"\nDtypes:\n{df.dtypes.to_string()}")
    print(f"\nMissing:\n{df.isnull().sum().to_string()}")
    print(f"\nNumeric stats:\n{df.describe().to_string()}")
    print(f"\nMonth:\n{df['month'].value_counts().to_string()}")
    print(f"\nDay:\n{df['day'].value_counts().to_string()}")
    print(f"\nArea stats:\n  zero: {(df['area']==0).sum()} ({(df['area']==0).mean()*100:.1f}%)")
    print(f"  non-zero: {(df['area']>0).sum()}")
    print(f"  max: {df['area'].max():.1f}")
    print(f"\nDuplicates: {df.duplicated().sum()}")
    return df


def clean_dataset(df):
    """Standard cleaning."""
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = (df_clean.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^a-z0-9_]", "_", regex=True)
                        .str.replace(r"_+", "_", regex=True)
                        .str.strip("_"))

    # Remove duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {dupes} duplicate rows")

    # Missing values
    for col in df_clean.select_dtypes(include=[np.number]).columns:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            print(f"  Numeric '{col}': filled {n} with median")

    for col in df_clean.select_dtypes(include=["object"]).columns:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna("Unknown")
            print(f"  Categorical '{col}': filled {n} with Unknown")

    # Outlier capping (1.5× IQR) — skip `area` (target, keep original distribution)
    numeric_cols = [c for c in df_clean.select_dtypes(include=[np.number]).columns if c != TARGET_COL]
    for col in numeric_cols:
        Q1, Q3 = df_clean[col].quantile(0.25), df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_capped = (df_clean[col] < lower).sum() + (df_clean[col] > upper).sum()
        if n_capped > 0:
            df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
            print(f"  Capped {n_capped} outliers in '{col}'")

    print(f"Cleaned: {df_clean.shape[0]} x {df_clean.shape[1]}, missing: {df_clean.isnull().sum().sum()}")
    return df_clean


def feature_engineer(df):
    """Engineer features from month/day + log-transform target."""
    print(f"\n--- Feature Engineering ---")
    df_feat = df.copy()

    # Log-transform area (reduce skew — many zeros, so log1p)
    df_feat['area_log'] = np.log1p(df_feat['area'])
    print(f"  Created 'area_log': log1p(area) — skew reduced")

    # Encode month as numeric (mar=3 ... sep=9)
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    df_feat['month_num'] = df_feat['month'].map(month_map).fillna(0).astype(int)
    print(f"  Encoded 'month' → 'month_num' ({df_feat['month_num'].nunique()} values)")

    # One-hot encode day
    dummies = pd.get_dummies(df_feat['day'], prefix='day')
    for c in dummies.columns:
        df_feat[c] = dummies[c].astype(int)
    print(f"  One-hot encoded 'day' → {len(dummies.columns)} binary columns")

    # Fire weather index features: ffmc, dmc, dc, isi (already numeric, keep as-is)
    # Spatial features: X, Y coordinates (keep as-is)
    # Weather features: temp, rh, wind, rain (keep as-is)

    # Ratio features: temp/rh (heat × dryness interaction)
    df_feat['temp_rh_ratio'] = df_feat['temp'] / (df_feat['rh'] + 1)
    print(f"  Created 'temp_rh_ratio'")

    # DC × ISI interaction (drought × spread potential)
    df_feat['dc_isi_interaction'] = df_feat['dc'] * df_feat['isi']
    print(f"  Created 'dc_isi_interaction'")

    print(f"  Final shape: {df_feat.shape}")
    return df_feat


def prepare_ml_data(df, target_col):
    """Split, scale, and save ML-ready files."""
    print(f"\n--- ML Prep (target: {target_col}) ---")

    # Convert bool columns to int
    for col in df.select_dtypes(include=['bool']).columns:
        df[col] = df[col].astype(int)

    # Feature columns: exclude target + original cat cols + original area
    exclude = {target_col, 'area', 'month', 'day'}
    X = df.select_dtypes(include=[np.number]).copy()
    X = X[[c for c in X.columns if c not in exclude]]

    y = df[target_col]

    # Handle any remaining NaNs
    for c in X.columns[X.isnull().any()]:
        X[c] = X[c].fillna(X[c].median())

    feature_names = list(X.columns)
    print(f"Features ({len(feature_names)}): {feature_names}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    FEATURES.mkdir(exist_ok=True)
    X_train_df = pd.DataFrame(X_train_scaled, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feature_names)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Saved: {FEATURES}/")
    print(f"  Train: {X_train_df.shape}")
    print(f"  Test: {X_test_df.shape}")
    return X_train_df, X_test_df, feature_names, scaler


def save_metadata(df, features, extra=None):
    """Save metadata.json."""
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "source": "https://archive.ics.uci.edu/ml/datasets/Forest+Fires",
        "citation": "Cortez, P., & Morais, A. (2007). A data mining approach to predict forest fires using meteorological data.",
        "created_date": str(datetime.now()),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_list": list(df.columns),
        "feature_count": len(features),
        "feature_list": features,
        "target": TARGET_COL,
        "ml_task": "Regression (log1p-transformed burned area)",
        "missing_values_remaining": int(df.isnull().sum().sum()),
    }
    if extra:
        metadata.update(extra)

    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved: {BASE / 'metadata.json'}")


def main():
    print(f"{'='*70}")
    print(f"  {DATASET_NAME}  |  {DOMAIN}")
    print(f"{'='*70}\n")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df = load_data()
    run_eda(df)
    df = clean_dataset(df)
    df = feature_engineer(df)

    # Save cleaned
    PROCESSED.mkdir(exist_ok=True)
    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nSaved cleaned: {clean_path}")

    # ML prep — use log-transformed area
    X_tr, X_te, feats, scaler = prepare_ml_data(df, "area_log")

    save_metadata(df, feats)
    print(f"\nDone — all files in {BASE}")


if __name__ == "__main__":
    main()
