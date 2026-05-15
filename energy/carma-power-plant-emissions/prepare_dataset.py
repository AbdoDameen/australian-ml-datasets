#!/usr/bin/env python3
"""
Data preparation pipeline for CARMA Australia Power Plant Emissions dataset.
Covers 2000, 2007, and Future projected emissions for 481 power plants.
Source: Carbon Monitoring for Action (CARMA) — http://carma.org/
"""

import pandas as pd
import numpy as np
import json
import os
import re
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
# STEP 1: EXTRACT DATA FROM PDF (GeoJSON embedded)
# =============================================================================
step("1. EXTRACTING RAW DATA")

pdf_path = RAW / "CARMA AUSTRALIA power plant emissions 2000 - 2007.pdf"

# Extract text from PDF
import subprocess
result = subprocess.run(['pdftotext', '-raw', str(pdf_path), '-'],
                       capture_output=True, text=True)
raw_text = result.stdout

# Clean and parse GeoJSON
clean_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', raw_text)
geojson = json.loads(clean_text)

print(f"FeatureCollection with {len(geojson['features'])} power plants")

# Build dataframe from features
records = []
for f in geojson['features']:
    props = f['properties'].copy()
    # Split concatenated names (PDF extraction joins them)
    records.append(props)

df = pd.DataFrame(records)
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
print(f"\n--- Unique States ---")
print(df['state'].value_counts().to_string())
print(f"\n--- Unique Cities ---")
print(f"Total cities: {df['city_name'].nunique()}")
print(f"\n--- Top 10 Companies by Plant Count ---")
print(df['company_id'].value_counts().head(10).to_string())
print(f"\n--- Numeric Stats ---")
print(df.describe().to_string())

# =============================================================================
# STEP 3: DATA CLEANING
# =============================================================================
step("3. DATA CLEANING")

df_clean = df.copy()

# 3a. Clean plant names (remove PDF concatenation artifacts)
df_clean['name'] = df_clean['name'].str.strip()
print(f"✓ Cleaned plant names")

# 3b. Clean company names
df_clean['company_id'] = df_clean['company_id'].str.strip()
df_clean['parentcomp_id'] = df_clean['parentcomp_id'].fillna('').str.strip()
df_clean['parentcomp_id'] = df_clean['parentcomp_id'].replace('', 'Unknown')
print(f"✓ Cleaned company/parent names")

# 3c. Remove duplicates
dupes_before = df_clean.duplicated(subset=['plant_id']).sum()
df_clean = df_clean.drop_duplicates(subset=['plant_id'])
print(f"✓ Removed {dupes_before} duplicate plant_ids")

# 3d. Handle missing values in numeric columns
numeric_cols = ['carbon_2000', 'carbon_2007', 'carbon_nextdecade',
                'energy_2000', 'energy_2007', 'energy_nextdecade',
                'intensity_2000', 'intensity_2007', 'intensity_nextdecade']

for col in numeric_cols:
    n_missing = df_clean[col].isnull().sum()
    if n_missing > 0:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
        print(f"  {col}: filled {n_missing} missing values with median ({median_val:.2f})")

# 3e. Standardize state names
state_map = {
    'New South Wales': 'NSW', 'Queensland': 'QLD', 'Victoria': 'VIC',
    'Western Australia': 'WA', 'South Australia': 'SA',
    'Tasmania': 'TAS', 'Australian Capital Territory': 'ACT',
    'Northern Territory': 'NT'
}
df_clean['state_code'] = df_clean['state'].map(state_map).fillna(df_clean['state'])
print(f"✓ Created state codes")

# 3f. Classify plant type by intensity/carbon profile
print("\n--- Plant Classification ---")
# Zero-carbon plants (renewables like wind, solar, hydro)
df_clean['is_renewable'] = ((df_clean['carbon_2007'] == 0) & 
                             (df_clean['intensity_2007'] == 0)).astype(int)
n_renewable = df_clean['is_renewable'].sum()
print(f"  Renewable plants (zero emissions): {n_renewable}")
print(f"  Fossil fuel plants: {df_clean.shape[0] - n_renewable}")

