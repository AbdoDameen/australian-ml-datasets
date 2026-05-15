#!/usr/bin/env python3
"""
Data preparation pipeline for Child Mortality dataset.
Sex ratios and levels of infant, child and under-five mortality for countries, 1970s-2000s.
Source: UN World Population Prospects 2010 Revision / UNICEF State of the World's Children 2012
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

def step(msg):
    print(f"\n{'='*80}")
    print(f"  {msg}")
    print('='*80)

# =============================================================================
# STEP 1: LOAD DATA
# =============================================================================
step("1. LOADING RAW DATA")

xls_path = RAW / "Table_S2.xls"

# Column names from the table structure (rows 3-4 in the sheet are headers)
columns = [
    "iso_code",            # A - ISO Code
    "country",             # B - Country or area
    "sex_ratio_trend",     # C - Trend estimates of sex ratios (Y/N)
    "decade",              # D - Decade (1970s, 1980s, 1990s, 2000s)
    "sex_ratio_infant",    # E - Sex ratio of mortality - infant
    "sex_ratio_child",     # F - Sex ratio of mortality - child
    "sex_ratio_under5",    # G - Sex ratio of mortality - under-five
    "imr_male",            # H - Infant mortality rate - male
    "imr_female",          # I - Infant mortality rate - female
    "imr_both",            # J - Infant mortality rate - both sexes
    "cmr_male",            # K - Child mortality rate - male
    "cmr_female",          # L - Child mortality rate - female
    "cmr_both",            # M - Child mortality rate - both sexes
    "u5mr_male",           # N - Under-five mortality rate - male
    "u5mr_female",         # O - Under-five mortality rate - female
    "u5mr_both",           # P - Under-five mortality rate - both sexes
    "method",              # Q - Method used (Loess, Linear, Average)
]

# Read skipping the first 5 rows (title + explanatory + blank + 2 header rows)
df = pd.read_excel(xls_path, sheet_name="Table S2-Methods and results",
                   engine='xlrd', header=None, skiprows=5, names=columns)

print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

# =============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS
# =============================================================================
step("2. EXPLORATORY DATA ANALYSIS")

print(f"\nShape: {df.shape}")
print(f"\n--- Data Types ---")
print(df.dtypes.to_string())
print(f"\n--- Missing Values ---")
missing = df.isnull().sum()
print(missing.to_string())
print(f"\n--- Basic Stats (Numeric) ---")
print(df.describe().to_string())
print(f"\n--- Unique Countries ---")
print(f"Total countries: {df['country'].nunique()}")
print(f"\n--- Decade distribution ---")
print(df['decade'].value_counts().to_string())
print(f"\n--- Method distribution ---")
print(df['method'].value_counts().to_string())
print(f"\n--- Trend (Y/N) distribution ---")
print(df['sex_ratio_trend'].value_counts().to_string())

# =============================================================================
# STEP 3: DATA CLEANING
# =============================================================================
step("3. DATA CLEANING")

df_clean = df.copy()

# 3a. Remove duplicates
dupes_before = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()
print(f"✓ Removed {dupes_before} duplicate rows")

# 3b. Standardize country names (strip whitespace)
df_clean['country'] = df_clean['country'].str.strip()

# 3c. Handle missing values
print("\n--- Missing Value Treatment ---")
# Numeric columns - fill with median
numeric_cols = ['sex_ratio_infant', 'sex_ratio_child', 'sex_ratio_under5',
                'imr_male', 'imr_female', 'imr_both',
                'cmr_male', 'cmr_female', 'cmr_both',
                'u5mr_male', 'u5mr_female', 'u5mr_both']

for col in numeric_cols:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
        print(f"  {col}: filled {n_missing} missing values with median ({median_val:.2f})")

# Categorical columns - fill with 'Unknown'
cat_cols = ['method']
for col in cat_cols:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        df_clean[col] = df_clean[col].fillna('Unknown')
        print(f"  {col}: filled {n_missing} missing values with 'Unknown'")

# 3d. Encode decade as numeric
print("\n--- Decade Encoding ---")
decade_map = {'1970s': 1970, '1980s': 1980, '1990s': 1990, '2000s': 2000}
df_clean['decade_num'] = df_clean['decade'].map(decade_map)
print(f"  Decade mapping: {decade_map}")

# 3e. Flag countries with reliable trend estimates
df_clean['has_trend'] = (df_clean['sex_ratio_trend'] == 'Y').astype(int)
print(f"  Created 'has_trend' flag: {df_clean['has_trend'].sum()} countries with trends")

# 3f. Outlier treatment (IQR capping for key mortality columns)
print("\n--- Outlier Treatment (IQR capping) ---")
outlier_cols = ['imr_both', 'cmr_both', 'u5mr_both', 'sex_ratio_infant']
for col in outlier_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_lower = (df_clean[col] < lower).sum()
    n_upper = (df_clean[col] > upper).sum()
    if n_lower > 0:
        df_clean[col] = df_clean[col].clip(lower=lower)
    if n_upper > 0:
        df_clean[col] = df_clean[col].clip(upper=upper)
    print(f"  {col}: capped {n_lower + n_upper} outliers (bounds: [{lower:.2f}, {upper:.2f}])")

print(f"\n✓ Cleaning complete! Shape: {df_clean.shape}")
print(f"✓ Missing values remaining: {df_clean.isnull().sum().sum()}")

# =============================================================================
# STEP 4: FEATURE ENGINEERING
# =============================================================================
step("4. FEATURE ENGINEERING")

df_feat = df_clean.copy()

# 4a. Compute derived mortality ratios
print("--- Derived Features ---")
df_feat['infant_child_ratio'] = df_feat['imr_both'] / df_feat['cmr_both'].replace(0, np.nan)
df_feat['infant_child_ratio'] = df_feat['infant_child_ratio'].fillna(df_feat['infant_child_ratio'].median())
print("  ✓ infant_child_ratio = imr_both / cmr_both")

df_feat['under5_child_ratio'] = df_feat['u5mr_both'] / df_feat['cmr_both'].replace(0, np.nan)
df_feat['under5_child_ratio'] = df_feat['under5_child_ratio'].fillna(df_feat['under5_child_ratio'].median())
print("  ✓ under5_child_ratio = u5mr_both / cmr_both")

# Mortality sex gap (female advantage)
df_feat['imr_sex_gap'] = df_feat['imr_male'] - df_feat['imr_female']
df_feat['u5mr_sex_gap'] = df_feat['u5mr_male'] - df_feat['u5mr_female']
print("  ✓ imr_sex_gap = imr_male - imr_female")
print("  ✓ u5mr_sex_gap = u5mr_male - u5mr_female")

# 4b. One-hot encode method
print("\n--- Categorical Encoding ---")
method_dummies = pd.get_dummies(df_feat['method'], prefix='method', drop_first=False)
df_feat = pd.concat([df_feat, method_dummies], axis=1)
print(f"  ✓ One-hot encoded 'method' → {len(method_dummies.columns)} columns")
for c in method_dummies.columns:
    print(f"     {c}: {method_dummies[c].sum()} occurrences")

# 4c. Frequency encode country (since it has 180+ unique values)
country_freq = df_feat['country'].value_counts().to_dict()
df_feat['country_freq'] = df_feat['country'].map(country_freq)
print(f"  ✓ Frequency-encoded 'country' (→ country_freq)")
print(f"     Country frequency range: [{min(country_freq.values())}, {max(country_freq.values())}]")

# 4d. Regional grouping by ISO code range
print("\n--- Region Assignment ---")
def assign_region(iso):
    if pd.isna(iso):
        return 'Unknown'
    iso = int(iso)
    if iso <= 20:
        return 'Northern Africa'
    elif iso <= 60:
        return 'Sub-Saharan Africa'
    elif iso <= 150:
        return 'Europe & Central Asia'
    elif iso <= 200:
        return 'Middle East & South Asia'
    elif iso <= 530:
        return 'East Asia & Pacific'
    elif iso <= 600:
        return 'Americas'
    elif iso <= 900:
        return 'Oceania'
    else:
        return 'Other'

df_feat['region'] = df_feat['iso_code'].apply(assign_region)
print(f"  ✓ Regions assigned:")
print(df_feat['region'].value_counts().to_string())

# One-hot encode region
region_dummies = pd.get_dummies(df_feat['region'], prefix='region', drop_first=True)
df_feat = pd.concat([df_feat, region_dummies], axis=1)
print(f"  ✓ One-hot encoded 'region' → {len(region_dummies.columns)} columns")

print(f"\n✓ Feature engineering complete! Shape: {df_feat.shape}")

# =============================================================================
# STEP 5: SAVE CLEANED DATASET
# =============================================================================
step("5. SAVING CLEANED DATASET")

clean_csv = PROCESSED / "child_mortality_clean.csv"
df_feat.to_csv(clean_csv, index=False)
print(f"✓ Saved: {clean_csv}")
print(f"  Rows: {df_feat.shape[0]}, Columns: {df_feat.shape[1]}")

# =============================================================================
# STEP 6: PREPARE FOR ML
# =============================================================================
step("6. PREPARING ML-READY DATA")

# Select features for ML (numeric only, drop identifiers and original text columns)
ml_features = [
    'decade_num', 'has_trend',
    'sex_ratio_infant', 'sex_ratio_child', 'sex_ratio_under5',
    'imr_male', 'imr_female', 'imr_both',
    'cmr_male', 'cmr_female', 'cmr_both',
    'u5mr_male', 'u5mr_female', 'u5mr_both',
    'infant_child_ratio', 'under5_child_ratio',
    'imr_sex_gap', 'u5mr_sex_gap',
    'country_freq',
]

# Add one-hot encoded columns
for c in method_dummies.columns:
    ml_features.append(c)
for c in region_dummies.columns:
    ml_features.append(c)

# Also add country_freq since it's numeric
print(f"Total ML features: {len(ml_features)}")
print(f"Feature list: {ml_features}")

# Create the ML dataset
ml_df = df_feat[ml_features].copy()

# Check for any remaining NaN
nan_cols = ml_df.columns[ml_df.isnull().any()].tolist()
if nan_cols:
    print(f"\n⚠ Filling NaNs in {len(nan_cols)} columns")
    for c in nan_cols:
        ml_df[c] = ml_df[c].fillna(ml_df[c].median())

# Train/test split
X = ml_df
y = df_feat['u5mr_both']  # Default target: under-five mortality rate

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=ml_features)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=ml_features)

print(f"\n✓ Train set: {X_train_scaled_df.shape}")
print(f"✓ Test set:  {X_test_scaled_df.shape}")
print(f"✓ Features:  {len(ml_features)}")

# Save ML files
X_train_scaled_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
X_test_scaled_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=['u5mr_both'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=['u5mr_both'])

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"\n✓ All ML files saved to {FEATURES}/")

# =============================================================================
# STEP 7: CREATE METADATA
# =============================================================================
step("7. CREATING METADATA")

metadata = {
    "dataset_name": "child-mortality-1970-2000",
    "title": "Sex ratios and levels of infant, child and under-five mortality for countries, 1970s-2000s",
    "source": "United Nations, World Population Prospects: The 2010 Revision; UNICEF, State of the World's Children 2012",
    "source_url": "https://www.un.org/development/desa/pd/",
    "license": "UN Data - Free use with attribution",
    "created_date": str(datetime.now()),
    "description": "Sex ratios of mortality rates for children under 5, with disaggregated infant, child and under-five mortality rates by sex for countries across four decades (1970s-2000s).",
    "rows_original": df.shape[0],
    "rows_clean": df_feat.shape[0],
    "columns_original": df.shape[1],
    "columns_clean": df_feat.shape[1],
    "features_for_ml": len(ml_features),
    "countries": int(df['country'].nunique()),
    "decades": ["1970s", "1980s", "1990s", "2000s"],
    "method_types": ["Loess - locally weighted regression",
                     "Linear - robust linear regression",
                     "Average - simple average"],
    "target_variable": "u5mr_both (under-five mortality rate, both sexes)",
    "train_samples": len(X_train),
    "test_samples": len(X_test),
    "ml_features": ml_features,
    "cleaning_steps": [
        "Removed header rows and parsed structured Excel data",
        "Standardized column names to lowercase with underscores",
        "Removed duplicate rows",
        "Filled numeric missing values with median",
        "Capped outliers using IQR method (1.5× IQR bounds)",
        "Encoded decade as numeric (1970s→1970, etc.)",
        "Created derived features: infant/child ratio, under5/child ratio, sex gaps",
        "One-hot encoded method (Loess/Linear/Average)",
        "One-hot encoded region (7 geographic regions)",
        "Frequency-encoded country names",
        "StandardScaler normalization applied for ML-ready data"
    ],
    "file_manifest": {
        "raw/Table_S2.xls": "Original Excel file from UN source",
        "processed/child_mortality_clean.csv": "Cleaned dataset with engineered features",
        "features/X_train_scaled.csv": "Scaled training features",
        "features/X_test_scaled.csv": "Scaled test features",
        "features/y_train.csv": "Training target (u5mr_both)",
        "features/y_test.csv": "Test target (u5mr_both)",
        "features/scaler.pkl": "Fitted StandardScaler",
        "metadata.json": "This metadata file",
        "README.md": "Dataset documentation",
        "DATA_PREPARATION_PROCESS.md": "Full process documentation",
        "prepare_dataset.py": "Reproducible preparation script"
    }
}

with open(BASE / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Created: {BASE / 'metadata.json'}")

# =============================================================================
# STEP 8: PRINT SUMMARY
# =============================================================================
step("8. PIPELINE COMPLETE — SUMMARY")

print(f"""
📊 CHILD MORTALITY DATASET — Preparation Complete

  Original:   {df.shape[0]} rows × {df.shape[1]} columns
  Cleaned:    {df_feat.shape[0]} rows × {df_feat.shape[1]} columns
  Countries:  {int(df['country'].nunique())}
  Decades:    1970s, 1980s, 1990s, 2000s
  ML Features: {len(ml_features)}
  Train/Test:  {len(X_train)} / {len(X_test)}

  Files created:
    {clean_csv}
    {FEATURES / 'X_train_scaled.csv'}
    {FEATURES / 'X_test_scaled.csv'}
    {FEATURES / 'y_train.csv'}
    {FEATURES / 'y_test.csv'}
    {FEATURES / 'scaler.pkl'}
    {BASE / 'metadata.json'}
""")
