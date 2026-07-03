#!/usr/bin/env python3
"""
Beijing Air Quality — data preparation pipeline.
Predict PM2.5 concentration from hourly meteorological and pollutant data.
Source: UCI Machine Learning Repository (Beijing PM2.5 Data Set)
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

# ─── CONFIG ─────────────────────────────────────────────────────────────────
RAW_FILE = "PRSA_data_2010.1.1-2014.12.31.csv"
HEADER_ROW = 0
SKIP_ROWS = 0
TARGET_COL = "pm2_5"
DOMAIN = "environmental"
DATASET_NAME = "beijing-air-quality"
# ────────────────────────────────────────────────────────────────────────────


def load_data():
    csv_path = RAW / RAW_FILE
    print(f"Loading {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8")
    print(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing:\n{df.isnull().sum().to_string()}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nNumeric Stats:\n{df[numeric_cols].describe().to_string()}")
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        print(f"\n{col}:\n{df[col].value_counts().to_string()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")


def clean_dataset(df):
    df_c = df.copy()

    # Standardise column names
    df_c.columns = (df_c.columns.str.strip()
                    .str.lower()
                    .str.replace(r"[^a-z0-9_]", "_", regex=True)
                    .str.replace(r"_+", "_", regex=True)
                    .str.strip("_"))

    # Drop row-number column (no signal)
    if "no" in df_c.columns:
        df_c = df_c.drop(columns=["no"])
        print("Dropped 'No' (row index)")

    # Drop duplicates
    dupes = df_c.duplicated().sum()
    df_c = df_c.drop_duplicates()
    print(f"Removed {dupes} duplicate rows")

    # Missing: pm2.5 — fill with median grouped by (year, month) to preserve
    # seasonal pattern rather than global median
    pm25_n = df_c["pm2_5"].isnull().sum()
    if pm25_n > 0:
        month_median = df_c.groupby(["year", "month"])["pm2_5"].transform("median")
        # Fallback to global median where group is all NaN
        global_median = df_c["pm2_5"].median()
        df_c["pm2_5"] = df_c["pm2_5"].fillna(month_median).fillna(global_median)
        print(f"Filled {pm25_n} missing pm2.5 values with (year, month) group median")

    # Check remaining missing values
    remaining = df_c.isnull().sum().sum()
    print(f"Remaining missing values: {remaining}")

    # Outlier capping on pm2.5 and Iws (wind speed has heavy tail)
    for col in ["pm2_5", "iws", "pres", "temp", "dewp"]:
        if col not in df_c.columns:
            continue
        Q1, Q3 = df_c[col].quantile(0.25), df_c[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_capped = ((df_c[col] < lower) | (df_c[col] > upper)).sum()
        if n_capped > 0:
            df_c[col] = df_c[col].clip(lower=lower, upper=upper)
            print(f"Capped {n_capped} outliers in '{col}'")

    print(f"\nClean shape: {df_c.shape}, Missing: {df_c.isnull().sum().sum()}")
    return df_c


def engineer_features(df):
    """Create datetime features, encode wind direction."""
    df_f = df.copy()

    # Build datetime column
    df_f["datetime"] = pd.to_datetime(
        df_f[["year", "month", "day", "hour"]].rename(
            columns={"year": "year", "month": "month", "day": "day", "hour": "hour"}
        )
    )

    # Temporal features
    df_f["year"] = df_f["year"].astype(int)
    df_f["month"] = df_f["month"].astype(int)
    df_f["day"] = df_f["day"].astype(int)
    df_f["hour"] = df_f["hour"].astype(int)
    df_f["dayofweek"] = df_f["datetime"].dt.dayofweek
    df_f["quarter"] = df_f["datetime"].dt.quarter
    df_f["is_weekend"] = (df_f["dayofweek"] >= 5).astype(int)
    df_f["season"] = df_f["month"].map(
        {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3}
    )

    # One-hot encode wind direction
    dummies = pd.get_dummies(df_f["cbwd"], prefix="wind")
    for c in dummies.columns:
        df_f[c] = dummies[c].astype(int)

    # Drop raw cbwd (now one-hot encoded)
    df_f = df_f.drop(columns=["cbwd"])

    # Keep datetime for reference but don't use in ML
    print(f"Features after engineering: {df_f.shape[1]} columns")
    return df_f


def prepare_ml_data(df, target_col):
    print(f"\nPreparing ML data (target: {target_col})...")

    # Convert all bool to int
    for col in df.columns:
        if df[col].dtype == bool:
            df[col] = df[col].astype(int)

    # Separate features and target
    if target_col not in df.columns:
        print(f"Target '{target_col}' not found — skipping ML prep")
        return None, None, [], None

    y = df[target_col]

    # Feature cols: numeric only, drop target and datetime
    drop_cols = {target_col, "datetime"}
    feat_cols = [c for c in df.select_dtypes(include=[np.number]).columns
                 if c not in drop_cols]
    X = df[feat_cols].copy()

    # Fill any remaining NaNs
    for c in X.columns:
        if X[c].isnull().any():
            X[c] = X[c].fillna(X[c].median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=feat_cols)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feat_cols)

    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Train: {X_train_df.shape}  Test: {X_test_df.shape}")
    print(f"Saved ML files to {FEATURES}/")
    return X_train_df, X_test_df, feat_cols, scaler


def save_metadata(df):
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "source": "UCI Machine Learning Repository",
        "source_url": "https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data",
        "license": "CC BY 4.0",
        "created_date": str(datetime.now()),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_list": list(df.columns),
        "target_column": TARGET_COL,
        "ml_task": "Regression (PM2.5 concentration forecasting)",
        "missing_values_remaining": int(df.isnull().sum().sum()),
        "description": (
            "Hourly air quality and meteorological data from the US Embassy "
            "in Beijing, China. Records span Jan 2010 to Dec 2014. Target is "
            "PM2.5 concentration in micrograms per cubic meter."
        ),
        "transformations": [
            "Dropped 'No' (row index column)",
            "Standardized column names to lowercase with underscores",
            "Removed duplicate rows",
            "Filled missing pm2.5 values with (year, month) group median",
            "Capped outliers on pm2.5, Iws, PRES, TEMP, DEWP using 1.5x IQR",
            "One-hot encoded wind direction (cbwd) into 4 binary columns",
            "Added temporal features: dayofweek, quarter, is_weekend, season",
            "Train/test split 80/20 with StandardScaler normalization"
        ],
    }
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


def main():
    print("=" * 80)
    print(f"  {DATASET_NAME}  |  {DOMAIN}")
    print("=" * 80)

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df_raw = load_data()
    run_eda(df_raw)
    df_clean = clean_dataset(df_raw)
    df_feat = engineer_features(df_clean)

    # Save cleaned + engineered data
    clean_csv = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df_feat.to_csv(clean_csv, index=False)
    print(f"\nSaved clean data: {clean_csv}")

    # ML prep
    prepare_ml_data(df_feat, TARGET_COL)

    save_metadata(df_feat)
    print(f"\nDone — all files in {BASE}")


if __name__ == "__main__":
    main()