# Carbon intensity classification for non-renewable
df_clean['intensity_category'] = 'unknown'
mask = df_clean['intensity_2007'] > 0
df_clean.loc[mask & (df_clean['intensity_2007'] < 500), 'intensity_category'] = 'low'
df_clean.loc[mask & (df_clean['intensity_2007'] >= 500) & (df_clean['intensity_2007'] < 1500), 'intensity_category'] = 'medium'
df_clean.loc[mask & (df_clean['intensity_2007'] >= 1500), 'intensity_category'] = 'high'
print(f"  Intensity categories: {df_clean['intensity_category'].value_counts().to_dict()}")

# 3g. Outlier treatment (IQR capping)
print("\n--- Outlier Treatment ---")
outlier_cols = ['carbon_2007', 'energy_2007', 'carbon_2000', 'energy_2000',
                'carbon_nextdecade', 'energy_nextdecade']
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
    if n_lower + n_upper > 0:
        print(f"  {col}: capped {n_lower + n_upper} outliers")

print(f"\n✓ Cleaning complete! Shape: {df_clean.shape}")
print(f"✓ Missing values remaining: {df_clean.isnull().sum().sum()}")

# =============================================================================
# STEP 4: FEATURE ENGINEERING
# =============================================================================
step("4. FEATURE ENGINEERING")

df_feat = df_clean.copy()

# 4a. Derived features
print("--- Temporal Changes ---")
df_feat['carbon_change_2000_2007'] = df_feat['carbon_2007'] - df_feat['carbon_2000']
df_feat['carbon_change_2007_future'] = df_feat['carbon_nextdecade'] - df_feat['carbon_2007']
df_feat['energy_change_2000_2007'] = df_feat['energy_2007'] - df_feat['energy_2000']
df_feat['energy_change_2007_future'] = df_feat['energy_nextdecade'] - df_feat['energy_2007']
print("  ✓ carbon change 2000→2007, 2007→Future")
print("  ✓ energy change 2000→2007, 2007→Future")

# Growth flags
df_feat['carbon_growing'] = (df_feat['carbon_change_2000_2007'] > 0).astype(int)
df_feat['carbon_declining'] = (df_feat['carbon_change_2000_2007'] < 0).astype(int)
print("  ✓ carbon_growing / carbon_declining flags")

# 4b. Emission intensity tiers
df_feat['is_high_emitter'] = (df_feat['carbon_2007'] > df_feat['carbon_2007'].median()).astype(int)
print("  ✓ is_high_emitter flag (above median)")

# 4c. Clean energy ratio
df_feat['is_clean_plant'] = ((df_feat['intensity_2007'] == 0) | 
                              (df_feat['carbon_2007'] == 0)).astype(int)
print("  ✓ is_clean_plant flag")

# 4d. Plant size category by energy output
print("\n--- Plant Size Classification ---")
def size_category(row):
    e = row['energy_2007']
    if e == 0: return 'zero'
    elif e < 1000: return 'small'
    elif e < 100000: return 'medium'
    elif e < 1000000: return 'large'
    else: return 'mega'

df_feat['size_category'] = df_feat.apply(size_category, axis=1)
print(f"  Size distribution: {df_feat['size_category'].value_counts().to_dict()}")

# 4e. Regional classification
print("\n--- Region Assignment ---")
def assign_region(state):
    if state in ['New South Wales', 'ACT']:
        return 'NSW-ACT'
    elif state in ['Victoria']:
        return 'Victoria'
    elif state in ['Queensland']:
        return 'Queensland'
    elif state in ['Western Australia']:
        return 'Western Australia'
    elif state in ['South Australia']:
        return 'South Australia'
    elif state in ['Tasmania']:
        return 'Tasmania'
    elif state in ['Northern Territory']:
        return 'Northern Territory'
    else:
        return 'Other'

df_feat['region'] = df_feat['state'].apply(assign_region)
print(f"  Region distribution: {df_feat['region'].value_counts().to_string()}")

