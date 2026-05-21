#!/usr/bin/env python3
"""
Cervical Cancer Risk Factors — UCI dataset pipeline.
858 patients, 33 risk factors + 3 diagnosis tests + 1 biopsy target.
Target: Biopsy (0=negative, 1=positive cervical cancer).
"""
import pandas as pd
import numpy as np
import json
import pickle
import warnings
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

DATASET_NAME = "cervical_cancer_risk"
TARGET_COL = "Biopsy"

# Columns that are numeric but stored as object with '?'
NUMERIC_OBJECT_COLS = [
    "Number of sexual partners", "First sexual intercourse",
    "Num of pregnancies", "Smokes", "Smokes (years)", "Smokes (packs/year)",
    "Hormonal Contraceptives", "Hormonal Contraceptives (years)",
    "IUD", "IUD (years)", "STDs", "STDs (number)",
    "STDs:condylomatosis", "STDs:cervical condylomatosis",
    "STDs:vaginal condylomatosis", "STDs:vulvo-perineal condylomatosis",
    "STDs:syphilis", "STDs:pelvic inflammatory disease",
    "STDs:genital herpes", "STDs:molluscum contagiosum",
    "STDs:AIDS", "STDs:HIV", "STDs:Hepatitis B", "STDs:HPV",
    "STDs: Time since first diagnosis", "STDs: Time since last diagnosis",
]

# Binary columns that should be 0/1
BINARY_COLS = [
    "Smokes", "Hormonal Contraceptives", "IUD", "STDs",
    "STDs:condylomatosis", "STDs:cervical condylomatosis",
    "STDs:vaginal condylomatosis", "STDs:vulvo-perineal condylomatosis",
    "STDs:syphilis", "STDs:pelvic inflammatory disease",
    "STDs:genital herpes", "STDs:molluscum contagiosum",
    "STDs:AIDS", "STDs:HIV", "STDs:Hepatitis B", "STDs:HPV",
    "Dx:Cancer", "Dx:CIN", "Dx:HPV", "Dx",
]

TARGET_NAMES = {0: "Negative", 1: "Positive"}


