#!/usr/bin/env python3
"""
Data preparation pipeline for NSW Dwelling Units dataset.
Number of dwelling units approved in NSW by sector, building type, and series type.
Source: ABS Building Approvals Australia
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

def step(msg):
    print(f"\n{'='*80}")
    print(f"  {msg}")
    print('='*80)

# =============================================================================
# STEP 1: LOAD DATA
# =============================================================================
step("1. LOADING RAW DATA")

csv_path = RAW / "nsw_dwelling_units_clean.csv"

# Read CSV: row 0 has unnamed headers, row 1 has real column names, data starts row 2
column_names = [
    "data_item_description",
    "col1",  # blank
    "col2",  # blank
    "series_type",
    "series_id",
    "series_start",
    "series_end",
    "no_obs",
    "unit",
    "data_type",
    "freq",
    "collection_month",
]

df = pd.read_csv(csv_path, header=None, skiprows=2, names=column_names, engine='python')

# Drop the copyright row and any rows with null series_id
df = df.dropna(subset=['series_id'])
# Drop rows where data_item_description contains copyright symbol
df = df[~df['data_item_description'].astype(str).str.contains('©', na=False)]

print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")

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
print(f"\n--- Series Type distribution ---")
print(df['series_type'].value_counts().to_string())
print(f"\n--- Building Type & Sector breakdown ---")
# Preview the data item descriptions
print(df['data_item_description'].head(10).to_string())

# =============================================================================
# STEP 3: DATA CLEANING & PARSING
# =============================================================================
step("3. DATA CLEANING & PARSING")

df_clean = df.copy()

# 3a. Remove duplicates
dupes_before = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()
print(f"✓ Removed {dupes_before} duplicate rows")

# 3b. Parse the data_item_description semicolon-separated fields
# Format: "Total number of dwelling units ; New South Wales ; [Building Type] ; [Sector] ;"
def parse_description(desc):
    """Parse semicolon-separated description into structured fields."""
    if pd.isna(desc):
        return pd.Series({'building_type': 'Unknown', 'sector': 'Unknown'})
    parts = [p.strip() for p in str(desc).split(';')]
    # parts[0] = "Total number of dwelling units"
    # parts[1] = "New South Wales"
    # parts[2] = building type (Houses, Dwellings excluding houses, Total (Type of Building))
    # parts[3] = sector (Private Sector, Total Sectors)
    building_type = parts[2] if len(parts) > 2 else 'Unknown'
    sector = parts[3] if len(parts) > 3 else 'Unknown'
    return pd.Series({'building_type': building_type, 'sector': sector})

parsed = df_clean['data_item_description'].apply(parse_description)
df_clean['building_type'] = parsed['building_type']
df_clean['sector'] = parsed['sector']
print(f"✓ Parsed data_item_description into building_type and sector")
print(f"\n  Building types: {df_clean['building_type'].unique()}")
print(f"  Sectors: {df_clean['sector'].unique()}")

# 3c. Parse dates
print("\n--- Date Parsing ---")
# Remove time component from datetime strings
df_clean['series_start_clean'] = pd.to_datetime(df_clean['series_start'].astype(str).str.replace(' 00:00:00', ''), errors='coerce')
df_clean['series_end_clean'] = pd.to_datetime(df_clean['series_end'].astype(str).str.replace(' 00:00:00', ''), errors='coerce')

df_clean['start_year'] = df_clean['series_start_clean'].dt.year
df_clean['end_year'] = df_clean['series_end_clean'].dt.year
df_clean['start_decade'] = (df_clean['start_year'] // 10 * 10).astype(int)
df_clean['end_decade'] = (df_clean['end_year'] // 10 * 10).astype(int)
df_clean['series_span_years'] = df_clean['end_year'] - df_clean['start_year']

print(f"✓ Parsed dates: start_year range {int(df_clean['start_year'].min())}-{int(df_clean['start_year'].max())}")
print(f"✓ Start decades: {sorted(df_clean['start_decade'].unique())}")
print(f"✓ Series span range: {int(df_clean['series_span_years'].min())} - {int(df_clean['series_span_years'].max())} years")

# 3d. Standardize building_type (clean up whitespace)
df_clean['building_type'] = df_clean['building_type'].str.strip()
df_clean['sector'] = df_clean['sector'].str.strip()

# 3e. Handle missing values
print("\n--- Missing Value Treatment ---")
numeric_cols = ['no_obs', 'collection_month', 'series_span_years']
for col in numeric_cols:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
        print(f"  {col}: filled {n_missing} missing values with median ({median_val:.2f})")

cat_cols = ['building_type', 'sector', 'series_type']
for col in cat_cols:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        df_clean[col] = df_clean[col].fillna('Unknown')
        print(f"  {col}: filled {n_missing} missing values with 'Unknown'")

# 3f. Convert no_obs and collection_month to numeric
df_clean['no_obs'] = pd.to_numeric(df_clean['no_obs'], errors='coerce')
df_clean['collection_month'] = pd.to_numeric(df_clean['collection_month'], errors='coerce')

# Fill any coercion NaNs
for col in ['no_obs', 'collection_month']:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
        print(f"  {col}: filled {n_missing} coercion NaNs with median ({median_val:.2f})")

# 3g. Create target-friendly numeric decade column
decade_map = {1980: 1980, 1990: 1990, 2000: 2000, 2010: 2010, 2020: 2020}
df_clean['decade_label'] = df_clean['start_decade'].map(decade_map)
unknown_decades = df_clean['start_decade'].isin(decade_map.keys())
if not unknown_decades.all():
    print(f"  ⚠ Some decades outside expected range: {df_clean[~unknown_decades]['start_decade'].unique()}")

print(f"\n✓ Cleaning complete! Shape: {df_clean.shape}")
print(f"✓ Missing values remaining: {df_clean.isnull().sum().sum()}")

# =============================================================================
# STEP 4: FEATURE ENGINEERING
# =============================================================================
step("4. FEATURE ENGINEERING")

df_feat = df_clean.copy()

# 4a. Create is_original, is_seasonally_adjusted, is_trend flags
print("--- Series Type Flags ---")
df_feat['is_original'] = (df_feat['series_type'] == 'Original').astype(int)
df_feat['is_seasonally_adjusted'] = (df_feat['series_type'] == 'Seasonally Adjusted').astype(int)
df_feat['is_trend'] = (df_feat['series_type'] == 'Trend').astype(int)
print(f"  ✓ is_original: {df_feat['is_original'].sum()}")
print(f"  ✓ is_seasonally_adjusted: {df_feat['is_seasonally_adjusted'].sum()}")
print(f"  ✓ is_trend: {df_feat['is_trend'].sum()}")

# 4b. Create sector encoding: Private Sector = 0, Total Sectors = 1
print("\n--- Sector Encoding ---")
sector_map = {'Private Sector': 0, 'Total Sectors': 1}
df_feat['sector_encoded'] = df_feat['sector'].map(sector_map)
# Handle any unknown sectors
df_feat['sector_encoded'] = df_feat['sector_encoded'].fillna(-1)
print(f"  ✓ sector_encoded (Private=0, Total=1)")

# 4c. One-hot encode building_type
print("\n--- Building Type Encoding ---")
building_dummies = pd.get_dummies(df_feat['building_type'], prefix='bldg', drop_first=False)
df_feat = pd.concat([df_feat, building_dummies], axis=1)
print(f"  ✓ One-hot encoded building_type → {len(building_dummies.columns)} columns")
for c in building_dummies.columns:
    print(f"     {c}: {int(building_dummies[c].sum())} occurrences")

# 4d. Create series ID prefix feature (first letter = broad category)
df_feat['series_id_prefix'] = df_feat['series_id'].astype(str).str[0]
print(f"\n  ✓ Series ID prefixes: {sorted(df_feat['series_id_prefix'].unique())}")

# 4e. Time-based features
print("\n--- Time Features ---")
# Decade as mid-point numeric
df_feat['start_decade_num'] = df_feat['start_decade'].astype(float)
# Month of series start
df_feat['start_month'] = df_feat['series_start_clean'].dt.month
# Era: pre-2000, 2000s, 2010s, 2020s
df_feat['era'] = pd.cut(
    df_feat['start_year'],
    bins=[-np.inf, 1999, 2009, 2019, np.inf],
    labels=['pre_2000', '2000s', '2010s', '2020s']
)
print(f"  ✓ start_decade_num: time-based numeric feature")
print(f"  ✓ start_month: month of series start")
print(f"  ✓ era: {df_feat['era'].value_counts().to_dict()}")

# 4f. Frequency encode series_id_prefix (low cardinality, may help)
prefix_freq = df_feat['series_id_prefix'].value_counts().to_dict()
df_feat['prefix_freq'] = df_feat['series_id_prefix'].map(prefix_freq)
print(f"  ✓ prefix_freq: frequency-encoded series_id_prefix")
print(f"     Range: [{min(prefix_freq.values())}, {max(prefix_freq.values())}]")

print(f"\n✓ Feature engineering complete! Shape: {df_feat.shape}")

# =============================================================================
# STEP 5: SAVE CLEANED DATASET
# =============================================================================
step("5. SAVING CLEANED DATASET")

# Select columns for the clean output
clean_columns = [
    'series_id', 'series_type', 'building_type', 'sector',
    'start_year', 'end_year', 'start_decade', 'series_span_years',
    'no_obs', 'collection_month',
    'is_original', 'is_seasonally_adjusted', 'is_trend',
    'sector_encoded', 'start_decade_num', 'start_month', 'era',
    'prefix_freq',
]

clean_csv = PROCESSED / "nsw_dwelling_units_clean.csv"
df_feat.to_csv(clean_csv, index=False)
print(f"✓ Saved full cleaned dataset: {clean_csv}")
print(f"  Rows: {df_feat.shape[0]}, Columns: {df_feat.shape[1]}")

# =============================================================================
# STEP 6: PREPARE FOR ML
# =============================================================================
step("6. PREPARING ML-READY DATA")

# Select numeric features for ML
ml_features = [
    'no_obs',
    'collection_month',
    'start_decade_num',
    'series_span_years',
    'start_month',
    'sector_encoded',
    'is_original',
    'is_seasonally_adjusted',
    'is_trend',
    'prefix_freq',
]
# Add all one-hot encoded building type columns
for c in building_dummies.columns:
    ml_features.append(c)

print(f"Total ML features: {len(ml_features)}")
print(f"Feature list: {ml_features}")

# Ensure all ml_features exist in df_feat
available_features = [f for f in ml_features if f in df_feat.columns]
missing_features = [f for f in ml_features if f not in df_feat.columns]
if missing_features:
    print(f"⚠ Missing features: {missing_features}")

# Create ML dataset
ml_df = df_feat[available_features].copy()

# Convert era dummies if we want to add them
era_dummies = pd.get_dummies(df_feat['era'], prefix='era', drop_first=True)
ml_df = pd.concat([ml_df, era_dummies], axis=1)
print(f"  ✓ Added era dummies: {len(era_dummies.columns)} columns")
for c in era_dummies.columns:
    print(f"     {c}")

# Update ml_features list
for c in era_dummies.columns:
    ml_features.append(c)

# Check for any remaining NaN
nan_cols = ml_df.columns[ml_df.isnull().any()].tolist()
if nan_cols:
    print(f"\n⚠ Filling NaNs in {len(nan_cols)} columns")
    for c in nan_cols:
        ml_df[c] = ml_df[c].fillna(ml_df[c].median())

# Train/test split
X = ml_df

# Target: no_obs is the main numeric target (number of observations per series)
# This is what a model would predict: how many data points a series has
y = df_feat['no_obs'].fillna(df_feat['no_obs'].median())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=ml_df.columns)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=ml_df.columns)

print(f"\n✓ Train set: {X_train_scaled_df.shape}")
print(f"✓ Test set:  {X_test_scaled_df.shape}")
print(f"✓ Features:  {len(ml_df.columns)}")

# Save ML files
X_train_scaled_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
X_test_scaled_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=['no_obs'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=['no_obs'])

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"\n✓ All ML files saved to {FEATURES}/")

# Also save the soft-mapped sector encoding for reference
sector_mapping = pd.DataFrame(list(sector_map.items()), columns=['sector', 'encoded'])
sector_mapping.to_csv(FEATURES / "sector_mapping.csv", index=False)
print(f"✓ Saved sector mapping: {FEATURES / 'sector_mapping.csv'}")

# =============================================================================
# STEP 7: CREATE METADATA
# =============================================================================
step("7. CREATING METADATA")

metadata = {
    "dataset_name": "nsw-dwelling-units",
    "title": "Number of dwelling units approved, by sector, building type, and series type - New South Wales",
    "source": "Australian Bureau of Statistics (ABS) - Building Approvals Australia",
    "source_url": "https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release#data-downloads",
    "license": "ABS Data - Commonwealth of Australia (Free use with attribution)",
    "created_date": str(datetime.now()),
    "description": "Metadata index of time series for the number of dwelling units approved in New South Wales, Australia. "
                   "Each row represents one ABS data series identified by Series ID, with information on building type "
                   "(Houses, Dwellings excluding houses, Total), sector (Private, Total), series type "
                   "(Original, Seasonally Adjusted, Trend), date range, and observation count.",
    "rows_original": int(df.shape[0]),
    "rows_clean": int(df_feat.shape[0]),
    "columns_original": int(df.shape[1]),
    "columns_clean": int(df_feat.shape[1]),
    "features_for_ml": int(len(ml_df.columns)),
    "series_count": int(df_feat.shape[0]),
    "unique_series_ids": int(df_feat['series_id'].nunique()),
    "building_types": list(df_feat['building_type'].unique()),
    "sectors": list(df_feat['sector'].unique()),
    "series_types": ["Original", "Seasonally Adjusted", "Trend"],
    "date_range": {
        "earliest_start": str(df_feat['start_year'].min()),
        "latest_end": str(df_feat['end_year'].max()),
    },
    "target_variable": "no_obs (number of observations per series)",
    "train_samples": int(len(X_train)),
    "test_samples": int(len(X_test)),
    "ml_features": list(ml_df.columns),
    "cleaning_steps": [
        "Parsed raw CSV with multi-row header structure",
        "Removed copyright/attribution rows from data",
        "Dropped duplicate rows",
        "Parsed semicolon-delimited data item descriptions into building_type (Houses, Dwellings excluding houses, Total) and sector (Private Sector, Total Sectors)",
        "Parsed date strings into structured start_year, end_year, start_decade, and series_span_years",
        "Filled numeric missing values with median",
        "Created binary flags for series type (Original, Seasonally Adjusted, Trend)",
        "Encoded sector as numeric (Private=0, Total=1)",
        "One-hot encoded building type",
        "Created time-based features: decade number, start month, era category",
        "Frequency-encoded series ID prefix",
        "StandardScaler normalization applied for ML-ready data (80/20 train/test split)"
    ],
    "file_manifest": {
        "raw/nsw_dwelling_units_clean.csv": "Original cleaned CSV from ABS source",
        "processed/nsw_dwelling_units_clean.csv": "Cleaned dataset with engineered features and parsed columns",
        "features/X_train_scaled.csv": "Scaled training features (80%)",
        "features/X_test_scaled.csv": "Scaled test features (20%)",
        "features/y_train.csv": "Training target (no_obs)",
        "features/y_test.csv": "Test target (no_obs)",
        "features/scaler.pkl": "Fitted StandardScaler for normalization",
        "features/sector_mapping.csv": "Sector to encoded value mapping",
        "metadata.json": "This metadata file",
        "README.md": "Dataset documentation and usage guide",
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
🏠 NSW DWELLING UNITS DATASET — Preparation Complete

  Original:          {df.shape[0]} rows × {df.shape[1]} columns
  Cleaned:           {df_feat.shape[0]} rows × {df_feat.shape[1]} columns
  Unique Series IDs: {int(df_feat['series_id'].nunique())}
  ML Features:       {len(ml_df.columns)}
  Train/Test:        {len(X_train)} / {len(X_test)}

  Series Types:         {list(df_feat['series_type'].unique())}
  Building Types:       {list(df_feat['building_type'].unique())}
  Sectors:              {list(df_feat['sector'].unique())}
  Date Range:           {str(df_feat['start_year'].min())} - {str(df_feat['end_year'].max())}

  Files created:
    {clean_csv}
    {FEATURES / 'X_train_scaled.csv'}
    {FEATURES / 'X_test_scaled.csv'}
    {FEATURES / 'y_train.csv'}
    {FEATURES / 'y_test.csv'}
    {FEATURES / 'scaler.pkl'}
    {FEATURES / 'sector_mapping.csv'}
    {BASE / 'metadata.json'}
""")
