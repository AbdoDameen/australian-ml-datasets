#!/usr/bin/env python3
"""
prepare_dataset.py — Australian Rainfall (BOM) ML Pipeline
=========================================================
Loads weatherAUS.csv, cleans, feature-engineers, and prepares
ML-ready stratified train/test splits for binary classification
(target: RainToday).

Outputs:
    processed/australian-rainfall_clean.csv
    processed/australian-rainfall_features.csv
    features/X_train_scaled.csv, X_test_scaled.csv
    features/y_train.csv, y_test.csv
    features/scaler.pkl
    metadata.json  (updated)
"""

import os
import sys
import json
import pickle
import warnings
import numpy as np
import pandas as pd

from datetime import datetime
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────────────
DATASET_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(DATASET_DIR, "weatherAUS.csv")
PROCESSED_DIR = os.path.join(DATASET_DIR, "processed")
FEATURES_DIR = os.path.join(DATASET_DIR, "features")
METADATA_PATH = os.path.join(DATASET_DIR, "metadata.json")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FEATURES_DIR, exist_ok=True)

TARGET_COL = "RainToday"
TEST_SIZE = 0.2
RANDOM_STATE = 42

print("=" * 70)
print("  Australian Rainfall (BOM) — ML Dataset Pipeline")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Load
# ═══════════════════════════════════════════════════════════════════════════
print("\n[1] Loading weatherAUS.csv ...")
df = pd.read_csv(RAW_PATH)
print(f"    Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: EDA
# ═══════════════════════════════════════════════════════════════════════════
print("\n[2] Exploratory Data Analysis")
print(f"    Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print(f"\n    ── Column dtypes ──")
for col, dtype in df.dtypes.items():
    print(f"    {col:22s}  {str(dtype):12s}")

# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_df = pd.DataFrame({"missing": missing, "pct": missing_pct})
missing_df = missing_df[missing_df["missing"] > 0].sort_values("missing", ascending=False)
print(f"\n    ── Missing values (columns with any) ──")
if len(missing_df) > 0:
    for col, row in missing_df.iterrows():
        print(f"    {col:22s}  {int(row['missing']):>7,}  ({row['pct']:5.1f}%)")
else:
    print("    (none)")

# Target distribution
print(f"\n    ── Target ({TARGET_COL}) distribution ──")
target_dist = df[TARGET_COL].value_counts(dropna=False)
for val, cnt in target_dist.items():
    pct = cnt / len(df) * 100
    label = str(val) if not pd.isna(val) else "NaN"
    print(f"    {label:6s}  {cnt:>7,}  ({pct:5.1f}%)")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Cleaning
# ═══════════════════════════════════════════════════════════════════════════
print("\n[3] Cleaning data ...")

# 3a — Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace(r"(?<=[a-z])(?=[A-Z])", "_", regex=True)
    .str.lower()
)
# Fix a few known names
rename_map = {
    "wind_gust_dir": "wind_gust_dir",
    "wind_gust_speed": "wind_gust_speed",
    "wind_dir9am": "wind_dir_9am",
    "wind_dir3pm": "wind_dir_3pm",
    "wind_speed9am": "wind_speed_9am",
    "wind_speed3pm": "wind_speed_3pm",
    "humidity9am": "humidity_9am",
    "humidity3pm": "humidity_3pm",
    "pressure9am": "pressure_9am",
    "pressure3pm": "pressure_3pm",
    "cloud9am": "cloud_9am",
    "cloud3pm": "cloud_3pm",
    "temp9am": "temp_9am",
    "temp3pm": "temp_3pm",
    "rain_today": "rain_today",
}
# Actually just use the transformation that already happened
print("    Column names standardized (snake_case)")

# 3b — Parse Date -> datetime features
print("    Parsing Date column ...")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["dayofweek"] = df["date"].dt.dayofweek
df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)
print(f"    Extracted: year, month, day, dayofweek, is_weekend")

# Drop original date column
df.drop(columns=["date"], inplace=True)

# 3c — Handle missing values
print("    Handling missing values ...")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

# Keep target in imputation for now — we'll drop NaN targets later
# Remove rain_tomorrow from imputation lists (not our target)
if "rain_tomorrow" in categorical_cols:
    categorical_cols.remove("rain_tomorrow")

