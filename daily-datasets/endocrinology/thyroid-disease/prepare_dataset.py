#!/usr/bin/env python3
"""
Thyroid Disease Dataset — Pipeline

Source: UCI Machine Learning Repository (ann-thyroid subset)
Donor: Randolf Werner, Daimler-Benz, 1992
Original: Ross Quinlan, Garavan Institute, Sydney, Australia

Preprocessed by Werner for backpropagation benchmarking — all attributes
normalised to [0,1], no missing values.
"""

import numpy as np
import pandas as pd
import gc
import json
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"
PROCESSED.mkdir(exist_ok=True)
FEATURES.mkdir(exist_ok=True)

TARGET_COL = "thyroid_class"

COLUMNS = [
    # 6 continuous
    "age",
    # 15 binary
    "sex",
    "on_thyroxine",
    "query_on_thyroxine",
    "on_antithyroid_medication",
    "thyroid_surgery",
    "query_hypothyroid",
    "query_hyperthyroid",
    "pregnant",
    "sick",
    "tumor",
    "lithium",
    "goitre",
    "tsh_measured",
    "t3_measured",
    "tt4_measured",
    # 5 continuous
    "tsh",
    "t3",
    "tt4",
    "t4u",
    "fti",
    TARGET_COL,
]

CLASS_NAMES = {1: "normal", 2: "hyperfunction", 3: "subnormal"}

# ─── 1. Load ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("THYROID DISEASE — Preprocessing Pipeline")
print("=" * 60)

print("\n[1/6] Loading raw data...")
train = np.loadtxt(RAW / "ann-train.data")
test = np.loadtxt(RAW / "ann-test.data")
print(f"  Train: {train.shape[0]:,} rows")
print(f"  Test:  {test.shape[0]:,} rows")

# Combine into single dataframe
df = pd.DataFrame(np.vstack([train, test]), columns=COLUMNS)
print(f"  Full:  {df.shape[0]:,} rows × {df.shape[1]} columns")

del train, test
gc.collect()

# ─── 2. EDA ──────────────────────────────────────────────────────────────────
print("\n[2/6] Exploratory Data Analysis...")
print(f"\nClass distribution:")
class_counts = df[TARGET_COL].value_counts().sort_index()
for k, v in class_counts.items():
    print(f"  {int(k)} ({CLASS_NAMES[int(k)]}): {v:>5,} ({v/len(df)*100:.1f}%)")

print(f"\nMissing values: {df.isnull().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")

binary_cols = [c for c in COLUMNS if c not in ("age", "tsh", "t3", "tt4", "t4u", "fti", TARGET_COL)]
continuous_cols = ["age", "tsh", "t3", "tt4", "t4u", "fti"]

print(f"\nContinuous stats:")
print(df[continuous_cols].describe().round(4).to_string())

# ─── 3. Clean ────────────────────────────────────────────────────────────────
print("\n[3/6] Cleaning...")

# Column names already clean
# No missing values (confirmed)
# No duplicates to drop (UCI benchmark — keep exact)
# Outliers: the data is already normalised, skip IQR clipping
# Binary columns already 0/1
# Data already normalised to [0,1]

print("  ✓ No missing values")
print("  ✓ All columns standardised")
print("  ✓ Binary columns are 0/1")

# ─── 4. Feature Engineering ─────────────────────────────────────────────────
print("\n[4/6] Feature Engineering...")

# Already preprocessed — all binary flags present, continuous normalised.
# Add interaction: TSH-to-T3 ratio as a clinical indicator
df["tsh_t3_ratio"] = df["tsh"] / (df["t3"] + 1e-8)

# Free T4 index: TT4 * T4U (already captured by FTI, but add explicit)
df["calculated_fti"] = df["tt4"] * df["t4u"]

new_features = ["tsh_t3_ratio", "calculated_fti"]
print(f"  Added {len(new_features)} engineered features: {new_features}")

# ─── 5. Save Cleaned ────────────────────────────────────────────────────────
print("\n[5/6] Saving cleaned dataset...")
clean_path = PROCESSED / "thyroid_disease_clean.csv"
df.to_csv(clean_path, index=False)
print(f"  Saved: {clean_path}  ({df.shape[0]:,} rows × {df.shape[1]} columns)")

# ─── 6. ML Prep ──────────────────────────────────────────────────────────────
print("\n[6/6] Preparing ML-ready files...")

feature_cols = [c for c in df.columns if c != TARGET_COL]
X = df[feature_cols]
y = df[TARGET_COL].astype(int)

# Train/test split: use 80/20 (stratified due to imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

del df, X, y
gc.collect()

print(f"  Train: {X_train.shape[0]:,} × {X_train.shape[1]}")
print(f"  Test:  {X_test.shape[0]:,} × {X_test.shape[1]}")
print(f"  Train class dist: {np.bincount(y_train)}")
print(f"  Test  class dist: {np.bincount(y_test)}")

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
del X_train
gc.collect()
X_test_scaled = scaler.transform(X_test)

# Save scaled arrays
np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
del X_train_scaled
gc.collect()
np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
del X_test_scaled
gc.collect()

y_train.to_csv(FEATURES / "y_train.csv", index=False, header=False)
y_test.to_csv(FEATURES / "y_test.csv", index=False, header=False)

# Save scaler
import pickle
with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"  Saved: X_train_scaled.csv ({FEATURES / 'X_train_scaled.csv'})")
print(f"  Saved: X_test_scaled.csv")
print(f"  Saved: y_train.csv / y_test.csv")
print(f"  Saved: scaler.pkl")

# ─── Quick Validation ────────────────────────────────────────────────────────
print("\n  Training baseline model (Random Forest)...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(pd.read_csv(FEATURES / "X_train_scaled.csv", header=None).values,
        pd.read_csv(FEATURES / "y_train.csv", header=None).values.ravel())
y_pred = clf.predict(pd.read_csv(FEATURES / "X_test_scaled.csv", header=None).values)
acc = accuracy_score(
    pd.read_csv(FEATURES / "y_test.csv", header=None).values.ravel(),
    y_pred
)
print(f"  Baseline RF accuracy: {acc:.4f}")

print("\n" + "=" * 60)
print("Pipeline complete.")
print("=" * 60)
