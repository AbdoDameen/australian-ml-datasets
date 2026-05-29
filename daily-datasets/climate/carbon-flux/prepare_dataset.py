#!/usr/bin/env python3
"""
Carbon Flux (OzFlux) Dataset - ML-Ready Pipeline
=================================================
Loads the raw Excel file, cleans, feature-engineers, and produces
ML-ready train/test splits for NEP (Net Ecosystem Productivity) regression.

Outputs:
  - processed/carbon-flux_clean.csv       : Cleaned DataFrame (wide)
  - processed/carbon-flux_features.csv    : Feature-engineered DataFrame
  - features/X_train_scaled.csv           : Training features (scaled)
  - features/X_test_scaled.csv            : Test features (scaled)
  - features/y_train.csv                  : Training target
  - features/y_test.csv                   : Test target
  - features/scaler.pkl                   : Fitted StandardScaler
  - metadata.json                         : Updated metadata
"""

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '1991-2023全球陆地生态系统8天尺度碳通量站点观测数据集_V2.xlsx')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
FEATURES_DIR = os.path.join(BASE_DIR, 'features')
METADATA_FILE = os.path.join(BASE_DIR, 'metadata.json')

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FEATURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
print("=" * 60)
print("CARBON FLUX DATASET PIPELINE")
print("=" * 60)

print("\n[1/6] Loading data...")
df = pd.read_excel(DATA_FILE, sheet_name='data')
print(f"  Raw shape: {df.shape}")

# Keep only the 12 data columns (cols after index 11 are empty)
df = df.iloc[:, :12]

# Rename Chinese -> English
col_map = {
    '站点名': 'site_name',
    '国家': 'country',
    '生态系统类型': 'ecosystem_type',
    '纬度': 'latitude',
    '经度': 'longitude',
    '观测年份': 'year',
    '年积日': 'day_of_year',
    '净生态系统生产力NEP': 'nep',
    '总初级生产力GPP': 'gpp',
    '生态系统呼吸RE': 'ecosystem_respiration',
    '数据来源': 'data_source',
    '数据标识': 'data_id',
}
df = df.rename(columns=col_map)
df = df[list(col_map.values())]

# Save original feature counts for metadata (before one-hot encoding)
nunique_sites = int(df['site_name'].nunique())
nunique_countries = int(df['country'].nunique())
nunique_ecosystems = int(df['ecosystem_type'].nunique())

# ---------------------------------------------------------------------------
# 2. EDA
# ---------------------------------------------------------------------------
print("\n[2/6] Exploratory Data Analysis...")
print(f"  Shape: {df.shape}")
print(f"  Columns: {list(df.columns)}")
print(f"  Dtypes:\n{df.dtypes.to_string()}")
print(f"\n  Missing values (NaN):\n{df.isnull().sum().to_string()}")

# Replace -9999 (missing sentinel) with NaN for flux columns
flux_cols = ['nep', 'gpp', 'ecosystem_respiration']
for c in flux_cols:
    n_sentinel = (df[c] == -9999).sum()
    if n_sentinel > 0:
        print(f"  Replacing {n_sentinel} sentinel -9999 values in '{c}' with NaN")
        df[c] = df[c].replace(-9999, np.nan)

print(f"\n  Actual missing after sentinel replacement:\n{df.isnull().sum().to_string()}")

# Basic stats
print(f"\n  Numeric stats:\n{df[['latitude','longitude','year','day_of_year','nep','gpp','ecosystem_respiration']].describe().to_string()}")

print(f"\n  Unique sites: {nunique_sites}")
print(f"  Unique countries: {nunique_countries}")
print(f"  Unique ecosystem types: {nunique_ecosystems}")
print(f"  Year range: {df['year'].min()} - {df['year'].max()}")

# ---------------------------------------------------------------------------
# 3. Clean
# ---------------------------------------------------------------------------
print("\n[3/6] Cleaning data...")

# 3a. Drop rows where target (nep) is NaN
before = len(df)
df = df.dropna(subset=['nep'])
print(f"  Dropped {before - len(df)} rows with NaN target (nep). Remaining: {len(df)}")

# 3b. Drop rows where ALL flux features are NaN (can't impute meaningfully)
flux_feature_cols = ['gpp', 'ecosystem_respiration']
before = len(df)
df = df.dropna(subset=flux_feature_cols, how='all')
print(f"  Dropped {before - len(df)} rows with all flux features NaN. Remaining: {len(df)}")

# 3c. Impute remaining NaN in flux features with median
for c in flux_feature_cols:
    n_nan = df[c].isnull().sum()
    if n_nan > 0:
        median_val = df[c].median()
        df[c] = df[c].fillna(median_val)
        print(f"  Imputed {n_nan} NaN values in '{c}' with median ({median_val:.4f})")

# 3d. Remove extreme outliers in NEP (beyond 5 std from mean)
nep_mean = df['nep'].mean()
nep_std = df['nep'].std()
lower_bound = nep_mean - 5 * nep_std
upper_bound = nep_mean + 5 * nep_std
before = len(df)
df = df[(df['nep'] >= lower_bound) & (df['nep'] <= upper_bound)]
print(f"  Removed {before - len(df)} extreme NEP outliers (|z| > 5). Remaining: {len(df)}")

# 3e. Remove outliers in flux features too (|z| > 5)
for c in flux_feature_cols:
    before2 = len(df)
    mean_v = df[c].mean()
    std_v = df[c].std()
    df = df[(df[c] >= mean_v - 5*std_v) & (df[c] <= mean_v + 5*std_v)]
    removed = before2 - len(df)
    if removed > 0:
        print(f"  Removed {removed} extreme outliers in '{c}'")

print(f"\n  Final cleaned shape: {df.shape}")

