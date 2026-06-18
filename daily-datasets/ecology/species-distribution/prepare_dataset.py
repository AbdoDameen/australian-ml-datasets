#!/usr/bin/env python3
"""
Species Distribution (GBIF) — ML Pipeline
===========================================
Target: taxonomic 'class' (multi-class classification)
Predict taxonomic class from spatial/temporal/environmental features.

Reads:  species_sample.csv
Outputs:
  processed/cleaned.csv           — cleaned feature-engineered data (pre-split)
  processed/class_distribution.png|json
  features/X_train.npy, X_test.npy
  features/y_train.npy, y_test.npy
  features/scaler.pkl
  features/label_encoder.pkl
  features/feature_columns.json
"""

import os
import json
import warnings
import sys
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
RAW_CSV = BASE_DIR / "species_sample.csv"
PROCESSED_DIR = BASE_DIR / "processed"
FEATURES_DIR = BASE_DIR / "features"
METADATA_PATH = BASE_DIR / "metadata.json"

for d in [PROCESSED_DIR, FEATURES_DIR]:
    d.mkdir(exist_ok=True)

print("=" * 60)
print("Species Distribution (GBIF) — ML Pipeline")
print("=" * 60)

# ── 1. Load ────────────────────────────────────────────────────────────
print("\n[1/6] Loading data...")
df = pd.read_csv(RAW_CSV, low_memory=False)
print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# ── 2. EDA ─────────────────────────────────────────────────────────────
print("\n[2/6] EDA...")

# Target distribution
target_col = "class"
print(f"\n  Class distribution (top 20):")
vc = df[target_col].value_counts()
print(vc.head(20).to_string())
print(f"  Total unique classes: {len(vc)}")

# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
miss_df = pd.DataFrame({"missing": missing, "pct": missing_pct}).sort_values("missing", ascending=False)
miss_df = miss_df[miss_df["missing"] > 0]
print(f"\n  Columns with missing values ({len(miss_df)} total):")
print(miss_df.head(30).to_string())

# Unique counts per column
unique_counts = df.nunique().sort_values(ascending=False)
print(f"\n  Unique counts per column (top 20):")
print(unique_counts.head(20).to_string())

# Save class distribution as JSON for metadata
class_dist = vc.to_dict()
with open(PROCESSED_DIR / "class_distribution.json", "w") as f:
    json.dump(class_dist, f, indent=2)
print(f"\n  Class distribution saved to processed/class_distribution.json")

# ── 3. Clean ───────────────────────────────────────────────────────────
print("\n[3/6] Cleaning...")

# Columns to drop (IDs, UUIDs, high-cardinality text, non-predictive)
cols_to_drop = [
    "gbifID", "datasetKey", "occurrenceID",
    "publishingOrgKey", "taxonKey", "speciesKey",
    "institutionCode", "collectionCode", "catalogNumber",
    "recordNumber", "identifiedBy", "dateIdentified",
    "rightsHolder", "recordedBy", "lastInterpreted",
    "scientificName", "verbatimScientificName",
    "verbatimScientificNameAuthorship", "infraspecificEpithet",
    "taxonRank", "locality", "issue", "mediaType",
    "license", "typeStatus", "establishmentMeans",
    "eventDate", "depth", "depthAccuracy", "coordinatePrecision",
    # Also drop spatial accuracy / occurrence metadata not used as features
    "stateProvince", "occurrenceStatus", "order", "family",
    "genus", "species", "coordinateUncertaintyInMeters",
    "elevationAccuracy",
]

existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
df.drop(columns=existing_cols_to_drop, inplace=True)
print(f"  Dropped {len(existing_cols_to_drop)} columns")
print(f"  Remaining columns ({len(df.columns)}): {list(df.columns)}")

# ── 4. Handle missing values ───────────────────────────────────────────
print("\n[4/6] Handling missing values...")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

# Remove target from imputation lists
if target_col in numeric_cols:
    numeric_cols.remove(target_col)
if target_col in categorical_cols:
    categorical_cols.remove(target_col)

print(f"  Numeric columns to impute: {numeric_cols}")
print(f"  Categorical columns to impute: {categorical_cols}")

# Impute numeric with median (fallback to 0 if entire column is NaN)
for col in numeric_cols:
    if col in df.columns and df[col].isnull().any():
        med = df[col].median()
        if pd.isna(med):
            med = 0.0
            print(f"    {col}: entire column NaN, filling with 0")
        df[col].fillna(med, inplace=True)
        print(f"    {col}: imputed {df[col].isnull().sum()} missing with median={med}")

# Impute categorical with mode
for col in categorical_cols:
    if col in df.columns and df[col].isnull().any():
        mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else "UNKNOWN"
        df[col].fillna(mode_val, inplace=True)
        print(f"    {col}: imputed {df[col].isnull().sum()} missing with mode='{mode_val}'")

print(f"  Remaining missing values: {df.isnull().sum().sum()}")

# ── 5. Feature engineering ─────────────────────────────────────────────
print("\n[5/6] Feature engineering...")

# Target: taxonomic class
y_raw = df[target_col].copy()

# One-hot encode categorical features
cat_feats = ["kingdom", "phylum", "countryCode", "basisOfRecord"]
existing_cat_feats = [c for c in cat_feats if c in df.columns]
print(f"  One-hot encoding: {existing_cat_feats}")

df_encoded = pd.get_dummies(df[existing_cat_feats], prefix=existing_cat_feats, drop_first=False)
print(f"  Generated {df_encoded.shape[1]} dummy columns")