def main():
    for d in [PROCESSED, FEATURES]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Loading data ===")
    df = pd.read_csv(RAW / "risk_factors_cervical_cancer.csv")
    print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} cols")

    # ── EDA ──
    print("\n=== EDA ===")
    print(f"Missing values (? encoded): {df.isin(['?']).sum().sum()}")

    # Convert '?' to NaN and cast numeric object columns
    for col in NUMERIC_OBJECT_COLS:
        df[col] = df[col].replace("?", np.nan)
    for col in NUMERIC_OBJECT_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Confirm no string '?' remains
    remaining_q = df.isin(["?"]).sum().sum()
    print(f"Remaining '?': {remaining_q}")

    # Target distribution
    target_dist = df[TARGET_COL].value_counts().sort_index()
    print(f"\nTarget ({TARGET_COL}):")
    for k, v in target_dist.items():
        name = TARGET_NAMES.get(k, k)
        print(f"  {k} ({name}): {v} ({v/len(df)*100:.1f}%)")

    # ── Clean ──
    print("\n=== Cleaning ===")

    # Check duplicates
    dups = df.duplicated().sum()
    print(f"Duplicates: {dups}")
    df = df.drop_duplicates()
    if dups:
        print(f"After dedup: {len(df)} rows")

    # Handle missing values
    missing_counts = df.isnull().sum()
    missing_cols = missing_counts[missing_counts > 0]
    if len(missing_cols) > 0:
        print(f"\nMissing value count per column:")
        for col, cnt in missing_cols.items():
            print(f"  {col:45s}: {cnt:>3} ({cnt/len(df)*100:.1f}%)")

    # Fill numeric: median for continuous, 0 for binary
    continuous_cols = [
        "Age", "Number of sexual partners", "First sexual intercourse",
        "Num of pregnancies", "Smokes (years)", "Smokes (packs/year)",
        "Hormonal Contraceptives (years)", "IUD (years)",
        "STDs (number)",
        "STDs: Time since first diagnosis", "STDs: Time since last diagnosis",
    ]
    for col in continuous_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  Filled {col} with median ({median_val})")

    for col in BINARY_COLS:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(0).astype(int)
            print(f"  Filled {col} with 0")

    print(f"\nRemaining missing: {df.isnull().sum().sum()}")

    # ── Feature Engineering ──
    print("\n=== Feature Engineering ===")

    # Age groups
    df["age_group"] = pd.cut(df["Age"], bins=[0, 25, 35, 45, 100], labels=[0, 1, 2, 3]).astype(int)

    # Sexual health composite
    df["sexual_activity_score"] = (
        df["Number of sexual partners"].fillna(0) *
        df["Num of pregnancies"].fillna(0)
    ).clip(0, 100)

    # Smoking severity
    df["smoking_years_per_age"] = df["Smokes (years)"] / (df["Age"] + 1)
    df["heavy_smoker"] = (df["Smokes (packs/year)"] >= 20).astype(int)

    # Hormonal exposure duration
    df["hormonal_years_per_age"] = df["Hormonal Contraceptives (years)"] / (df["Age"] + 1)

    # Total STD count (sum of individual STD indicators)
    std_cols = [c for c in BINARY_COLS if c.startswith("STDs:") and c != "STDs (number)" and c not in [
        "STDs: Time since first diagnosis", "STDs: Time since last diagnosis"
    ]]
    df["std_count"] = df[std_cols].sum(axis=1)

    # Any prior diagnosis
    df["prior_diagnosis"] = ((df["Dx:Cancer"] == 1) | (df["Dx:CIN"] == 1) | (df["Dx:HPV"] == 1) | (df["Dx"] == 1)).astype(int)

    # Screening test flag (any positive test)
    test_cols = ["Hinselmann", "Schiller", "Citology"]
    df["positive_screening"] = ((df["Hinselmann"] == 1) | (df["Schiller"] == 1) | (df["Citology"] == 1)).astype(int)

    new_features = [
        "age_group", "sexual_activity_score", "smoking_years_per_age",
        "heavy_smoker", "hormonal_years_per_age", "std_count",
        "prior_diagnosis", "positive_screening",
    ]
    print(f"Added {len(new_features)} derived features")

    # ── Save cleaned ──
    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nSaved: {clean_path}")

    # ── ML Prep ──
    print("\n=== ML Preparation ===")

    # Feature columns (exclude targets and screening tests that leak the target)
    exclude_from_features = [TARGET_COL, "Hinselmann", "Schiller", "Citology",
                             "Dx:Cancer", "Dx:CIN", "Dx:HPV", "Dx"]
    feature_cols = [c for c in df.columns if c not in exclude_from_features]

    X = df[feature_cols]
    y = df[TARGET_COL]

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"Features: {X_train_scaled.shape[1]}")

    # Save ML files
    pd.DataFrame(X_train_scaled).to_csv(FEATURES / "X_train_scaled.csv", index=False, header=False)
    pd.DataFrame(X_test_scaled).to_csv(FEATURES / "X_test_scaled.csv", index=False, header=False)
    pd.Series(y_train.values).to_csv(FEATURES / "y_train.csv", index=False, header=False)
    pd.Series(y_test.values).to_csv(FEATURES / "y_test.csv", index=False, header=False)

    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"\n=== Done ===")
    print(f"Rows: {len(df)}")
    print(f"Features: {len(feature_cols)}")
    print(f"Target: {TARGET_COL}")
    print(f"Class distribution (train):")
    y_train_dist = pd.Series(y_train).value_counts().sort_index()
    for k, v in y_train_dist.items():
        name = TARGET_NAMES.get(k, k)
        print(f"  {k} ({name}): {v} ({v/len(y_train)*100:.1f}%)")
    print(f"Class distribution (test):")
    y_test_dist = pd.Series(y_test).value_counts().sort_index()
    for k, v in y_test_dist.items():
        name = TARGET_NAMES.get(k, k)
        print(f"  {k} ({name}): {v} ({v/len(y_test)*100:.1f}%)")


if __name__ == "__main__":
    main()
