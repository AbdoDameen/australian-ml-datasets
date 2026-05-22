#!/usr/bin/env python3
"""
Protein Sequence (Bioinfo) — protein classification from physicochemical features.
60K protein sequences, 7 sequence-derived features, 5 structural/functional classes.
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

DATASET_NAME = "protein_sequence_bioinfo"
TARGET_COL = "protein_class"

# Column translations and groupings
COLUMN_RENAMES = {
    "ID_Proteína": "protein_id",
    "Sequência": "sequence",
    "Massa_Molecular": "molecular_mass",
    "Ponto_Isoelétrico": "isoelectric_point",
    "Hidrofobicidade": "hydrophobicity",
    "Carga_Total": "total_charge",
    "Proporção_Polar": "polar_ratio",
    "Proporção_Apolar": "apolar_ratio",
    "Comprimento_Sequência": "sequence_length",
    "Classe": "protein_class",
}

CLASS_TRANSLATIONS = {
    "Receptora": "Receptor",
    "Enzima": "Enzyme",
    "Estrutural": "Structural",
    "Sinalizacao": "Signaling",
    "Transporte": "Transport",
}

# Features (exclude ID and sequence text)
FEATURE_COLS = [
    "molecular_mass", "isoelectric_point", "hydrophobicity",
    "total_charge", "polar_ratio", "apolar_ratio", "sequence_length",
]


def main():
    for d in [PROCESSED, FEATURES]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Loading data ===")
    df = pd.read_csv(RAW / "proteinas_20000_enriquecido.csv")
    print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} cols")

    # Rename columns to English
    df = df.rename(columns=COLUMN_RENAMES)

    # ── EDA ──
    print("\n=== EDA ===")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicates: {df.duplicated().sum():,}")

    # Target distribution
    df["protein_class"] = df["protein_class"].map(CLASS_TRANSLATIONS).fillna(df["protein_class"])
    target_dist = df[TARGET_COL].value_counts()
    print(f"\nTarget (protein_class) — {len(target_dist)} classes:")
    for cls, cnt in target_dist.items():
        print(f"  {cls:20s}: {cnt:>6,} ({cnt/len(df)*100:5.1f}%)")

    print(f"\nFeature stats:")
    print(df[FEATURE_COLS].describe().to_string())

    # ── Clean ──
    print("\n=== Cleaning ===")
    df = df.drop_duplicates()
    print(f"After dedup: {len(df):,} rows")

    # No missing values from EDA above

    # Outlier cap for extreme values (IQR method, capped not removed)
    for col in FEATURE_COLS:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            df[col] = df[col].clip(lower, upper)
            print(f"  Capped {col}: {outliers} outliers ({outliers/len(df)*100:.1f}%)")

    # ── Feature Engineering ──
    print("\n=== Feature Engineering ===")

    # Charge density (charge per residue)
    df["charge_density"] = df["total_charge"] / (df["sequence_length"] + 1)

    # Hydrophobicity-polarity interaction
    df["hydrophobicity_polar_interaction"] = df["hydrophobicity"] * df["polar_ratio"]

    # Polar-apolar ratio
    df["polar_apolar_ratio"] = df["polar_ratio"] / (df["apolar_ratio"] + 0.001)

    # Mass per residue
    df["mass_per_residue"] = df["molecular_mass"] / (df["sequence_length"] + 1)

    new_features = [
        "charge_density", "hydrophobicity_polar_interaction",
        "polar_apolar_ratio", "mass_per_residue",
    ]
    print(f"Added {len(new_features)} derived features")

    # ── Save cleaned ──
    # Keep all columns for reference but save
    df.to_csv(PROCESSED / f"{DATASET_NAME}_clean.csv", index=False)
    print(f"\nSaved cleaned: {PROCESSED / f'{DATASET_NAME}_clean.csv'}")

    # ── ML Prep ──
    print("\n=== ML Preparation ===")

    all_features = FEATURE_COLS + new_features
    X = df[all_features]
    y = df[TARGET_COL]

    # Encode target
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    print(f"Encoded classes: {list(le.classes_)}")

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

    # Scale
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

    # Summary
    print(f"\n=== Done ===")
    print(f"Rows: {len(df):,}")
    print(f"Features: {len(all_features)}")
    print(f"Classes: {len(le.classes_)} — {list(le.classes_)}")
    y_train_dist = pd.Series(y_train).value_counts().sort_index()
    print(f"Train class distribution:")
    for k, v in y_train_dist.items():
        cls_name = le.classes_[k]
        print(f"  {cls_name:20s}: {v:>6,} ({v/len(y_train)*100:5.1f}%)")


if __name__ == "__main__":
    main()