# Numeric features
num_feats = ["decimalLatitude", "decimalLongitude", "year", "month", "day", "elevation", "individualCount"]
existing_num_feats = [c for c in num_feats if c in df.columns]
print(f"  Numeric features: {existing_num_feats}")

X_numeric = df[existing_num_feats].copy()

# Combine features
X = pd.concat([X_numeric.reset_index(drop=True), df_encoded.reset_index(drop=True)], axis=1)
y = y_raw.reset_index(drop=True)

print(f"  Feature matrix shape: {X.shape}")
print(f"  Target shape: {y.shape}")

# Save feature column names
feature_columns = list(X.columns)
with open(FEATURES_DIR / "feature_columns.json", "w") as f:
    json.dump(feature_columns, f, indent=2)
print(f"  Feature columns saved to features/feature_columns.json")

# ── 6. Collapse rare classes ───────────────────────────────────────────
print("\n[5b/6] Collapsing rare classes...")

vc_y = y.value_counts()
rare_classes = vc_y[vc_y < 100].index.tolist()
print(f"  Classes with < 100 occurrences: {len(rare_classes)}")
print(f"  Total rows affected: {y.isin(rare_classes).sum()}")

y = y.copy()
y[y.isin(rare_classes)] = "OTHER"

vc_after = y.value_counts()
print(f"  Unique classes after collapse: {len(vc_after)}")
print(vc_after.head(20).to_string())

# ── 7. ML Prep — Train/Test Split, Scale, Encode ──────────────────────
print("\n[6/6] ML preparation...")

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  Train: {X_train.shape[0]} samples")
print(f"  Test:  {X_test.shape[0]} samples")
print(f"  Train class distribution:")
print(y_train.value_counts().head(10).to_string())

# Scale numeric features only
scaler = StandardScaler()
num_idx = list(range(len(existing_num_feats)))
X_train_num_scaled = scaler.fit_transform(X_train.iloc[:, num_idx])
X_test_num_scaled = scaler.transform(X_test.iloc[:, num_idx])

# Combine scaled numeric with unchanged one-hot columns
if num_idx:
    X_train_arr = np.concatenate(
        [X_train_num_scaled, X_train.iloc[:, len(existing_num_feats):].values], axis=1
    )
    X_test_arr = np.concatenate(
        [X_test_num_scaled, X_test.iloc[:, len(existing_num_feats):].values], axis=1
    )
else:
    X_train_arr = X_train.values
    X_test_arr = X_test.values

# Label encode target
label_encoder = LabelEncoder()
y_train_enc = label_encoder.fit_transform(y_train)
y_test_enc = label_encoder.transform(y_test)

print(f"  Number of classes: {len(label_encoder.classes_)}")
print(f"  Classes: {list(label_encoder.classes_)}")

# Save all outputs
np.save(FEATURES_DIR / "X_train.npy", X_train_arr)
np.save(FEATURES_DIR / "X_test.npy", X_test_arr)
np.save(FEATURES_DIR / "y_train.npy", y_train_enc)
np.save(FEATURES_DIR / "y_test.npy", y_test_enc)

with open(FEATURES_DIR / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open(FEATURES_DIR / "label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Save cleaned pre-split dataset
df_clean = X.copy()
df_clean[target_col] = y
df_clean.to_csv(PROCESSED_DIR / "cleaned.csv", index=False)

# Save train/test dataframes for inspection
train_df = pd.DataFrame(X_train_arr, columns=feature_columns)
train_df[target_col] = y_train_enc
train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)

test_df = pd.DataFrame(X_test_arr, columns=feature_columns)
test_df[target_col] = y_test_enc
test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)

print("\n  Saved outputs:")
print(f"    processed/cleaned.csv        — cleaned data ({df_clean.shape[0]} rows)")
print(f"    processed/train.csv          — train split ({X_train.shape[0]} rows)")
print(f"    processed/test.csv           — test split ({X_test.shape[0]} rows)")
print(f"    processed/class_distribution.json")
print(f"    features/X_train.npy         — shape {X_train_arr.shape}")
print(f"    features/X_test.npy          — shape {X_test_arr.shape}")
print(f"    features/y_train.npy         — shape {y_train_enc.shape}")
print(f"    features/y_test.npy          — shape {y_test_enc.shape}")
print(f"    features/scaler.pkl")
print(f"    features/label_encoder.pkl")
print(f"    features/feature_columns.json")

# ── 8. Update metadata.json ────────────────────────────────────────────
print("\n[Final] Updating metadata.json...")

updated_metadata = {
    "dataset_id": 16,
    "name": "Species Distribution (GBIF)",
    "folder": "ecology/species-distribution",
    "domain": "Ecology",
    "ml_task": "Multi-class Classification",
    "source": "GBIF",
    "description": "199K species occurrence records (sampled from 4.5M+ records)",
    "status": "✅ PIPELINE READY",
    "has_raw_data": True,
    "has_pipeline": True,
    "target": "class (taxonomic class)",
    "num_classes": len(label_encoder.classes_),
    "num_features": X_train_arr.shape[1],
    "train_samples": int(X_train.shape[0]),
    "test_samples": int(X_test.shape[0]),
    "numeric_features": existing_num_feats,
    "categorical_features": existing_cat_feats,
    "rare_classes_collapsed_into_OTHER": len(rare_classes),
    "class_distribution_top10": {
        str(k): int(v) for k, v in vc_after.head(10).items()
    },
}

with open(METADATA_PATH, "w") as f:
    json.dump(updated_metadata, f, indent=2)
print(f"  metadata.json updated")

print("\n" + "=" * 60)
print("✅ Pipeline complete!")
print("=" * 60)
print(f"\nNext step: Run `rm 0011324-260519110011954.csv` to free disk space.")
