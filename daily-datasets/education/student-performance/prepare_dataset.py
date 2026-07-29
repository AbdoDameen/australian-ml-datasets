#!/usr/bin/env python3
"""
Student Performance (UCI) — clean, combine, engineer features, ML-ready.
Two subjects: Math (395 students) and Portuguese (649 students).
Target: G3 (final grade, 0–20, regression).
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

DOMAIN = "education"
DATASET_NAME = "student-performance"

COL_DESCRIPTIONS = {
    "school": "student's school (GP - Gabriel Pereira or MS - Mousinho da Silveira)",
    "sex": "student's sex (F/M)",
    "age": "student's age (15–22)",
    "address": "student's home address type (U - urban or R - rural)",
    "famsize": "family size (LE3 - ≤3 or GT3 - >3)",
    "pstatus": "parent's cohabitation status (T - living together or A - apart)",
    "medu": "mother's education (0=none, 1=primary 4yr, 2=5th–9th, 3=secondary, 4=higher)",
    "fedu": "father's education (same scale)",
    "mjob": "mother's job (teacher, health, services, at_home, other)",
    "fjob": "father's job (same categories)",
    "reason": "reason to choose this school (home, reputation, course, other)",
    "guardian": "student's guardian (mother, father, other)",
    "traveltime": "home-to-school travel time (1=<15min, 2=15–30, 3=30–60, 4=>60min)",
    "studytime": "weekly study time (1=<2h, 2=2–5h, 3=5–10h, 4=>10h)",
    "failures": "number of past class failures (0–4)",
    "schoolsup": "extra educational support (yes/no)",
    "famsup": "family educational support (yes/no)",
    "paid": "extra paid classes within course subject (yes/no)",
    "activities": "extra-curricular activities (yes/no)",
    "nursery": "attended nursery school (yes/no)",
    "higher": "wants to take higher education (yes/no)",
    "internet": "Internet access at home (yes/no)",
    "romantic": "in a romantic relationship (yes/no)",
    "famrel": "quality of family relationships (1=very bad to 5=excellent)",
    "freetime": "free time after school (1=very low to 5=very high)",
    "goout": "going out with friends (1=very low to 5=very high)",
    "dalc": "workday alcohol consumption (1=very low to 5=very high)",
    "walc": "weekend alcohol consumption (1=very low to 5=very high)",
    "health": "current health status (1=very bad to 5=very good)",
    "absences": "number of school absences (0–93)",
    "g1": "first period grade (0–20)",
    "g2": "second period grade (0–20)",
    "g3": "final grade (0–20) — TARGET",
    "subject": "subject (Math or Portuguese)",
}


def load_data():
    """Load both subjects, add subject column, combine."""
    print(f"Loading student-mat.csv...")
    math = pd.read_csv(RAW / "student-mat.csv", sep=";")
    math["subject"] = "Math"

    print(f"Loading student-por.csv...")
    por = pd.read_csv(RAW / "student-por.csv", sep=";")
    por["subject"] = "Portuguese"

    df = pd.concat([math, por], ignore_index=True)
    print(f"Combined: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  Math: {len(math)}, Portuguese: {len(por)}")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]} x {df.shape[1]}")
    print(f"Subjects: {df['subject'].value_counts().to_dict()}")
    print(f"Target G3: min={df['G3'].min()}, max={df['G3'].max()}, mean={df['G3'].mean():.2f}, std={df['G3'].std():.2f}")
    print(f"Missing values total: {int(df.isnull().sum().sum())}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    return df


def clean_dataset(df):
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = (
        df_clean.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9_]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    # Drop duplicates
    dupes_before = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    dupes_removed = dupes_before - len(df_clean)
    print(f"Removed {dupes_removed} duplicate rows")

    # Already verified: no missing values in this dataset
    print("No missing values to fill")

    # Outlier capping on absences (has high range 0–93)
    for col in ["absences"]:
        Q1, Q3 = df_clean[col].quantile(0.25), df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_capped = int((df_clean[col] < lower).sum() + (df_clean[col] > upper).sum())
        if n_capped > 0:
            df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
            print(f"Capped {n_capped} outliers in '{col}'")

    print(f"Cleaning done — shape: {df_clean.shape}")
    return df_clean


def engineer_features(df):
    """Add derived features: grade changes, performance tiers, interaction terms."""
    df_f = df.copy()

    # Grade changes
    df_f["g1_to_g2_change"] = df_f["g2"] - df_f["g1"]
    df_f["g1_to_g3_change"] = df_f["g3"] - df_f["g1"]

    # Average of G1, G2, G3
    df_f["avg_grade"] = df_f[["g1", "g2", "g3"]].mean(axis=1)

    # Performance tiers based on past failures & current grades
    df_f["has_failed"] = (df_f["failures"] > 0).astype(int)
    df_f["high_absences"] = (df_f["absences"] > 10).astype(int)

    # Study-to-performance ratio (inverse — how much time per grade point)
    df_f["studytime_effort"] = df_f["studytime"] / (df_f["g3"] + 1)

    # Alcohol composite (workday + weekend)
    df_f["alcohol_score"] = df_f["dalc"] + df_f["walc"]

    # Low family support flag
    df_f["low_famrel"] = (df_f["famrel"] <= 2).astype(int)

    print(f"Engineered {df_f.shape[1] - df.shape[1]} new features")
    return df_f


def prepare_ml_data(df, target_col="g3"):
    """One-hot encode categoricals, split, scale, save."""
    print(f"\n--- ML Prep (target: {target_col}) ---")

    df_ml = df.copy()

    # Encode categoricals
    cat_cols = df_ml.select_dtypes(include=["object"]).columns.tolist()
    if "subject" in cat_cols:
        cat_cols.remove("subject")  # keep subject as a useful filter column

    for col in cat_cols:
        dummies = pd.get_dummies(df_ml[col], prefix=col)
        for c in dummies.columns:
            df_ml[c] = dummies[c].astype(int)
        df_ml = df_ml.drop(columns=[col])

    # Get numeric features, drop target
    numeric = df_ml.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in numeric:
        numeric.remove(target_col)

    X = df_ml[numeric].copy()
    y = df_ml[target_col]

    # Drop any remaining NaN rows
    nan_idx = X.isnull().any(axis=1)
    if nan_idx.any():
        X = X[~nan_idx]
        y = y[~nan_idx]
        print(f"Dropped {nan_idx.sum()} rows with NaNs")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=numeric)
    X_test_df = pd.DataFrame(X_test_scaled, columns=numeric)

    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])

    feat_names_path = FEATURES / "feature_names.json"
    with open(feat_names_path, "w") as f:
        json.dump({"features": numeric, "target": target_col}, f, indent=2)

    scaler_path = FEATURES / "scaler.pkl"
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    print(f"ML files saved to {FEATURES}/")
    print(f"  Train: {X_train_df.shape}, Test: {X_test_df.shape}")
    print(f"  Features: {len(numeric)}")

    return X_train_df, X_test_df, y_train, y_test, scaler


def save_metadata(df_clean, df_full, X_train=None, X_test=None, y_train=None, y_test=None):
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "created_date": str(datetime.now()),
        "source": "UCI Machine Learning Repository — Student Performance",
        "source_url": "https://archive.ics.uci.edu/dataset/320/student+performance",
        "license": "CC BY 4.0",
        "description": "Student performance in secondary education of two Portuguese schools. "
                       "Includes demographic, social/emotional, and academic features. "
                       "Target: G3 (final grade 0–20).",
        "data_shape": {
            "total_rows": int(df_clean.shape[0]),
            "total_columns": int(df_clean.shape[1]),
            "math_students": int((df_full[df_full["subject"] == "Math"]).shape[0]),
            "portuguese_students": int((df_full[df_full["subject"] == "Portuguese"]).shape[0]),
        },
        "target_variable": "g3",
        "ml_task": "regression",
        "feature_engineering": [
            "g1_to_g2_change — grade change from first to second period",
            "g1_to_g3_change — grade change from first to final period",
            "avg_grade — average of G1, G2, G3",
            "has_failed — binary: has at least one past class failure",
            "high_absences — binary: absences > 10",
            "studytime_effort — study time per grade point (inverse)",
            "alcohol_score — DALC + WALC (workday + weekend alcohol)",
            "low_famrel — binary: family relationship quality ≤ 2",
        ],
        "column_descriptions": COL_DESCRIPTIONS,
        "ml_data": {},
    }

    if X_train is not None:
        metadata["ml_data"] = {
            "train_samples": int(X_train.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "feature_count": int(X_train.shape[1]),
            "features": list(X_train.columns),
        }

    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


def main():
    print("=" * 80)
    print(f"  DATASET: {DATASET_NAME} ({DOMAIN})")
    print("=" * 80)

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df = load_data()
    run_eda(df)

    df_clean = clean_dataset(df)
    df_feat = engineer_features(df_clean)

    # Save cleaned + feature-engineered file
    PROCESSED.mkdir(exist_ok=True)
    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df_feat.to_csv(clean_path, index=False)
    print(f"\nSaved cleaned data: {clean_path}")

    # ML prep
    X_train, X_test, y_train, y_test, scaler = prepare_ml_data(df_feat, target_col="g3")

    # Metadata
    save_metadata(df_clean, df, X_train, X_test, y_train, y_test)

    print(f"\n{'=' * 80}")
    print(f"  Done — all files in {BASE}")
    print(f"  {PROCESSED / f'{DATASET_NAME}_clean.csv'}")
    print(f"  {FEATURES / 'X_train_scaled.csv'}")
    print(f"  {FEATURES / 'X_test_scaled.csv'}")
    print(f"  {FEATURES / 'y_train.csv'}")
    print(f"  {FEATURES / 'y_test.csv'}")
    print(f"  {FEATURES / 'scaler.pkl'}")
    print(f"  {FEATURES / 'feature_names.json'}")
    print(f"  {BASE / 'metadata.json'}")
    print(f"  {BASE / 'prepare_dataset.py'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
