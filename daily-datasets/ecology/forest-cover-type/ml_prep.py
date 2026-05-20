#!/usr/bin/env python3
"""ML prep for Forest Cover Type — loads clean CSV, splits, scales, saves.
Memory-conscious: frees intermediates immediately after use."""
import gc
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

BASE = Path(__file__).parent
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"
FEATURES.mkdir(exist_ok=True)

COVER_TYPE_NAMES = {
    1: "Spruce/Fir", 2: "Lodgepole Pine", 3: "Ponderosa Pine",
    4: "Cottonwood/Willow", 5: "Aspen", 6: "Douglas-fir", 7: "Krummholz",
}

quant_cols = [
    "elevation", "aspect", "slope",
    "horizontal_distance_to_hydrology", "vertical_distance_to_hydrology",
    "horizontal_distance_to_roadways",
    "hillshade_9am", "hillshade_noon", "hillshade_3pm",
    "horizontal_distance_to_fire_points",
]

print("=== Loading cleaned data ===")
df = pd.read_csv(PROCESSED / "forest_cover_type_clean.csv")
print(f"{len(df):,} rows, {len(df.columns)} cols")

binary_cols = [c for c in df.columns if c.startswith("wilderness") or c.startswith("soil")]
new_features = [
    "elevation_slope", "horiz_vert_hydrology_ratio",
    "avg_hillshade", "hillshade_range", "total_hydrology_distance",
    "near_water", "near_road", "near_fire",
    "northness", "eastness",
    "wilderness_count", "soil_count",
]
feature_cols = quant_cols + binary_cols + new_features
print(f"Feature count: {len(feature_cols)}")

target_col = "cover_type"

# Encode target
le = LabelEncoder()
y_enc = le.fit_transform(df[target_col])
print(f"Classes: {len(le.classes_)} {[COVER_TYPE_NAMES.get(i, i) for i in le.classes_]}")

# Split (stratified for class balance)
print("=== Train/test split ===")
X_train, X_test, y_train, y_test = train_test_split(
    df[feature_cols], y_enc, test_size=0.2, random_state=42, stratify=y_enc,
)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# Free the big dataframe
del df, y_enc
gc.collect()

# Scale
print("=== Scaling ===")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
print(f"X_train_scaled: {X_train_scaled.shape}")
del X_train
gc.collect()

X_test_scaled = scaler.transform(X_test)
print(f"X_test_scaled: {X_test_scaled.shape}")
del X_test
gc.collect()

# Save ML files
print("=== Saving ===")
np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
print("X_train_scaled.csv saved")
del X_train_scaled
gc.collect()

np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
print("X_test_scaled.csv saved")
del X_test_scaled
gc.collect()

np.savetxt(FEATURES / "y_train.csv", y_train, delimiter=",", fmt="%d")
np.savetxt(FEATURES / "y_test.csv", y_test, delimiter=",", fmt="%d")
print("y_train.csv, y_test.csv saved")

with open(FEATURES / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open(FEATURES / "label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)
print("scaler.pkl, label_encoder.pkl saved")

# Summary
train_dist = pd.Series(y_train).value_counts().sort_index()
print(f"\n=== Done ===")
print(f"Rows: {len(y_train) + len(y_test):,}")
print(f"Features: {len(feature_cols)}")
print(f"Train class distribution:")
for k, v in train_dist.items():
    name = COVER_TYPE_NAMES.get(k, k)
    print(f"  {k} ({str(name):20s}): {v:>6,} ({v/len(y_train)*100:5.1f}%)")
