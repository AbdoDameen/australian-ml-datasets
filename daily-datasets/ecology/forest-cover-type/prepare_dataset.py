#!/usr/bin/env python3
"""
Forest Cover Type — UCI dataset pipeline.
10 quantitative features + 4 wilderness binary + 40 soil binary = 54 features.
Target: forest cover type (7 classes).
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

DATASET_NAME = "forest_cover_type"
TARGET_COL = "cover_type"

COLUMNS = [
    "elevation", "aspect", "slope",
    "horizontal_distance_to_hydrology", "vertical_distance_to_hydrology",
    "horizontal_distance_to_roadways",
    "hillshade_9am", "hillshade_noon", "hillshade_3pm",
    "horizontal_distance_to_fire_points",
] + [f"wilderness_area_{i}" for i in range(1, 5)] + \
    [f"soil_type_{i}" for i in range(1, 41)] + \
    ["cover_type"]

COVER_TYPE_NAMES = {
    1: "Spruce/Fir", 2: "Lodgepole Pine", 3: "Ponderosa Pine",
    4: "Cottonwood/Willow", 5: "Aspen", 6: "Douglas-fir", 7: "Krummholz"
}


def main():
    for d in [PROCESSED, FEATURES]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Loading data ===")
    data_path = RAW / "covtype.data"
    df = pd.read_csv(data_path, header=None, names=COLUMNS)
    print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} cols")

    # ── EDA ──
    print(f"\n=== EDA ===")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicates: {df.duplicated().sum():,}")
    
    target_dist = df[TARGET_COL].value_counts().sort_index()
    print(f"\nTarget distribution:")
    for k, v in target_dist.items():
        name = COVER_TYPE_NAMES.get(k, f"Type {k}")
        print(f"  {k} ({name:20s}): {v:>6,} ({v/len(df)*100:5.1f}%)")

    # ── Clean ──
    print(f"\n=== Cleaning ===")
    df = df.drop_duplicates()
    print(f"After dedup: {len(df):,} rows")

    # No missing values (confirmed above)

    # ── Feature engineering ──
    print(f"\n=== Feature Engineering ===")

    # Quantitative features
    quant_cols = [
        "elevation", "aspect", "slope",
        "horizontal_distance_to_hydrology", "vertical_distance_to_hydrology",
        "horizontal_distance_to_roadways",
        "hillshade_9am", "hillshade_noon", "hillshade_3pm",
        "horizontal_distance_to_fire_points",
    ]

    binary_cols = [c for c in COLUMNS if c.startswith("wilderness") or c.startswith("soil")]

    # Derived features
    df["elevation_slope"] = df["elevation"] * df["slope"]
    df["horiz_vert_hydrology_ratio"] = np.clip(
        df["horizontal_distance_to_hydrology"] / (df["vertical_distance_to_hydrology"].abs() + 1),
        0, 1000)
    df["avg_hillshade"] = (df["hillshade_9am"] + df["hillshade_noon"] + df["hillshade_3pm"]) / 3
    df["hillshade_range"] = df[["hillshade_9am", "hillshade_noon", "hillshade_3pm"]].max(axis=1) - \
        df[["hillshade_9am", "hillshade_noon", "hillshade_3pm"]].min(axis=1)
    df["total_hydrology_distance"] = df["horizontal_distance_to_hydrology"] + df["vertical_distance_to_hydrology"]
    df["near_water"] = ((df["horizontal_distance_to_hydrology"] < 100) | 
                        (df["vertical_distance_to_hydrology"] < 20)).astype(int)
    df["near_road"] = (df["horizontal_distance_to_roadways"] < 100).astype(int)
    df["near_fire"] = (df["horizontal_distance_to_fire_points"] < 500).astype(int)
    df["northness"] = np.cos(np.radians(df["aspect"]))
    df["eastness"] = np.sin(np.radians(df["aspect"]))

    # Total wilderness and soil types present
    df["wilderness_count"] = df[[c for c in binary_cols if "wilderness" in c]].sum(axis=1)
    df["soil_count"] = df[[c for c in binary_cols if "soil" in c]].sum(axis=1)

    new_features = [
        "elevation_slope", "horiz_vert_hydrology_ratio",
        "avg_hillshade", "hillshade_range", "total_hydrology_distance",
        "near_water", "near_road", "near_fire",
        "northness", "eastness",
        "wilderness_count", "soil_count",
    ]
    print(f"Added {len(new_features)} derived features")

    # ── Save cleaned ──
    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nSaved: {clean_path}")

    # ── ML prep ──
    print(f"\n=== ML Preparation ===")
    feature_cols = quant_cols + binary_cols + new_features
    target_col = TARGET_COL

    X = df[feature_cols]
    y = df[target_col]

    # Encode target
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"Features: {X_train_scaled.shape[1]}")

    # Save ML files
    pd.DataFrame(X_train_scaled).to_csv(FEATURES / "X_train_scaled.csv", index=False, header=False)
    pd.DataFrame(X_test_scaled).to_csv(FEATURES / "X_test_scaled.csv", index=False, header=False)
    pd.Series(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=False)
    pd.Series(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=False)

    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    with open(FEATURES / "label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    print(f"\n=== Done ===")
    print(f"Rows: {len(df):,}")
    print(f"Features: {len(feature_cols)}")
    print(f"Classes: {len(le.classes_)}")
    print(f"Class names: {[COVER_TYPE_NAMES.get(i, i) for i in le.classes_]}")


if __name__ == "__main__":
    main()