# ---------------------------------------------------------------------------
# 4. Feature engineering
# ---------------------------------------------------------------------------
print("\n[4/6] Feature engineering...")

# 4a. Cyclical encoding of day_of_year (8-day steps: 1, 9, 17, ..., 361)
max_doy = 365.0  # full year cycle
df['doy_sin'] = np.sin(2 * np.pi * df['day_of_year'] / max_doy)
df['doy_cos'] = np.cos(2 * np.pi * df['day_of_year'] / max_doy)
print("  Added doy_sin, doy_cos (cyclical encoding of day_of_year)")

# 4b. One-hot encode categorical features
cat_cols = ['ecosystem_type', 'country']
df = pd.get_dummies(df, columns=cat_cols, prefix=cat_cols, drop_first=False, dtype=int)
print(f"  One-hot encoded {cat_cols}. Shape after: {df.shape}")

# 4c. Drop high-cardinality / non-predictive ID columns
drop_cols = ['site_name', 'data_id']
for c in drop_cols:
    if c in df.columns:
        df = df.drop(columns=[c])
        print(f"  Dropped column '{c}'")

# 4d. One-hot encode data_source (8 values, manageable)
df = pd.get_dummies(df, columns=['data_source'], prefix='source', drop_first=False, dtype=int)
print(f"  One-hot encoded data_source. Shape after: {df.shape}")

print(f"\n  Final feature-engineered shape: {df.shape}")

# ---------------------------------------------------------------------------
# Save clean + feature-engineered versions
# ---------------------------------------------------------------------------
clean_path = os.path.join(PROCESSED_DIR, 'carbon-flux_clean.csv')
df.to_csv(clean_path, index=False)
print(f"\n  Saved clean data -> {clean_path}")

features_path = os.path.join(PROCESSED_DIR, 'carbon-flux_features.csv')
df.to_csv(features_path, index=False)
print(f"  Saved features CSV -> {features_path}")

# ---------------------------------------------------------------------------
# 5. ML prep
# ---------------------------------------------------------------------------
print("\n[5/6] ML prep: train/test split + scaling...")

# Separate features and target
target_col = 'nep'
feature_cols = [c for c in df.columns if c != target_col]
X = df[feature_cols].copy()
y = df[target_col].copy()

print(f"  X shape: {X.shape}, y shape: {y.shape}")

# 80/20 stratified split (use quantile bins for stratification)
y_binned = pd.qcut(y, q=10, labels=False, duplicates='drop')
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y_binned
)

print(f"  Train: X={X_train.shape}, y={y_train.shape}")
print(f"  Test:  X={X_test.shape}, y={y_test.shape}")

# StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns.copy(), index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns.copy(), index=X_test.index)

# Save features
X_train_scaled.to_csv(os.path.join(FEATURES_DIR, 'X_train_scaled.csv'), index=False)
X_test_scaled.to_csv(os.path.join(FEATURES_DIR, 'X_test_scaled.csv'), index=False)
y_train.to_csv(os.path.join(FEATURES_DIR, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(FEATURES_DIR, 'y_test.csv'), index=False)
joblib.dump(scaler, os.path.join(FEATURES_DIR, 'scaler.pkl'))

print(f"\n  Saved X_train_scaled.csv ({X_train_scaled.shape[0]} rows, {X_train_scaled.shape[1]} cols)")
print(f"  Saved X_test_scaled.csv  ({X_test_scaled.shape[0]} rows, {X_test_scaled.shape[1]} cols)")
print(f"  Saved y_train.csv        ({len(y_train)} rows)")
print(f"  Saved y_test.csv         ({len(y_test)} rows)")
print(f"  Saved scaler.pkl")

# ---------------------------------------------------------------------------
# 6. Update metadata.json
# ---------------------------------------------------------------------------
print("\n[6/6] Updating metadata.json...")

if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r') as f:
        meta = json.load(f)
else:
    meta = {}

meta['has_pipeline'] = True
meta['pipeline_script'] = 'prepare_dataset.py'
meta['last_run'] = pd.Timestamp.now().isoformat()
meta['raw_rows'] = 156283
meta['raw_columns'] = 12
meta['clean_rows'] = len(df)
meta['clean_columns'] = X_train.shape[1] + 1  # features + target
meta['train_rows'] = int(len(y_train))
meta['test_rows'] = int(len(y_test))
meta['feature_count'] = int(X_train.shape[1])
meta['target'] = 'nep (Net Ecosystem Productivity)'
meta['task'] = 'regression'
meta['sites'] = nunique_sites
meta['countries'] = nunique_countries
meta['ecosystem_types'] = nunique_ecosystems
meta['feature_names'] = list(feature_cols)
meta['num_features'] = len(feature_cols)

with open(METADATA_FILE, 'w') as f:
    json.dump(meta, f, indent=2)

print(f"  Updated {METADATA_FILE}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
print(f"\nOriginal rows : {156283}")
print(f"Clean rows    : {len(df)}")
print(f"Features      : {X_train.shape[1]}")
print(f"Train samples : {len(y_train)}")
print(f"Test samples  : {len(y_test)}")
print(f"\nOutput files:")
print(f"  {clean_path}")
print(f"  {features_path}")
print(f"  {os.path.join(FEATURES_DIR, 'X_train_scaled.csv')}")
print(f"  {os.path.join(FEATURES_DIR, 'X_test_scaled.csv')}")
print(f"  {os.path.join(FEATURES_DIR, 'y_train.csv')}")
print(f"  {os.path.join(FEATURES_DIR, 'y_test.csv')}")
print(f"  {os.path.join(FEATURES_DIR, 'scaler.pkl')}")
print(f"  {METADATA_FILE}")
