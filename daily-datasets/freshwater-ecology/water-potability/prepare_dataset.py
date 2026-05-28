#!/usr/bin/env python3
"""
Water Potability Dataset — Pipeline

Source: Kaggle (water_potability.csv)
Goal: Binary classification — is water potable (drinkable) based on chemical properties?
"""

import numpy as np
import pandas as pd
import gc
import pickle
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"
PROCESSED.mkdir(exist_ok=True)
FEATURES.mkdir(exist_ok=True)

TARGET_COL = "potability"

# ─── 1. Load ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("WATER POTABILITY — Preprocessing Pipeline")
print("=" * 60)

print("\n[1/6] Loading raw data...")
df = pd.read_csv(RAW / "water_potability.csv")
print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Standardise column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
print(f"  Columns: {list(df.columns)}")

# ─── 2. EDA ──────────────────────────────────────────────────────────────────
print("\n[2/6] Exploratory Data Analysis...")

# Class distribution
class_counts = df[TARGET_COL].value_counts().sort_index()
for k, v in class_counts.items():
    pct = v / len(df) * 100
    label = "Potable" if k == 1 else "Not Potable"
    print(f"  {label}: {v:>4,} ({pct:.1f}%)")

print(f"\n  Missing values:")
for col, count in df.isnull().sum()[df.isnull().sum() > 0].items():
    print(f"    {col}: {count} ({count/len(df)*100:.1f}%)")

print(f"\n  Duplicate rows: {df.duplicated().sum()}")

feature_cols = [c for c in df.columns if c != TARGET_COL]
print(f"\n  Feature stats (all continuous):")
print(df[feature_cols].describe().round(2).to_string())

# ─── 3. Clean ────────────────────────────────────────────────────────────────
print("\n[3/6] Cleaning...")

# Impute missing values with median (skewed distributions for water chem)
before = df.isnull().sum().sum()
for col in df.columns:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"  {col}: filled {df[col].isnull().sum()} NaN with median ({median_val:.4f})")

print(f"  Missing values after imputation: {df.isnull().sum().sum()}")

# Outlier capping (IQR × 3 — wider bounds since water chem has legitimate extremes)
for col in feature_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR
    upper = Q3 + 3 * IQR
    n_cap = ((df[col] < lower) | (df[col] > upper)).sum()
    if n_cap > 0:
        df[col] = df[col].clip(lower, upper)
        print(f"  {col}: capped {n_cap} outliers at [{lower:.2f}, {upper:.2f}]")

# ─── 4. Feature Engineering ─────────────────────────────────────────────────
print("\n[4/6] Feature Engineering...")

# Salinity index: conductivity × solids (high TDS water)
df["salinity_index"] = df["conductivity"] * df["solids"] / 1e6

# Organic load: organic_carbon × trihalomethanes (TOC byproduct indicator)
df["organic_load"] = df["organic_carbon"] * df["trihalomethanes"]

# Hardness-to-conductivity ratio (mineral composition indicator)
df["hardness_conductivity_ratio"] = df["hardness"] / (df["conductivity"] + 1e-8)

# pH category bins
pH_bins = [0, 5.5, 6.5, 7.5, 8.5, 14]
pH_labels = ["acidic", "slightly_acidic", "neutral", "slightly_alkaline", "alkaline"]
df["ph_category"] = pd.cut(df["ph"], bins=pH_bins, labels=pH_labels)
dummies = pd.get_dummies(df["ph_category"], prefix="ph")
for c in dummies.columns:
    df[c] = dummies[c].astype(int)

new_features = ["salinity_index", "organic_load", "hardness_conductivity_ratio"] + list(dummies.columns)
print(f"  Added {len(new_features)} engineered features: {new_features}")

# Update feature list
feature_cols = [c for c in df.columns if c != TARGET_COL]

# ─── 5. Save Cleaned ────────────────────────────────────────────────────────
print("\n[5/6] Saving cleaned dataset...")
clean_path = PROCESSED / "water_potability_clean.csv"
df.to_csv(clean_path, index=False)
print(f"  Saved: {clean_path}  ({df.shape[0]:,} rows × {df.shape[1]} columns)")

# ─── 6. ML Prep ──────────────────────────────────────────────────────────────
print("\n[6/6] Preparing ML-ready files...")

X = df[feature_cols]
y = df[TARGET_COL].astype(int)

# Bool columns to int (from one-hot dummies)
bool_cols = X.select_dtypes(include=['bool']).columns
for c in bool_cols:
    X[c] = X[c].astype(int)

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

del df, X, y
gc.collect()

print(f"  Train: {X_train.shape[0]:,} × {X_train.shape[1]}")
print(f"  Test:  {X_test.shape[0]:,} × {X_test.shape[1]}")
print(f"  Train class dist: {np.bincount(y_train)}")
print(f"  Test  class dist: {np.bincount(y_test)}")

# Scale — filter to numeric only
X_train_num = X_train.select_dtypes(include=[np.number])
X_test_num = X_test.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_num)
del X_train, X_train_num
gc.collect()
X_test_scaled = scaler.transform(X_test_num)
del X_test_num
gc.collect()

np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
del X_train_scaled
gc.collect()
np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
del X_test_scaled
gc.collect()

y_train.to_csv(FEATURES / "y_train.csv", index=False, header=False)
y_test.to_csv(FEATURES / "y_test.csv", index=False, header=False)

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"  Saved: ML-ready files to features/")

# ─── Quick Validation ────────────────────────────────────────────────────────
print("\n  Training baseline model (Random Forest)...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(pd.read_csv(FEATURES / "X_train_scaled.csv", header=None).values,
        pd.read_csv(FEATURES / "y_train.csv", header=None).values.ravel())
y_pred = clf.predict(pd.read_csv(FEATURES / "X_test_scaled.csv", header=None).values)
y_true = pd.read_csv(FEATURES / "y_test.csv", header=None).values.ravel()
acc = accuracy_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)
print(f"  Baseline RF accuracy: {acc:.4f}")
print(f"  Confusion matrix:\n{cm}")

print("\n" + "=" * 60)
print("Pipeline complete.")
print("=" * 60)