# Median imputation for numeric
if numeric_cols:
    num_imputer = SimpleImputer(strategy="median")
    df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
    print(f"    Numeric columns ({len(numeric_cols)}) → median imputation")

# Mode imputation for categorical
if categorical_cols:
    cat_imputer = SimpleImputer(strategy="most_frequent")
    df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
    print(f"    Categorical columns ({len(categorical_cols)}) → mode imputation")

# Double-check no missing values remain
remaining_na = df.isnull().sum().sum()
print(f"    Remaining NA values: {remaining_na}")

# ═══════════════════════════════════════════════════════════════════════════
# Save clean CSV
# ═══════════════════════════════════════════════════════════════════════════
clean_path = os.path.join(PROCESSED_DIR, "australian-rainfall_clean.csv")
df.to_csv(clean_path, index=False)
print(f"\n    ✓ Saved clean data → {clean_path}")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: Feature Engineering
# ═══════════════════════════════════════════════════════════════════════════
print("\n[4] Feature engineering ...")

# One-hot encode Location
print("    One-hot encoding Location ...")
location_dummies = pd.get_dummies(df["location"], prefix="loc", dtype=int)
df_features = pd.concat([df, location_dummies], axis=1)
df_features.drop(columns=["location"], inplace=True)
print(f"    Added {location_dummies.shape[1]} location dummy columns")

# One-hot encode wind directions and other categoricals
cat_to_encode = [c for c in categorical_cols if c != "location" and c != "rain_tomorrow" and c != "rain_today"]
prefix_map = {
    "wind_gust_dir": "gust",
    "wind_dir9am": "dir9",
    "wind_dir3pm": "dir3",
}
for col in cat_to_encode:
    if col in df_features.columns:
        prefix = prefix_map.get(col, col[:4])
        dummies = pd.get_dummies(df_features[col], prefix=prefix, dtype=int)
        df_features = pd.concat([df_features, dummies], axis=1)
        df_features.drop(columns=[col], inplace=True)
        print(f"    One-hot encoded: {col} → {prefix}_* ({dummies.shape[1]} categories)")

# Encode target
print("\n    Encoding target: RainToday (Yes=1, No=0) ...")
df_features["rain_today"] = df_features["rain_today"].map({"Yes": 1, "No": 0, 1: 1, 0: 0})

# Drop rows where target is still NaN
nan_target = df_features["rain_today"].isnull().sum()
if nan_target > 0:
    print(f"    Dropping {nan_target} rows with NaN target ...")
    df_features = df_features.dropna(subset=["rain_today"]).reset_index(drop=True)
    print(f"    Remaining rows: {df_features.shape[0]:,}")

# Also encode rain_tomorrow if present (not used in training but keep consistent)
if "rain_tomorrow" in df_features.columns:
    df_features["rain_tomorrow"] = df_features["rain_tomorrow"].map({"Yes": 1, "No": 0, 1: 1, 0: 0})

# Drop any remaining non-numeric columns
non_numeric = df_features.select_dtypes(exclude=[np.number]).columns.tolist()
if non_numeric:
    print(f"    Dropping remaining non-numeric columns: {non_numeric}")
    df_features.drop(columns=non_numeric, inplace=True)

features_path = os.path.join(PROCESSED_DIR, "australian-rainfall_features.csv")
df_features.to_csv(features_path, index=False)
print(f"    ✓ Saved feature-engineered data → {features_path}")
print(f"    Feature matrix shape: {df_features.shape[0]:,} × {df_features.shape[1]}")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: ML Prep — Stratified Train/Test Split
# ═══════════════════════════════════════════════════════════════════════════
print("\n[5] ML preparation — stratified train/test split ...")

# Separate features and target
if "rain_today" in df_features.columns:
    y = df_features["rain_today"].values
    X = df_features.drop(columns=["rain_today"]).values
    feature_names = df_features.drop(columns=["rain_today"]).columns.tolist()
elif "rain_tomorrow" in df_features.columns:
    y = df_features["rain_tomorrow"].values
    X = df_features.drop(columns=["rain_tomorrow"]).values
    feature_names = df_features.drop(columns=["rain_tomorrow"]).columns.tolist()
else:
    raise ValueError("Target column not found!")

print(f"    X shape: {X.shape[0]:,} × {X.shape[1]:,}")
print(f"    y shape: {y.shape[0]:,}")
print(f"    y distribution: {np.bincount(y.astype(int))}")

