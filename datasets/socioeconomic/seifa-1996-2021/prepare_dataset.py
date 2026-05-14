#!/usr/bin/env python3
"""
Data preparation pipeline for SEIFA (Socio-Economic Indexes for Areas).
Australian statistical area level data, 1996-2021.
Source: Australian Bureau of Statistics (ABS)
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

XLSX = RAW / "Annual SEIFA data 1996 to 2021.xlsx"

def step(msg):
    print(f"\n{'='*80}")
    print(f"  {msg}")
    print('='*80)

# Columns expected in each state sheet
COLUMNS = [
    'sa1_code', 'year',
    'irsd_score', 'irsd_rank', 'irsd_decile', 'irsd_percentile',
    'ier_score', 'ier_rank', 'ier_decile', 'ier_percentile',
    'ieo_score', 'ieo_rank', 'ieo_decile', 'ieo_percentile',
    'irsad_score', 'irsad_rank', 'irsad_decile', 'irsad_percentile',
]

STATE_SHEETS = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT', 'OT']
STATE_NAMES = {
    'NSW': 'New South Wales', 'VIC': 'Victoria', 'QLD': 'Queensland',
    'SA': 'South Australia', 'WA': 'Western Australia', 'TAS': 'Tasmania',
    'NT': 'Northern Territory', 'ACT': 'Australian Capital Territory',
    'OT': 'Other Territories'
}

# =============================================================================
# STEP 1: LOAD AND COMBINE ALL STATE SHEETS
# =============================================================================
step("1. LOADING ALL STATE SHEETS")

chunks = []
for sheet in STATE_SHEETS:
    print(f"  Reading {sheet} ({STATE_NAMES[sheet]})...", end=' ', flush=True)
    df_state = pd.read_excel(XLSX, sheet_name=sheet, engine='openpyxl',
                             header=0, names=COLUMNS)
    df_state['state_code'] = sheet
    df_state['state_name'] = STATE_NAMES[sheet]
    chunks.append(df_state)
    print(f"{len(df_state):,} rows")

df = pd.concat(chunks, ignore_index=True)
del chunks

print(f"\n✅ Combined: {len(df):,} rows × {len(df.columns)} columns")
print(f"  States: {df['state_code'].nunique()}")
print(f"  Years: {int(df['year'].min())} - {int(df['year'].max())}")
print(f"  Unique SA1 areas: {df['sa1_code'].nunique():,}")

# =============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS
# =============================================================================
step("2. EXPLORATORY DATA ANALYSIS")

print(f"\n--- Data Types ---")
print(df.dtypes.to_string())
print(f"\n--- Missing Values (top 15) ---")
missing = df.isnull().sum().sort_values(ascending=False)
print(missing[missing > 0].head(15).to_string())
print(f"\n--- Year Distribution ---")
print(df['year'].value_counts().sort_index().head(10).to_string())
print(f"\n--- State Distribution ---")
print(df['state_code'].value_counts().to_string())
print(f"\n--- IRSD Stats ---")
print(df['irsd_score'].describe().to_string())

# =============================================================================
# STEP 3: DATA CLEANING
# =============================================================================
step("3. DATA CLEANING")

df_clean = df.copy()

# 3a. IRSAD was introduced in 2001 — fill pre-2001 with NaN and we'll handle later
n_irsad_null = df_clean['irsad_score'].isnull().sum()
print(f"  IRSAD missing (pre-2001): {n_irsad_null:,} rows ({n_irsad_null/len(df_clean)*100:.1f}%)")

# 3b. Remove any rows with missing core IRSD/IER/IEO scores (shouldn't be many)
core_cols = ['irsd_score', 'ier_score', 'ieo_score']
n_missing_core = df_clean[core_cols].isnull().any(axis=1).sum()
if n_missing_core > 0:
    df_clean = df_clean.dropna(subset=core_cols)
    print(f"  Removed {n_missing_core} rows missing core index scores")

# 3c. Fix data types
df_clean['year'] = df_clean['year'].astype(int)
df_clean['sa1_code'] = df_clean['sa1_code'].astype(np.int64)
print(f"  ✓ Fixed data types")

# 3d. Remove duplicates
dupes = df_clean.duplicated(subset=['sa1_code', 'year']).sum()
if dupes > 0:
    df_clean = df_clean.drop_duplicates(subset=['sa1_code', 'year'])
print(f"  ✓ Removed {dupes} duplicate sa1_code+year rows")

# 3e. Fill remaining NaN in IRSAD with median per year
df_clean['irsad_score'] = df_clean.groupby('year')['irsad_score'].transform(
    lambda x: x.fillna(x.median()))
df_clean['irsad_rank'] = df_clean.groupby('year')['irsad_rank'].transform(
    lambda x: x.fillna(x.median()))
df_clean['irsad_decile'] = df_clean.groupby('year')['irsad_decile'].transform(
    lambda x: x.fillna(x.median()))
df_clean['irsad_percentile'] = df_clean.groupby('year')['irsad_percentile'].transform(
    lambda x: x.fillna(x.median()))
print(f"  ✓ Filled IRSAD missing values with yearly medians")

# 3f. Outlier treatment on scores (IQR capping)
print(f"\n--- Outlier Treatment ---")
score_cols = ['irsd_score', 'ier_score', 'ieo_score', 'irsad_score']
for col in score_cols:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR  # Wider bounds for index data
    upper = Q3 + 3 * IQR
    n_before = ((df_clean[col] < lower) | (df_clean[col] > upper)).sum()
    df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
    if n_before > 0:
        print(f"  {col}: capped {n_before} extreme values")

print(f"\n✅ Cleaning complete! Shape: {df_clean.shape[0]:,} × {df_clean.shape[1]}")
print(f"  Missing values remaining: {df_clean.isnull().sum().sum():,}")

# =============================================================================
# STEP 4: FEATURE ENGINEERING
# =============================================================================
step("4. FEATURE ENGINEERING")

df_feat = df_clean.copy()

# 4a. Decade classification
df_feat['census_year'] = df_feat['year'].apply(
    lambda y: y if y in [1996, 2001, 2006, 2011, 2016, 2021] else None)
print(f"  ✓ census_year flag (census years only)")

# 4b. Socio-economic tier classification
df_feat['irsd_tier'] = pd.cut(df_feat['irsd_decile'],
    bins=[0, 3, 7, 10], labels=['disadvantaged', 'middle', 'advantaged'])
print(f"  ✓ IRSD tier: {df_feat['irsd_tier'].value_counts().to_dict()}")

# 4c. Composite advantage score (average of all index scores)
df_feat['composite_advantage'] = df_feat[['irsd_score', 'ier_score', 'ieo_score', 'irsad_score']].mean(axis=1)
print(f"  ✓ composite_advantage (mean of 4 index scores)")

# 4d. Education-Economic gap
df_feat['ieo_ier_gap'] = df_feat['ieo_score'] - df_feat['ier_score']
print(f"  ✓ ieo_ier_gap (education vs economic resources difference)")

# 4e. Region classification (broader groupings)
def broad_region(state):
    if state in ['NSW', 'ACT']: return 'NSW-ACT'
    elif state in ['VIC', 'TAS']: return 'VIC-TAS'
    elif state == 'QLD': return 'QLD'
    elif state == 'SA': return 'SA'
    elif state == 'WA': return 'WA'
    elif state == 'NT': return 'NT'
    else: return 'Other'

df_feat['region'] = df_feat['state_code'].apply(broad_region)
print(f"  ✓ Region: {df_feat['region'].value_counts().to_dict()}")

# 4f. IRSAD availability flag (was introduced in 2001)
df_feat['has_irsad'] = (df_feat['year'] >= 2001).astype(int)
print(f"  ✓ has_irsad flag")

print(f"\n✅ Feature engineering complete! Shape: {df_feat.shape[0]:,} × {df_feat.shape[1]}")

# =============================================================================
# STEP 5: SAVE CLEANED DATASET
# =============================================================================
step("5. SAVING CLEANED DATASET")

clean_csv = PROCESSED / "seifa_1996_2021_clean.csv"
# Drop raw state_code for cleaner output (keep state_name)
cols_to_drop = ['state_code'] if 'state_code' in df_feat.columns else []
df_save = df_feat.drop(columns=cols_to_drop, errors='ignore')
df_save.to_csv(clean_csv, index=False)
print(f"✓ Saved: {clean_csv}")
size_mb = os.path.getsize(clean_csv) / (1024*1024)
print(f"  Size: {size_mb:.1f} MB")
print(f"  Rows: {df_save.shape[0]:,}, Columns: {df_save.shape[1]}")

# =============================================================================
# STEP 6: PREPARE FOR ML
# =============================================================================
step("6. PREPARING ML-READY DATA")

# ML features — numeric only
ml_features = [
    'year', 'sa1_code',
    'irsd_score', 'irsd_rank', 'irsd_decile', 'irsd_percentile',
    'ier_score', 'ier_rank', 'ier_decile', 'ier_percentile',
    'ieo_score', 'ieo_rank', 'ieo_decile', 'ieo_percentile',
    'irsad_score', 'irsad_rank', 'irsad_decile', 'irsad_percentile',
    'composite_advantage', 'ieo_ier_gap',
    'has_irsad',
]

# One-hot region
region_dummies = pd.get_dummies(df_feat['region'], prefix='region', drop_first=True)
for c in region_dummies.columns:
    df_feat[c] = region_dummies[c].astype(int)
region_cols = sorted(region_dummies.columns)
ml_features += region_cols

# Filter to existing
ml_features = [c for c in ml_features if c in df_feat.columns]

# Build ML dataframe
ml_df = df_feat[ml_features].copy()
for c in ml_df.columns:
    if ml_df[c].dtype == bool:
        ml_df[c] = ml_df[c].astype(int)
    ml_df[c] = pd.to_numeric(ml_df[c], errors='coerce').fillna(0)

print(f"Total ML features: {len(ml_features)}")
print(f"ML data shape: {ml_df.shape[0]:,} × {ml_df.shape[1]}")

# Default target: IRSD score (socioeconomic disadvantage)
X = ml_df
y = df_feat['irsd_score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=ml_features)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=ml_features)

print(f"✓ Train: {X_train_scaled_df.shape[0]:,} × {X_train_scaled_df.shape[1]}")
print(f"✓ Test:  {X_test_scaled_df.shape[0]:,} × {X_test_scaled_df.shape[1]}")

# Save
X_train_scaled_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
X_test_scaled_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=['irsd_score'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=['irsd_score'])

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print(f"✓ All ML files saved to {FEATURES}/")

# =============================================================================
# STEP 7: CREATE METADATA
# =============================================================================
step("7. CREATING METADATA")

metadata = {
    "dataset_name": "seifa-1996-2021",
    "title": "Socio-Economic Indexes for Areas (SEIFA) — Australia, 1996-2021",
    "source": "Australian Bureau of Statistics (ABS)",
    "source_url": "https://www.abs.gov.au/statistics/people/people-communities/socio-economic-indexes-areas-seifa",
    "license": "ABS Data — © Commonwealth of Australia, CC BY 4.0",
    "created_date": str(datetime.now()),
    "description": "SEIFA data for Australian Statistical Area 1 (SA1) regions from 1996-2021. Contains four indexes: IRSD (Relative Socio-economic Disadvantage), IER (Economic Resources), IEO (Education and Occupation), and IRSAD (Relative Socio-economic Advantage and Disadvantage). Each index includes score, rank, decile, and percentile.",
    "indexes": {
        "IRSD": "Index of Relative Socio-economic Disadvantage",
        "IER": "Index of Economic Resources",
        "IEO": "Index of Education and Occupation",
        "IRSAD": "Index of Relative Socio-economic Advantage and Disadvantage"
    },
    "years_covered": "1996-2021 (annual)",
    "census_years": [1996, 2001, 2006, 2011, 2016, 2021],
    "geography": "SA1 (Statistical Area 1)",
    "states_territories": list(STATE_NAMES.values()),
    "rows_original": int(len(df)),
    "rows_clean": int(len(df_feat)),
    "columns_clean": int(df_feat.shape[1]),
    "features_for_ml": len(ml_features),
    "unique_sa1_areas": int(df['sa1_code'].nunique()),
    "default_target": "irsd_score (Index of Relative Socio-economic Disadvantage score)",
    "file_size_mb": round(float(os.path.getsize(XLSX) / (1024*1024)), 1),
    "train_samples": len(X_train),
    "test_samples": len(X_test),
    "ml_features": ml_features,
    "cleaning_steps": [
        "Combined 9 state/territory sheets into unified dataset",
        "Fixed data types (year as int, SA1 code as int64)",
        "Removed duplicate sa1_code+year entries",
        "Filled IRSAD (pre-2001) missing values with yearly medians",
        "Capped extreme outliers on index scores (3× IQR)",
        "Created composite advantage score (mean of 4 indexes)",
        "Created education-economic gap feature",
        "Classified socioeconomic tiers from deciles",
        "One-hot encoded geographic regions"
    ],
    "file_manifest": {
        "raw/Annual_SEIFA_data_1996_to_2021.xlsx": "Original ABS Excel file (12 sheets)",
        "processed/seifa_1996_2021_clean.csv": "Cleaned dataset",
        "features/X_train_scaled.csv": "Scaled training features",
        "features/X_test_scaled.csv": "Scaled test features",
        "features/y_train.csv": "Training target (irsd_score)",
        "features/y_test.csv": "Test target",
        "features/scaler.pkl": "Fitted StandardScaler",
        "metadata.json": "This metadata file",
        "README.md": "Dataset documentation",
        "DATA_PREPARATION_PROCESS.md": "Full process documentation",
        "prepare_dataset.py": "Reproducible pipeline"
    }
}

with open(BASE / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Created: {BASE / 'metadata.json'}")

# =============================================================================
# STEP 8: SUMMARY
# =============================================================================
step("8. PIPELINE COMPLETE")

print(f"""
📊 SEIFA AUSTRALIA 1996-2021 — Preparation Complete

  SA1 Areas:  {df['sa1_code'].nunique():,}
  Rows:       {len(df_feat):,}
  Years:      1996 - 2021
  States:     9 (all states + territories)
  Indexes:    IRSD · IER · IEO · IRSAD
  ML Features: {len(ml_features)}
  Train/Test:  {len(X_train):,} / {len(X_test):,}

  Files:
    {clean_csv}
    FEATURES directory with scaled ML data
""")
