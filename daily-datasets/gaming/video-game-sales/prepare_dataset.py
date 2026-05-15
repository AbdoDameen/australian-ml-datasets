#!/usr/bin/env python3
"""
Data preparation pipeline for Video Game Sales dataset.
Global sales data for 16,598 games across platforms, genres, and publishers.
Source: vgsales (public dataset)
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

with open(RAW / "vgsales.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

# =============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS
# =============================================================================
step("2. EXPLORATORY DATA ANALYSIS")

print(f"\nShape: {df.shape}")
print(f"\n--- Columns ---")
print(list(df.columns))
print(f"\n--- Data Types ---")
print(df.dtypes.to_string())
print(f"\n--- Missing Values ---")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.sum() > 0 else "  No missing values!")
print(f"\n--- Years Covered ---")
print(f"  Range: {int(df['Year'].min())} - {int(df['Year'].max())}")
print(f"  Null years: {df['Year'].isnull().sum()}")
print(f"\n--- Top 10 Publishers ---")
print(df['Publisher'].value_counts().head(10).to_string())
print(f"\n--- Genres ---")
print(df['Genre'].value_counts().to_string())
print(f"\n--- Platforms ---")
print(f"Total platforms: {df['Platform'].nunique()}")
print(df['Platform'].value_counts().head(10).to_string())
print(f"\n--- Basic Stats (Sales in millions) ---")
print(df.describe().to_string())

# =============================================================================
# STEP 3: DATA CLEANING
# =============================================================================
step("3. DATA CLEANING")

df_clean = df.copy()

# 3a. Standardize column names
df_clean.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df_clean.columns]
print(f"✓ Standardized column names")

# 3b. Handle missing Year values
n_missing_year = df_clean['year'].isnull().sum()
if n_missing_year > 0:
    median_year = df_clean['year'].median()
    df_clean['year'] = df_clean['year'].fillna(median_year)
    print(f"  year: filled {n_missing_year} missing values with median ({int(median_year)})")

# 3c. Handle missing Publisher
n_missing_pub = df_clean['publisher'].isnull().sum()
if n_missing_pub > 0:
    df_clean['publisher'] = df_clean['publisher'].fillna('Unknown')
    print(f"  publisher: filled {n_missing_pub} missing values with 'Unknown'")

# 3d. Clean text fields
df_clean['name'] = df_clean['name'].str.strip()
df_clean['publisher'] = df_clean['publisher'].str.strip()
df_clean['genre'] = df_clean['genre'].str.strip()
df_clean['platform'] = df_clean['platform'].str.strip()
print(f"✓ Cleaned text fields")

# 3e. Remove duplicates
dupes_before = df_clean.duplicated(subset=['name', 'platform']).sum()
df_clean = df_clean.drop_duplicates(subset=['name', 'platform'])
print(f"✓ Removed {dupes_before} duplicate games (same name + platform)")

# 3f. Year as integer
df_clean['year'] = df_clean['year'].astype(int)
print(f"✓ Converted year to integer")

# 3g. Sales per region as percentage of global
print("\n--- Regional Sales Share ---")
for region in ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']:
    share_col = f'{region}_share'
    df_clean[share_col] = df_clean[region] / df_clean['global_sales'].replace(0, np.nan)
    df_clean[share_col] = df_clean[share_col].fillna(0)
    print(f"  ✓ Created {share_col}")

# 3h. Outlier treatment (IQR capping)
print("\n--- Outlier Treatment ---")
sales_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales', 'global_sales']
for col in sales_cols:
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
    if n_lower + n_upper > 0:
        print(f"  {col}: capped {n_lower + n_upper} outliers")

print(f"\n✓ Cleaning complete! Shape: {df_clean.shape}")
print(f"✓ Missing values remaining: {df_clean.isnull().sum().sum()}")

# =============================================================================
# STEP 4: FEATURE ENGINEERING
# =============================================================================
step("4. FEATURE ENGINEERING")

df_feat = df_clean.copy()

# 4a. Platform generation / era
print("--- Platform Era ---")
def platform_era(platform):
    era_map = {
        'NES': 'Retro', 'GB': 'Retro', 'SNES': 'Retro', 'N64': 'Retro',
        'GEN': 'Retro', 'SAT': 'Retro', 'DC': 'Retro', 'PS': 'Retro',
        'PS2': '6th Gen', 'Xbox': '6th Gen', 'GC': '6th Gen', 'GBA': '6th Gen',
        'PS3': '7th Gen', 'X360': '7th Gen', 'Wii': '7th Gen', 'NDS': '7th Gen', 'PSP': '7th Gen',
        'PS4': '8th Gen', 'XOne': '8th Gen', 'WiiU': '8th Gen', '3DS': '8th Gen', 'PSV': '8th Gen',
        'PC': 'PC', '2600': 'Retro'
    }
    return era_map.get(platform, 'Other')

df_feat['platform_era'] = df_feat['platform'].apply(platform_era)
print(f"  Era distribution: {df_feat['platform_era'].value_counts().to_dict()}")

# 4b. Top publisher flag
top_publishers = df_feat['publisher'].value_counts().head(10).index.tolist()
df_feat['is_top_publisher'] = df_feat['publisher'].isin(top_publishers).astype(int)
print(f"  ✓ is_top_publisher flag ({len(top_publishers)} publishers)")

# 4c. Publisher frequency encoding
pub_freq = df_feat['publisher'].value_counts().to_dict()
df_feat['publisher_games_count'] = df_feat['publisher'].map(pub_freq)
print("  ✓ publisher_games_count (frequency encoding)")

# 4d. Game name length feature
df_feat['name_length'] = df_feat['name'].str.len()
print("  ✓ name_length feature")

# 4e. Decade category
df_feat['decade'] = (df_feat['year'] // 10 * 10).astype(int)
print(f"  ✓ Decade distribution: {df_feat['decade'].value_counts().sort_index().to_dict()}")

# 4f. One-hot encode categoricals
print("\n--- Categorical Encoding ---")
cat_cols = ['genre', 'platform_era']
for col in cat_cols:
    dummies = pd.get_dummies(df_feat[col], prefix=col, drop_first=False)
    # Convert bool to int
    for c in dummies.columns:
        df_feat[c] = dummies[c].astype(int)
    print(f"  ✓ One-hot encoded '{col}' → {len(dummies.columns)} columns")

# Label encode platform (too many unique values for one-hot)
platform_freq = df_feat['platform'].value_counts().to_dict()
df_feat['platform_freq'] = df_feat['platform'].map(platform_freq)
print("  ✓ Frequency-encoded 'platform'")

# Label encode publisher (high cardinality)
# Already have publisher_games_count which is equivalent

print(f"\n✓ Feature engineering complete! Shape: {df_feat.shape}")

# =============================================================================
# STEP 5: SAVE CLEANED DATASET
# =============================================================================
step("5. SAVING CLEANED DATASET")

clean_csv = PROCESSED / "video_game_sales_clean.csv"
cols_to_drop = ['rank'] if 'rank' in df_feat.columns else []
df_save = df_feat.drop(columns=cols_to_drop, errors='ignore')
df_save.to_csv(clean_csv, index=False)
print(f"✓ Saved: {clean_csv}")
print(f"  Rows: {df_save.shape[0]}, Columns: {df_save.shape[1]}")

# =============================================================================
# STEP 6: PREPARE FOR ML
# =============================================================================
step("6. PREPARING ML-READY DATA")

# Select ML features
ml_features = [
    'year', 'na_sales', 'eu_sales', 'jp_sales', 'other_sales',
    'na_sales_share', 'eu_sales_share', 'jp_sales_share', 'other_sales_share',
    'publisher_games_count', 'platform_freq', 'name_length',
    'is_top_publisher',
]

# Add one-hot columns
genre_cols = [c for c in df_feat.columns if c.startswith('genre_')]
era_cols = [c for c in df_feat.columns if c.startswith('platform_era_')]
ml_features += genre_cols + era_cols

# Filter to existing columns
ml_features = [c for c in ml_features if c in df_feat.columns]
print(f"Total ML features: {len(ml_features)}")

# Create ML dataset — ensure all numeric
ml_df = df_feat[ml_features].copy()
for c in ml_df.columns:
    if ml_df[c].dtype == bool:
        ml_df[c] = ml_df[c].astype(int)

# Default target: global_sales
X = ml_df
y = df_feat['global_sales']

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

# Save ML files
X_train_scaled_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
X_test_scaled_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=['global_sales'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=['global_sales'])

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print(f"\n✓ All ML files saved to {FEATURES}/")

# =============================================================================
# STEP 7: CREATE METADATA
# =============================================================================
step("7. CREATING METADATA")

metadata = {
    "dataset_name": "video-game-sales",
    "title": "Video Game Sales — Global Sales Data (16,598 Games)",
    "source": "vgsales public dataset",
    "source_url": "",
    "license": "Public domain data",
    "created_date": str(datetime.now()),
    "description": "Global video game sales data covering 16,598 titles across platforms, genres, and publishers. Includes sales in millions by region (NA, EU, JP, Other) and globally.",
    "rows_original": df.shape[0],
    "rows_clean": df_feat.shape[0],
    "columns_clean": df_feat.shape[1],
    "features_for_ml": len(ml_features),
    "years_covered": f"{int(df['Year'].min())} - {int(df['Year'].max())}",
    "unique_platforms": int(df['Platform'].nunique()),
    "unique_genres": int(df['Genre'].nunique()),
    "unique_publishers": int(df['Publisher'].nunique()),
    "default_target": "global_sales (in millions)",
    "units": "Sales figures in millions of units",
    "train_samples": len(X_train),
    "test_samples": len(X_test),
    "ml_features": ml_features,
    "cleaning_steps": [
        "Standardized column names to lowercase",
        "Filled missing year values with median",
        "Filled missing publisher values with 'Unknown'",
        "Removed duplicate game entries (same name + platform)",
        "Converted year to integer type",
        "Created regional sales share features (NA, EU, JP, Other as % of global)",
        "Capped outliers using IQR method",
        "Created platform era classification (Retro, 6th Gen, 7th Gen, 8th Gen, PC)",
        "Flagged top 10 publishers",
        "Frequency-encoded publisher and platform",
        "Game name length feature",
        "Decade categorization",
        "One-hot encoded genre and platform era",
        "StandardScaler normalization for ML-ready data"
    ],
    "file_manifest": {
        "raw/vgsales.json": "Original JSON data",
        "raw/vgsales.md": "Original markdown table",
        "processed/video_game_sales_clean.csv": "Cleaned dataset with engineered features",
        "features/X_train_scaled.csv": "Scaled training features",
        "features/X_test_scaled.csv": "Scaled test features",
        "features/y_train.csv": "Training target (global_sales)",
        "features/y_test.csv": "Test target (global_sales)",
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
# STEP 8: SUMMARY
# =============================================================================
step("8. PIPELINE COMPLETE — SUMMARY")

print(f"""
🎮 VIDEO GAME SALES — Preparation Complete

  Games:       {len(df_feat):,}
  Years:       {int(df['Year'].min())}-{int(df['Year'].max())}
  Platforms:   {int(df['Platform'].nunique())}
  Genres:      {int(df['Genre'].nunique())}
  Publishers:  {int(df['Publisher'].nunique())}
  ML Features: {len(ml_features)}
  Train/Test:  {len(X_train):,} / {len(X_test):,}

  Files created:
    {clean_csv}
    {FEATURES / 'X_train_scaled.csv'}
    {FEATURES / 'X_test_scaled.csv'}
    {FEATURES / 'y_train.csv'}
    {FEATURES / 'y_test.csv'}
    {FEATURES / 'scaler.pkl'}
    {BASE / 'metadata.json'}
""")
