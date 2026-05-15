#!/usr/bin/env python3
"""
Standardised pipeline for Australian aircraft register dataset.
Loads raw CSV, cleans, feature engineers, and saves processed data + ML features.
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.preprocessing import StandardScaler, LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(BASE_DIR, "raw", "aircraft_register_clean.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
FEATURES_DIR = os.path.join(BASE_DIR, "features")
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FEATURES_DIR, exist_ok=True)

print("=" * 60)
print("AUSTRALIAN AIRCRAFT REGISTER - DATA PREPARATION PIPELINE")
print("=" * 60)

# ---------------------------------------------------------------------------
# 1. LOAD RAW DATA
# ---------------------------------------------------------------------------
print("\n[1/6] Loading raw CSV ...")
df = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False)
print(f"  Rows: {len(df):,}")
print(f"  Columns: {len(df.columns)}")

# ---------------------------------------------------------------------------
# 2. STRIP STRINGS & STANDARDISE COLUMN NAMES
# ---------------------------------------------------------------------------
print("\n[2/6] Cleaning strings and standardising column names ...")

# Strip whitespace from all string cells
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Standardise column names: lowercase, strip, underscore-separated
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

print(f"  Standardised columns ({len(df.columns)}):")
for c in df.columns:
    print(f"    - {c}")

# ---------------------------------------------------------------------------
# 3. HANDLE MISSING / PLACEHOLDER VALUES
# ---------------------------------------------------------------------------
print("\n[3/6] Handling missing and placeholder values ...")

# Replace common empty/placeholder strings with NaN
placeholder_values = {"", "na", "n/a", "none", "nil", "-", "--", "?"}
for col in df.columns:
    df[col] = df[col].replace(placeholder_values, np.nan)

# For numeric columns, coerce and fill NA
numeric_cols = ["mtow", "engnum", "yearmanu"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        na_count = df[col].isna().sum()
        if na_count > 0:
            fill_val = df[col].median()
            df[col] = df[col].fillna(fill_val)
            print(f"  {col}: filled {na_count:,} NA values with median ({fill_val})")

# For categorical / string columns, fill NA with "Unknown"
string_cols = [c for c in df.columns if c not in numeric_cols]
for col in string_cols:
    na_count = df[col].isna().sum()
    if na_count > 0:
        df[col] = df[col].fillna("Unknown")
        print(f"  {col}: filled {na_count:,} NA values with 'Unknown'")

# ---------------------------------------------------------------------------
# 4. FEATURE ENGINEERING
# ---------------------------------------------------------------------------
print("\n[4/6] Feature engineering ...")

# 4a. Year of manufacture -> Decade
if "yearmanu" in df.columns:
    valid_year = df["yearmanu"].notna() & (df["yearmanu"] >= 1900) & (df["yearmanu"] <= 2030)
    df["decade"] = np.where(
        valid_year,
        (df["yearmanu"].astype(int) // 10 * 10).astype(str) + "s",
        "Unknown"
    )
    decade_counts = df["decade"].value_counts()
    print(f"  Created 'decade' from yearmanu: {len(decade_counts)} unique decades")
    for d, cnt in decade_counts.head(8).items():
        print(f"    {d}: {cnt:,}")

# 4b. Manufacturer frequency encoding
if "manu" in df.columns:
    manu_freq = df["manu"].value_counts()
    df["manu_freq"] = df["manu"].map(manu_freq)
    print(f"  Created 'manu_freq' (manufacturer frequency encoding)")
    print(f"    Top manufacturer: '{manu_freq.index[0]}' with {manu_freq.iloc[0]:,} aircraft")

# 4c. Airframe type (simple binary: aeroplane vs rotorcraft vs other)
if "airframe" in df.columns:
    df["is_aeroplane"] = df["airframe"].str.contains("aeroplane", case=False, na=False).astype(int)
    df["is_rotorcraft"] = df["airframe"].str.contains("rotorcraft", case=False, na=False).astype(int)
    print(f"  Created 'is_aeroplane' ({df['is_aeroplane'].sum():,} True)")
    print(f"  Created 'is_rotorcraft' ({df['is_rotorcraft'].sum():,} True)")

# 4d. Engine type -> broad category
if "engtype" in df.columns:
    def broad_engine(et):
        if pd.isna(et) or et == "Unknown":
            return "Unknown"
        et_l = et.lower()
        if any(w in et_l for w in ["piston"]):
            return "Piston"
        elif any(w in et_l for w in ["turboshaft", "turboprop", "turbofan", "turbojet", "turbine"]):
            return "Turbine"
        elif any(w in et_l for w in ["electric"]):
            return "Electric"
        elif any(w in et_l for w in ["diesel"]):
            return "Diesel"
        elif "not applicable" in et_l:
            return "Not Applicable"
        else:
            return "Other"
    df["engine_category"] = df["engtype"].apply(broad_engine)
    print(f"  Created 'engine_category' — value counts:")
    for cat, cnt in df["engine_category"].value_counts().items():
        print(f"    {cat}: {cnt:,}")

# 4e. Aircraft age at time of dataset (use 2025 as reference year)
if "yearmanu" in df.columns:
    valid_year = df["yearmanu"].notna() & (df["yearmanu"] >= 1900) & (df["yearmanu"] <= 2030)
    df["aircraft_age"] = np.where(valid_year, 2025 - df["yearmanu"], np.nan)
    df["aircraft_age"] = df["aircraft_age"].fillna(df["aircraft_age"].median())
    print(f"  Created 'aircraft_age' (median: {df['aircraft_age'].median():.0f} years)")

# 4f. Registration type -> binary: full registration
if "regtype" in df.columns:
    df["is_full_registration"] = (df["regtype"].str.lower() == "full registration").astype(int)
    print(f"  Created 'is_full_registration' ({df['is_full_registration'].sum():,} True)")

# ---------------------------------------------------------------------------
# 5. SAVE PROCESSED DATASET
# ---------------------------------------------------------------------------
print("\n[5/6] Saving processed dataset ...")

processed_path = os.path.join(PROCESSED_DIR, "aircraft_register_processed.csv")
df.to_csv(processed_path, index=False)
print(f"  Saved: {processed_path}")
print(f"  Shape: {df.shape}")
print(f"  Size: {os.path.getsize(processed_path) / 1024 / 1024:.1f} MB")

# Also save a parquet version if pyarrow is available
try:
    import pyarrow
    parquet_path = os.path.join(PROCESSED_DIR, "aircraft_register_processed.parquet")
    df.to_parquet(parquet_path, index=False)
    print(f"  Saved: {parquet_path}")
    print(f"  Size: {os.path.getsize(parquet_path) / 1024 / 1024:.1f} MB")
except ImportError:
    print("  (pyarrow not available, skipping parquet export)")

# ---------------------------------------------------------------------------
# 6. CREATE ML FEATURES (NUMERIC ONLY, SCALED)
# ---------------------------------------------------------------------------
print("\n[6/6] Creating ML features with StandardScaler ...")

# Select numeric feature columns
feature_cols = [
    "mtow", "engnum", "yearmanu", "manu_freq", "aircraft_age",
    "is_aeroplane", "is_rotorcraft", "is_full_registration"
]
# Keep only columns that exist
feature_cols = [c for c in feature_cols if c in df.columns]
print(f"  Feature columns ({len(feature_cols)}): {feature_cols}")

# Drop any remaining NaN rows for features
features_df = df[feature_cols].copy()
features_df = features_df.dropna()

# Standardise
scaler = StandardScaler()
scaled = scaler.fit_transform(features_df)
scaled_df = pd.DataFrame(scaled, columns=feature_cols)
scaled_df["mark"] = df.loc[features_df.index, "mark"].values

# Save features
features_path = os.path.join(FEATURES_DIR, "aircraft_register_features.csv")
scaled_df.to_csv(features_path, index=False)
print(f"  Saved: {features_path}")
print(f"  Shape: {scaled_df.shape}")

# Save the scaler parameters
scaler_info = {
    "feature_columns": feature_cols,
    "means": scaler.mean_.tolist(),
    "scales": scaler.scale_.tolist(),
    "n_samples": len(scaled_df)
}
scaler_path = os.path.join(FEATURES_DIR, "scaler_params.json")
with open(scaler_path, "w") as f:
    json.dump(scaler_info, f, indent=2)
print(f"  Saved: {scaler_path}")

# Quick stats on the scaled features
print(f"\n  Scaled feature statistics:")
print(f"    Mean ~ {scaled_df[feature_cols].mean().abs().max():.4f} (should be near 0)")
print(f"    Std  ~ {scaled_df[feature_cols].std().max():.4f} (should be near 1)")

print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
