#!/usr/bin/env python3
"""
Human Activity Recognition — UCI HAR Dataset pipeline.
Merges train/test splits, maps activity labels, prepares ML-ready files.
6 activity classes: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING
"""
import pandas as pd
import numpy as np
import json
import os
import pickle
import zipfile
import shutil
import warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"
EXTRACT_DIR = RAW / "_extracted"

DATASET_NAME = "human_activity_recognition"
DOMAIN = "biophysics"
TARGET_COL = "activity_name"


def extract_zip():
    """Extract UCI HAR Dataset.zip to a temp directory."""
    zip_path = RAW / "UCI HAR Dataset.zip"
    if EXTRACT_DIR.exists():
        shutil.rmtree(EXTRACT_DIR)
    print(f"Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(EXTRACT_DIR)
    # Find the UCI HAR Dataset directory (might be nested)
    data_dir = EXTRACT_DIR / "UCI HAR Dataset"
    if not data_dir.exists():
        # try the extraction dir itself
        for p in EXTRACT_DIR.iterdir():
            if p.is_dir() and "UCI" in p.name:
                data_dir = p
                break
    print(f"Extracted to {data_dir}")
    return data_dir


def load_features(data_dir):
    """Load 561 feature names from features.txt, deduplicating by appending _N."""
    feat_path = data_dir / "features.txt"
    features = []
    seen = {}
    with open(feat_path) as f:
        for line in f:
            # Format: "1 tBodyAcc-mean()-X"
            parts = line.strip().split()
            name = parts[1] if len(parts) >= 2 else parts[0]
            if name in seen:
                seen[name] += 1
                name = f"{name}_{seen[name]}"
            else:
                seen[name] = 0
            features.append(name)
    print(f"Loaded {len(features)} feature names ({len(seen)} unique)")
    return features


def load_activity_labels(data_dir):
    """Load activity ID → name mapping."""
    labels = {}
    with open(data_dir / "activity_labels.txt") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                labels[int(parts[0])] = parts[1]
    print(f"Activity labels: {labels}")
    return labels


def load_split(data_dir, split_name, features, activity_labels):
    """Load X_{split}.txt, y_{split}.txt, subject_{split}.txt and combine."""
    print(f"\nLoading {split_name} split...")

    X_path = data_dir / split_name / f"X_{split_name}.txt"
    y_path = data_dir / split_name / f"y_{split_name}.txt"
    subj_path = data_dir / split_name / f"subject_{split_name}.txt"

    X = pd.read_csv(X_path, sep=r'\s+', header=None, names=features)
    y = pd.read_csv(y_path, sep=r'\s+', header=None, names=['activity_id'])
    subjects = pd.read_csv(subj_path, sep=r'\s+', header=None, names=['subject_id'])

    df = pd.concat([subjects, X, y], axis=1)
    df['activity_name'] = df['activity_id'].map(activity_labels)
    df['split'] = split_name

    print(f"  {split_name}: {df.shape[0]} samples, {df.shape[1]} columns")
    return df


def run_eda(df):
    """Print EDA summary."""
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]:,} x {df.shape[1]}")
    print(f"Subjects: {df['subject_id'].nunique()}")
    print(f"\nActivity distribution:")
    print(df['activity_name'].value_counts().to_string())
    print(f"\nSplit distribution:")
    print(df['split'].value_counts().to_string())
    print(f"\nMissing values: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")


def clean_dataset(df):
    """Clean and standardize."""
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = (df_clean.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^a-z0-9_]", "_", regex=True)
                        .str.replace(r"_+", "_", regex=True)
                        .str.strip("_"))

    # Drop duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {dupes} duplicate rows")

    # No missing values expected in this dataset
    print(f"Cleaning complete: {df_clean.shape[0]:,} x {df_clean.shape[1]}")
    return df_clean


def prepare_ml_data(df, target_col):
    """ML prep: one-hot encode activity, split, scale."""
    print(f"\nPreparing ML data (target: {target_col})...")

    # Drop identifier columns not useful for ML
    ml_df = df.drop(columns=['subject_id', 'activity_id', 'split'], errors='ignore')

    # Encode target
    le = LabelEncoder()
    ml_df['activity_encoded'] = le.fit_transform(ml_df[target_col])
    activity_classes = list(le.classes_)

    # Drop the string target column, keep encoded version
    ml_df = ml_df.drop(columns=[target_col])

    # Convert bool to int
    for col in ml_df.columns:
        if ml_df[col].dtype == bool:
            ml_df[col] = ml_df[col].astype(int)

    # Features and target
    feat_cols = [c for c in ml_df.columns if c != 'activity_encoded']
    X = ml_df[feat_cols].select_dtypes(include=[np.number])
    y = ml_df['activity_encoded']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=feat_cols)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feat_cols)

    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target_col])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target_col])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Save label encoder for decoding predictions
    with open(FEATURES / "label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    print(f"Saved ML files to {FEATURES}/")
    print(f"  Train: {X_train_df.shape}, Test: {X_test_df.shape}")
    print(f"  Classes: {activity_classes}")
    return activity_classes


def save_documentation(df_shape, activity_classes):
    """Save metadata.json."""
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "source": "UCI Machine Learning Repository",
        "source_url": "https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones",
        "description": "Smartphone sensor (Samsung Galaxy S II) recordings of 30 subjects performing 6 activities. 561 time/frequency features from accelerometer and gyroscope.",
        "created_date": str(datetime.now()),
        "rows": int(df_shape[0]),
        "columns": int(df_shape[1]),
        "features": 561,
        "subjects": 30,
        "activities": activity_classes,
        "target": "activity_name (multi-class classification: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING)",
        "sensor_types": ["accelerometer (3-axis)", "gyroscope (3-axis)"],
        "sampling_rate": "50 Hz",
        "window_size": "2.56 sec (128 readings, 50% overlap)",
        "column_list": list(['subject_id', 'activity_id', 'activity_name', 'split'] + [f'feature_{i}' for i in range(561)]),
        "missing_values_remaining": 0
    }
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata.json")


def main():
    print(f"{'='*80}")
    print(f"  DATASET: Human Activity Recognition  |  DOMAIN: Biophysics")
    print(f"{'='*80}")

    PROCESSED.mkdir(parents=True, exist_ok=True)

    # Extract
    data_dir = extract_zip()

    # Load metadata
    features = load_features(data_dir)
    activity_labels = load_activity_labels(data_dir)

    # Load both splits and combine
    df_train = load_split(data_dir, "train", features, activity_labels)
    df_test = load_split(data_dir, "test", features, activity_labels)
    df = pd.concat([df_train, df_test], ignore_index=True)

    # EDA
    run_eda(df)

    # Clean
    df_clean = clean_dataset(df)

    # Save cleaned data
    clean_csv = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df_clean.to_csv(clean_csv, index=False)
    print(f"\nSaved cleaned data: {clean_csv}")

    # ML prep
    activity_classes = prepare_ml_data(df_clean, TARGET_COL)

    # Docs
    save_documentation(df_clean.shape, activity_classes)

    # Clean up temp extraction
    shutil.rmtree(EXTRACT_DIR)
    print(f"\nDone — all files in {BASE}")
    print(f"  Processed: {clean_csv}")
    print(f"  ML-ready: {FEATURES}/")


if __name__ == "__main__":
    main()