# Stratified split
sss = StratifiedShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=RANDOM_STATE)
train_idx, test_idx = next(sss.split(X, y))

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print(f"\n    Train size: {X_train.shape[0]:,}  ({X_train.shape[0]/len(X)*100:.1f}%)")
print(f"    Test size:  {X_test.shape[0]:,}  ({X_test.shape[0]/len(X)*100:.1f}%)")
print(f"    Train y distribution: {np.bincount(y_train.astype(int))}")
print(f"    Test y distribution:  {np.bincount(y_test.astype(int))}")

# Scale features
print("\n    Fitting StandardScaler ...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"    Means (first 5 features):  {scaler.mean_[:5].round(3)}")
print(f"    Stds  (first 5 features):  {np.sqrt(scaler.var_)[:5].round(3)}")

# ═══════════════════════════════════════════════════════════════════════════
# Save ML-ready outputs
# ═══════════════════════════════════════════════════════════════════════════
print("\n[6] Saving ML-ready outputs ...")

# Save CSVs
pd.DataFrame(X_train_scaled, columns=feature_names).to_csv(
    os.path.join(FEATURES_DIR, "X_train_scaled.csv"), index=False
)
pd.DataFrame(X_test_scaled, columns=feature_names).to_csv(
    os.path.join(FEATURES_DIR, "X_test_scaled.csv"), index=False
)
pd.Series(y_train, name="rain_today").to_csv(
    os.path.join(FEATURES_DIR, "y_train.csv"), index=False
)
pd.Series(y_test, name="rain_today").to_csv(
    os.path.join(FEATURES_DIR, "y_test.csv"), index=False
)

# Save scaler
with open(os.path.join(FEATURES_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

# Save feature names for reference
with open(os.path.join(FEATURES_DIR, "feature_names.json"), "w") as f:
    json.dump(feature_names, f, indent=2)

print(f"    ✓ X_train_scaled.csv  — {X_train_scaled.shape}")
print(f"    ✓ X_test_scaled.csv   — {X_test_scaled.shape}")
print(f"    ✓ y_train.csv         — {y_train.shape}")
print(f"    ✓ y_test.csv          — {y_test.shape}")
print(f"    ✓ scaler.pkl")
print(f"    ✓ feature_names.json")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: Update metadata.json
# ═══════════════════════════════════════════════════════════════════════════
print("\n[7] Updating metadata.json ...")

metadata = {
    "dataset_id": 12,
    "name": "Australian Rainfall (BOM)",
    "folder": "climatology/australian-rainfall",
    "domain": "Climatology",
    "ml_task": "Binary Classification (RainToday)",
    "source": "BOM",
    "description": "145,460 daily rainfall records from 49 Australian locations. Target: RainToday (Yes/No).",
    "status": "✅ READY FOR ML",
    "has_raw_data": True,
    "has_pipeline": True,
    "pipeline": "prepare_dataset.py",
    "stats": {
        "raw_rows": int(df.shape[0]),
        "raw_columns": int(df.shape[1]),
        "feature_count": int(X.shape[1]),
        "locations": 49,
        "target_distribution": {
            "No": int(np.sum(y == 0)),
            "Yes": int(np.sum(y == 1))
        },
        "train_size": int(X_train.shape[0]),
        "test_size": int(X_test.shape[0]),
        "test_ratio": TEST_SIZE,
        "date_processed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feature_names": feature_names
    }
}

with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"    ✓ metadata.json updated")

# ═══════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  PIPELINE COMPLETE")
print("=" * 70)
print(f"\n  Raw data:      {RAW_PATH}")
print(f"  Clean data:    {clean_path}")
print(f"  Features:      {features_path}")
print(f"  ML outputs:    {FEATURES_DIR}/")
print(f"  Metadata:      {METADATA_PATH}")
print(f"\n  Features:      {X.shape[1]:,}")
print(f"  Train rows:    {X_train.shape[0]:,}")
print(f"  Test rows:     {X_test.shape[0]:,}")
print(f"  Target (1=Yes):  {np.sum(y==1):,}  ({np.mean(y)*100:.1f}%)")
print(f"  Target (0=No):   {np.sum(y==0):,}  ({(1-np.mean(y))*100:.1f}%)")
print("=" * 70)