# 4f. One-hot encode categoricals
print("\n--- Categorical Encoding ---")
cat_cols = ['intensity_category', 'size_category', 'state', 'region']
for col in cat_cols:
    dummies = pd.get_dummies(df_feat[col], prefix=col, drop_first=(col != 'state'))
    df_feat = pd.concat([df_feat, dummies], axis=1)
    print(f"  ✓ One-hot encoded '{col}' → {len(dummies.columns)} columns")

# 4g. Company frequency encoding
company_freq = df_feat['company_id'].value_counts().to_dict()
parent_freq = df_feat['parentcomp_id'].value_counts().to_dict()
df_feat['company_plants_count'] = df_feat['company_id'].map(company_freq)
df_feat['parent_plants_count'] = df_feat['parentcomp_id'].map(parent_freq)
print("  ✓ Frequency-encoded company_id, parentcomp_id")

print(f"\n✓ Feature engineering complete! Shape: {df_feat.shape}")
print(f"  Total columns now: {df_feat.shape[1]}")

# =============================================================================
# STEP 5: SAVE CLEANED DATASET
# =============================================================================
step("5. SAVING CLEANED DATASET")

clean_csv = PROCESSED / "carma_australia_emissions_clean.csv"
# Don't save geometry/id columns to CSV (keep clean tabular data)
cols_to_drop = ['id'] if 'id' in df_feat.columns else []
df_save = df_feat.drop(columns=cols_to_drop, errors='ignore')
df_save.to_csv(clean_csv, index=False)
print(f"✓ Saved: {clean_csv}")
print(f"  Rows: {df_save.shape[0]}, Columns: {df_save.shape[1]}")

# =============================================================================
# STEP 6: PREPARE FOR ML
# =============================================================================
step("6. PREPARING ML-READY DATA")

# Select ML features (numeric only)
ml_features_base = [
    'carbon_2000', 'carbon_2007', 'carbon_nextdecade',
    'energy_2000', 'energy_2007', 'energy_nextdecade',
    'intensity_2000', 'intensity_2007', 'intensity_nextdecade',
    'latitude', 'longitude',
    'plant_id',
    'carbon_change_2000_2007', 'carbon_change_2007_future',
    'energy_change_2000_2007', 'energy_change_2007_future',
    'company_plants_count', 'parent_plants_count',
]

# Add binary flags
flag_cols = ['is_renewable', 'carbon_growing', 'carbon_declining',
             'is_high_emitter', 'is_clean_plant']

# Add one-hot encoded columns (boolean → convert to int)
state_dummies = [c for c in df_feat.columns if c.startswith('state_') and c != 'state']
region_dummies = [c for c in df_feat.columns if c.startswith('region_') and c != 'region']
intensity_dummies = [c for c in df_feat.columns if c.startswith('intensity_category_')]
size_dummies = [c for c in df_feat.columns if c.startswith('size_category_') and c != 'size_category']

all_ml_cols = ml_features_base + flag_cols + state_dummies + region_dummies + intensity_dummies + size_dummies
print(f"Total ML features: {len(all_ml_cols)}")

# Create ML dataset — only select numeric types
# Convert boolean one-hot columns to int first
for c in state_dummies + region_dummies + intensity_dummies + size_dummies:
    if c in df_feat.columns and df_feat[c].dtype == bool:
        df_feat[c] = df_feat[c].astype(int)

df_feat_numeric = df_feat[all_ml_cols].select_dtypes(include=[np.number])
print(f"Numeric columns in ML set: {len(df_feat_numeric.columns)}")
dropped = set(all_ml_cols) - set(df_feat_numeric.columns)
if dropped:
    print(f"Dropped non-numeric columns: {dropped}")
all_ml_cols = list(df_feat_numeric.columns)

# Create ML dataset
ml_df = df_feat_numeric.copy()

# Fill any remaining NaN
for c in ml_df.columns:
    if ml_df[c].isnull().any():
        ml_df[c] = ml_df[c].fillna(ml_df[c].median())

# Default target: carbon_2007 (CO2 emissions in short tons)
X = ml_df
y = df_feat['carbon_2007']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=all_ml_cols)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=all_ml_cols)

print(f"\n✓ Train set: {X_train_scaled_df.shape}")
print(f"✓ Test set:  {X_test_scaled_df.shape}")

