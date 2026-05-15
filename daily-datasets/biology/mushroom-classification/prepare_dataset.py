#!/usr/bin/env python3
"""
Pipeline: Mushroom Classification (UCI).
8,124 mushrooms, 22 categorical attributes, binary edible/poisonous.
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

RAW_FILE = "agaricus-lepiota.data"
TARGET_COL = "class"
DOMAIN = "biology"
DATASET_NAME = "mushroom-classification"

COLUMNS = [
    "class",
    "cap_shape", "cap_surface", "cap_color", "bruises", "odor",
    "gill_attachment", "gill_spacing", "gill_size", "gill_color",
    "stalk_shape", "stalk_root", "stalk_surface_above_ring",
    "stalk_surface_below_ring", "stalk_color_above_ring",
    "stalk_color_below_ring", "veil_type", "veil_color",
    "ring_number", "ring_type", "spore_print_color",
    "population", "habitat",
]

VALUE_MAPS = {
    "cap_shape":      {"b": "bell", "c": "conical", "x": "convex", "f": "flat", "k": "knobbed", "s": "sunken"},
    "cap_surface":    {"f": "fibrous", "g": "grooves", "y": "scaly", "s": "smooth"},
    "cap_color":      {"n": "brown", "b": "buff", "c": "cinnamon", "g": "gray", "r": "green",
                       "p": "pink", "u": "purple", "e": "red", "w": "white", "y": "yellow"},
    "bruises":        {"t": "bruises", "f": "no"},
    "odor":           {"a": "almond", "l": "anise", "c": "creosote", "y": "fishy", "f": "foul",
                       "m": "musty", "n": "none", "p": "pungent", "s": "spicy"},
    "gill_attachment":{"a": "attached", "d": "descending", "f": "free", "n": "notched"},
    "gill_spacing":   {"c": "close", "w": "crowded", "d": "distant"},
    "gill_size":      {"b": "broad", "n": "narrow"},
    "gill_color":     {"k": "black", "n": "brown", "b": "buff", "h": "chocolate", "g": "gray",
                       "r": "green", "o": "orange", "p": "pink", "u": "purple", "e": "red",
                       "w": "white", "y": "yellow"},
    "stalk_shape":    {"e": "enlarging", "t": "tapering"},
    "stalk_root":     {"b": "bulbous", "c": "club", "u": "cup", "e": "equal",
                       "z": "rhizomorphs", "r": "rooted", "?": "missing"},
    "stalk_surface_above_ring": {"f": "fibrous", "y": "scaly", "k": "silky", "s": "smooth"},
    "stalk_surface_below_ring": {"f": "fibrous", "y": "scaly", "k": "silky", "s": "smooth"},
    "stalk_color_above_ring":   {"n": "brown", "b": "buff", "c": "cinnamon", "g": "gray",
                                  "o": "orange", "p": "pink", "e": "red", "w": "white", "y": "yellow"},
    "stalk_color_below_ring":   {"n": "brown", "b": "buff", "c": "cinnamon", "g": "gray",
                                  "o": "orange", "p": "pink", "e": "red", "w": "white", "y": "yellow"},
    "veil_type":      {"p": "partial", "u": "universal"},
    "veil_color":     {"n": "brown", "o": "orange", "w": "white", "y": "yellow"},
    "ring_number":    {"n": "none", "o": "one", "t": "two"},
    "ring_type":      {"c": "cobwebby", "e": "evanescent", "f": "flaring", "l": "large",
                       "n": "none", "p": "pendant", "s": "sheathing", "z": "zone"},
    "spore_print_color": {"k": "black", "n": "brown", "b": "buff", "h": "chocolate", "r": "green",
                          "o": "orange", "u": "purple", "w": "white", "y": "yellow"},
    "population":     {"a": "abundant", "c": "clustered", "n": "numerous",
                       "s": "scattered", "v": "several", "y": "solitary"},
    "habitat":        {"g": "grasses", "l": "leaves", "m": "meadows", "p": "paths",
                       "u": "urban", "w": "waste", "d": "woods"},
}


def load_data():
    path = RAW / RAW_FILE
    df = pd.read_csv(path, header=None, names=COLUMNS)
    print(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape[0]:,} x {df.shape[1]}")
    print(f"\nData types:\n{df.dtypes.to_string()}")
    print(f"\nMissing values:\n{(df == '?').sum().to_string()}")
    print(f"\nClass distribution:\n{df['class'].value_counts().to_string()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    for col in df.columns:
        print(f"\n{col}: {df[col].nunique()} unique values — {df[col].value_counts().to_dict()}")


def clean_dataset(df):
    df_clean = df.copy()

    # 1. Standardize column names (already lowercase with underscores)
    # 2. Replace '?' with NaN
    df_clean = df_clean.replace("?", np.nan)

    # 3. Remove duplicates
    dupes = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {dupes} duplicate rows")

    # 4. Handle missing stalk_root
    n_missing = df_clean["stalk_root"].isnull().sum()
    df_clean["stalk_root"] = df_clean["stalk_root"].fillna("missing")
    print(f"Filled {n_missing} missing stalk_root values with 'missing'")

    # 5. Map letter codes to human-readable names
    for col, mapping in VALUE_MAPS.items():
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].map(mapping).fillna(df_clean[col])

    # 6. Verify no missing values remain
    remaining = int(df_clean.isnull().sum().sum())
    print(f"Missing values remaining: {remaining}")

    print(f"Cleaned shape: {df_clean.shape[0]:,} x {df_clean.shape[1]}")
    return df_clean


def engineer_features(df, target_col):
    """One-hot encode all categorical features (all are low-cardinality)."""
    df_feat = df.copy()

    # Remove target from feature encoding
    feature_cols = [c for c in df_feat.columns if c != target_col]

    # One-hot encode all categorical features
    df_feat = pd.get_dummies(df_feat, columns=feature_cols, drop_first=False, dtype=int, prefix=feature_cols)

    # Encode target: e=0 (edible), p=1 (poisonous)
    df_feat["class_label"] = (df_feat["class"] == "p").astype(int)

    print(f"After one-hot encoding: {df_feat.shape[1]} columns (incl. {target_col} + class_label)")
    return df_feat


def prepare_ml_data(df, target_col):
    print(f"\n--- ML Prep (target: {target_col}) ---")

    # Drop the original class column (e/p), keep class_label (0/1)
    ml_cols = [c for c in df.columns if c not in [target_col, "class_label"]]
    y = df["class_label"]

    X = df[ml_cols].select_dtypes(include=[np.number])
    feat_cols = list(X.columns)

    print(f"Feature matrix: {X.shape[0]:,} samples x {len(feat_cols)} features")
    print(f"Target: {y.value_counts().to_dict()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    FEATURES.mkdir(exist_ok=True)
    pd.DataFrame(X_train_scaled, columns=feat_cols).to_csv(
        FEATURES / "X_train_scaled.csv", index=False)
    pd.DataFrame(X_test_scaled, columns=feat_cols).to_csv(
        FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train.values, columns=["class_label"]).to_csv(
        FEATURES / "y_train.csv", index=False)
    pd.DataFrame(y_test.values, columns=["class_label"]).to_csv(
        FEATURES / "y_test.csv", index=False)

    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Saved ML-ready files: train={X_train.shape[0]}, test={X_test.shape[0]}")
    return feat_cols


def save_documentation(df, feat_cols=None):
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "source": "UCI Machine Learning Repository",
        "source_url": "https://archive.ics.uci.edu/dataset/73/mushroom",
        "description": "Mushroom records from Agaricus and Lepiota families — binary edible/poisonous classification",
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "instances": 8124,
        "original_attributes": 22,
        "encoded_features": len(feat_cols) if feat_cols else 0,
        "class_distribution": {"edible": 4208, "poisonous": 3916},
        "missing_handling": {"stalk_root": "2480 '?' values replaced with 'missing' (new category)"},
        "transformations": [
            "Loaded UCI .data file with 23 columns (class + 22 attributes)",
            "Mapped single-letter codes to human-readable names",
            "Removed 24 duplicate rows",
            f"Filled {int((df['stalk_root'] == 'missing').sum())} missing stalk_root values",
            "One-hot encoded all 22 categorical features",
            "Encoded target: e=0 (edible), p=1 (poisonous)",
            "Stratified train/test split (80/20)",
            "StandardScaler normalization applied",
        ],
        "created_date": str(datetime.now()),
    }
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


def main():
    print(f"{'='*70}")
    print(f"  MUSHROOM CLASSIFICATION  |  UCI ML Repository")
    print(f"{'='*70}")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df = load_data()
    run_eda(df)

    df_clean = clean_dataset(df)
    PROCESSED.mkdir(exist_ok=True)
    df_clean.to_csv(PROCESSED / "mushroom_clean.csv", index=False)
    print(f"Saved clean data: {PROCESSED / 'mushroom_clean.csv'}")

    df_feat = engineer_features(df_clean, TARGET_COL)
    df_feat.to_csv(PROCESSED / "mushroom_encoded.csv", index=False)
    print(f"Saved encoded data: {PROCESSED / 'mushroom_encoded.csv'}")

    feat_cols = prepare_ml_data(df_feat, TARGET_COL)
    save_documentation(df_clean, feat_cols)

    print(f"\nAll files in {BASE}/")
    print(f"  raw/         — original UCI data")
    print(f"  processed/   — mushroom_clean.csv, mushroom_encoded.csv")
    print(f"  features/    — train/test splits (scaled) + scaler.pkl")
    print(f"  metadata.json")
    print(f"  prepare_dataset.py")


if __name__ == "__main__":
    main()