# Save ML files
X_train_scaled_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
X_test_scaled_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=['carbon_2007'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=['carbon_2007'])

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"\n✓ All ML files saved to {FEATURES}/")

# =============================================================================
# STEP 7: CREATE METADATA
# =============================================================================
step("7. CREATING METADATA")

metadata = {
    "dataset_name": "carma-power-plant-emissions",
    "title": "CARMA Australia Power Plant Emissions, Australia, 2000/2007/Future",
    "source": "Carbon Monitoring for Action (CARMA)",
    "source_url": "http://carma.org/region/detail/18",
    "citation": "carma.org — Carbon Monitoring for Action",
    "license": "CARMA public data — Free use with attribution",
    "created_date": str(datetime.now()),
    "description": "CO2 emissions data for 481 Australian power plants across three time periods (2000, 2007, projected future). Includes plant name, company, location, carbon emissions (short tons), energy output (MWh), and carbon intensity (lbs CO2/MWh).",
    "publish_date": "2007-11-15",
    "rows_original": df.shape[0],
    "rows_clean": df_feat.shape[0],
    "columns_clean": df_feat.shape[1],
    "features_for_ml": len(all_ml_cols),
    "power_plants": int(len(df_feat)),
    "states": list(df_feat['state'].unique()),
    "renewable_plants": int(n_renewable),
    "fossil_fuel_plants": int(df_feat.shape[0] - n_renewable),
    "time_periods": ["2000 (Annual Report)", "2007 (Present)", "Future (Projected)"],
    "default_target": "carbon_2007 (CO2 emissions in short tons)",
    "units": {
        "carbon": "Short tons CO2 (×0.907 for metric tons)",
        "energy": "MWh per year",
        "intensity": "lbs CO2 per MWh"
    },
    "train_samples": len(X_train),
    "test_samples": len(X_test),
    "ml_features": all_ml_cols,
    "cleaning_steps": [
        "Extracted GeoJSON data from PDF source file",
        "Cleaned plant names and company names (PDF concatenation artifacts)",
        "Removed duplicate plant entries",
        "Created state codes (NSW, QLD, VIC, etc.)",
        "Classified renewable vs fossil fuel plants",
        "Created carbon intensity categories (low/medium/high)",
        "Capped outliers using IQR method",
        "Engineered temporal change features (2000→2007→Future)",
        "Created size categories (zero/small/medium/large/mega)",
        "One-hot encoded state, region, intensity category, size category",
        "Frequency-encoded company and parent company",
        "StandardScaler normalization applied for ML-ready data"
    ],
    "file_manifest": {
        "raw/CARMA_Australia_Power_Plant_Emissions.pdf": "Original CARMA dataset PDF",
        "processed/carma_australia_emissions_clean.csv": "Cleaned dataset with engineered features",
        "features/X_train_scaled.csv": "Scaled training features",
        "features/X_test_scaled.csv": "Scaled test features",
        "features/y_train.csv": "Training target (carbon_2007)",
        "features/y_test.csv": "Test target (carbon_2007)",
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
# STEP 8: PIPELINE SUMMARY
# =============================================================================
step("8. PIPELINE COMPLETE — SUMMARY")

print(f"""
🏭 CARMA AUSTRALIA POWER PLANT EMISSIONS — Preparation Complete

  Power Plants:  {len(df_feat)}
  States:        {df_feat['state'].nunique()}
  Time Periods:  2000 · 2007 · Future
  ML Features:   {len(all_ml_cols)}
  Train/Test:    {len(X_train)} / {len(X_test)}

  Plants by type:
    Renewable:   {n_renewable} ({n_renewable/len(df_feat)*100:.0f}%)
    Fossil fuel: {len(df_feat) - n_renewable} ({(len(df_feat) - n_renewable)/len(df_feat)*100:.0f}%)

  Files created:
    {clean_csv}
    {FEATURES / 'X_train_scaled.csv'}
    {FEATURES / 'X_test_scaled.csv'}
    {FEATURES / 'y_train.csv'}
    {FEATURES / 'y_test.csv'}
    {FEATURES / 'scaler.pkl'}
    {BASE / 'metadata.json'}
""")
