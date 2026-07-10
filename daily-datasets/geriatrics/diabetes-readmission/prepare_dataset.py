#!/usr/bin/env python3
"""
Diabetes Readmission — data preparation pipeline.
Predict 30-day hospital readmission from clinical and demographic features.
Source: UCI ML Repository (Diabetes 130-US Hospitals, 1999-2008)
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

# ─── CONFIG ─────────────────────────────────────────────────────────────────
RAW_FILE = "diabetic_data.csv"
HEADER_ROW = 0
SKIP_ROWS = 0
TARGET_COL = "readmitted"
DOMAIN = "geriatrics"
DATASET_NAME = "diabetes-readmission"
# ────────────────────────────────────────────────────────────────────────────

# Columns to drop (identifiers, high-missingness, low-value)
DROP_COLS = [
    "encounter_id", "patient_nbr",      # IDs
    "weight", "payer_code",             # >50% missing / low predictive value
    "examide", "citoglipton",           # all zeros (drugs never prescribed)
]


def load_data():
    csv_path = RAW / RAW_FILE
    print(f"Loading {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8", na_values="?",
                     dtype={"diag_1": str, "diag_2": str, "diag_3": str})
    print(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def run_eda(df):
    print(f"\n--- EDA ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nMissing:\n{df.isnull().sum().to_string()}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nNumeric Stats:\n{df[numeric_cols].describe().to_string()}")
    cat_cols = df.select_dtypes(include=["object"]).columns
    print(f"\nCategorical value counts:")
    for c in cat_cols:
        vc = df[c].value_counts()
        print(f"  {c}: {vc.to_dict()}")
    print(f"\nTarget distribution:\n{df[TARGET_COL].value_counts(normalize=True).to_string()}")


def clean_dataset(df):
    df = df.copy()
    print(f"\n--- Cleaning ---")

    # Drop identifier columns
    cols_to_drop = [c for c in DROP_COLS if c in df.columns]
    df.drop(columns=cols_to_drop, inplace=True)
    print(f"Dropped: {cols_to_drop}")

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {before - len(df)} duplicates")

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    print(f"Standardized column names")

    # Handle missing values
    # race: ~2% missing — fill with mode
    if "race" in df.columns:
        race_mode = df["race"].mode().iloc[0] if not df["race"].mode().empty else "Unknown"
        df["race"] = df["race"].fillna(race_mode)
        print(f"Filled race missing with '{race_mode}'")

    # diag_1/2/3: missing — fill with 'Unknown'
    for c in ["diag_1", "diag_2", "diag_3"]:
        if c in df.columns:
            df[c] = df[c].fillna("Unknown")
            print(f"Filled {c} missing with 'Unknown'")

    # max_glu_serum, a1cresult: 'None' means not measured — keep as category
    # medication columns: 'No' means not prescribed — keep as category

    # Encode '?' in admission_type/discharge/admission_source
    # These are stored as ints but some have 0/NaN — map properly
    for c in ["admission_type_id", "discharge_disposition_id", "admission_source_id"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    # Replace 'No' / 'Up' / 'Down' / 'Steady' / 'Ch' in medication columns
    med_cols = [c for c in df.columns if c in [
        "metformin", "repaglinide", "nateglinide", "chlorpropamide",
        "glimepiride", "acetohexamide", "glipizide", "glyburide",
        "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose",
        "miglitol", "troglitazone", "tolazamide", "insulin",
        "glyburide-metformin", "glipizide-metformin",
        "glimepiride-pioglitazone", "metformin-rosiglitazone",
        "metformin-pioglitazone"
    ]]
    for c in med_cols:
        print(f"  {c}: {df[c].value_counts().to_dict()}")

    print(f"\nMissing after cleaning:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string() if df.isnull().sum().sum() > 0 else 'None'}")
    return df


def engineer_features(df):
    df = df.copy()
    print(f"\n--- Feature Engineering ---")

    # 1. Encode age as midpoint numeric
    age_map = {
        "[0-10)": 5, "[10-20)": 15, "[20-30)": 25, "[30-40)": 35,
        "[40-50)": 45, "[50-60)": 55, "[60-70)": 65, "[70-80)": 75,
        "[80-90)": 85, "[90-100)": 95
    }
    df["age_mid"] = df["age"].map(age_map)
    df.drop(columns=["age"], inplace=True)
    print("Encoded age → age_mid (numeric midpoint)")

    # 2. Encode gender as binary
    df["is_female"] = (df["gender"] == "Female").astype(int)
    df.drop(columns=["gender"], inplace=True)
    print("Encoded gender → is_female (binary)")

    # 3. One-hot encode race (low cardinality)
    race_dummies = pd.get_dummies(df["race"], prefix="race")
    dummies = ["race_Caucasian", "race_AfricanAmerican", "race_Hispanic",
               "race_Asian", "race_Other"]
    for d in dummies:
        if d not in race_dummies.columns:
            race_dummies[d] = 0
    race_dummies = race_dummies[dummies].astype(int)
    df = pd.concat([df, race_dummies], axis=1)
    df.drop(columns=["race"], inplace=True)
    print("One-hot encoded race → 5 columns")

    # 4. Admission type mapping (one-hot)
    adm_type_map = {
        1: "Emergency", 2: "Urgent", 3: "Elective",
        4: "Newborn", 5: "Not Available", 6: "NULL",
        7: "Trauma Center", 8: "Not Mapped"
    }
    df["admission_type"] = df["admission_type_id"].map(adm_type_map).fillna("Other")
    adm_dummies = pd.get_dummies(df["admission_type"], prefix="adm_type")
    adm_dummies = adm_dummies.astype(int)
    df = pd.concat([df, adm_dummies], axis=1)
    df.drop(columns=["admission_type_id", "admission_type"], inplace=True)
    print("One-hot encoded admission_type_id → 8 columns")

    # 5. A1C result: encode as ordered categories
    a1c_map = {"None": 0, "Norm": 1, ">7": 2, ">8": 3}
    df["a1c_level"] = df["a1cresult"].map(a1c_map).fillna(0).astype(int)
    df.drop(columns=["a1cresult"], inplace=True)
    print("Encoded a1cresult → a1c_level (0-3)")

    # 6. Max glucose serum: encode as ordered
    glu_map = {"None": 0, "Norm": 1, ">200": 2, ">300": 3}
    df["glucose_level"] = df["max_glu_serum"].map(glu_map).fillna(0).astype(int)
    df.drop(columns=["max_glu_serum"], inplace=True)
    print("Encoded max_glu_serum → glucose_level (0-3)")

    # 7. Medication change: encode as binary
    df["med_change"] = (df["change"] == "Ch").astype(int)
    df.drop(columns=["change"], inplace=True)
    print("Encoded change → med_change (binary)")

    # 8. Diabetes medication flag
    df["diabetes_med"] = (df["diabetesmed"] == "Yes").astype(int)
    df.drop(columns=["diabetesmed"], inplace=True)
    print("Encoded diabetesmed → diabetes_med (binary)")

    # 9. Medication columns: encode Steady/Up/Down/No/Ch as ordinal
    med_ord_map = {"No": 0, "Down": 1, "Steady": 2, "Up": 3}
    med_cols = [c for c in df.columns if c in [
        "metformin", "repaglinide", "nateglinide", "chlorpropamide",
        "glimepiride", "acetohexamide", "glipizide", "glyburide",
        "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose",
        "miglitol", "troglitazone", "tolazamide", "insulin",
        "glyburide-metformin", "glipizide-metformin",
        "glimepiride-pioglitazone", "metformin-rosiglitazone",
        "metformin-pioglitazone"
    ]]
    for c in med_cols:
        df[c] = df[c].map(med_ord_map).fillna(0).astype(int)
    print(f"Encoded {len(med_cols)} medication columns as ordinal (0-3)")

    # 10. Medical specialty: collapse rare specialties (frequency < 100) into "Other"
    if "medical_specialty" in df.columns:
        specialty_counts = df["medical_specialty"].value_counts()
        rare_specialties = specialty_counts[specialty_counts < 100].index
        df["medical_specialty"] = df["medical_specialty"].fillna("Unknown")
        df.loc[df["medical_specialty"].isin(rare_specialties), "medical_specialty"] = "Other"
        spec_dummies = pd.get_dummies(df["medical_specialty"], prefix="spec")
        # Keep top 20 specialties + Unknown/Other
        spec_cols = [c for c in spec_dummies.columns
                     if c in ["spec_InternalMedicine", "spec_Emergency/Trauma",
                              "spec_Family/GeneralPractice", "spec_Cardiology",
                              "spec_Surgery-General", "spec_Orthopedics",
                              "spec_Nephrology", "spec_Pulmonology",
                              "spec_Unknown", "spec_Other"]]
        for d in spec_cols:
            if d not in spec_dummies.columns:
                spec_dummies[d] = 0
        spec_dummies = spec_dummies[spec_cols].astype(int)
        df = pd.concat([df, spec_dummies], axis=1)
        df.drop(columns=["medical_specialty"], inplace=True)
        print(f"One-hot encoded medical_specialty → {len(spec_cols)} columns")

    return df


def prepare_ml(df):
    print(f"\n--- ML Preparation ---")

    # Target: binary classification — readmitted within 30 days vs not
    df["readmit_30d"] = (df[TARGET_COL] == "<30").astype(int)
    df.drop(columns=[TARGET_COL], inplace=True)
    print(f"Binary target: readmit_30d ({df['readmit_30d'].mean():.3%} positive rate)")

    # Select numeric columns for ML
    ml_cols = [c for c in df.columns if c != "readmit_30d"]
    ml_df = df[ml_cols].select_dtypes(include=[np.number])

    # Drop any remaining non-numeric
    X = ml_df.values
    y = df["readmit_30d"].values

    print(f"ML shape: X={X.shape}, y={y.shape}")

    # Train/test split (stratified for class imbalance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save
    PROCESSED.mkdir(parents=True, exist_ok=True)
    FEATURES.mkdir(parents=True, exist_ok=True)

    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"Saved cleaned data: {clean_path}")

    np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
    np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
    np.savetxt(FEATURES / "y_train.csv", y_train, delimiter=",", fmt="%d")
    np.savetxt(FEATURES / "y_test.csv", y_test, delimiter=",", fmt="%d")
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("Saved ML-ready files to features/")

    # Feature names
    return ml_cols


def generate_metadata(df, orig_rows, ml_cols):
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "source": "UCI Machine Learning Repository",
        "source_url": "https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008",
        "license": "CC BY 4.0",
        "created_date": str(datetime.now()),
        "original_rows": int(orig_rows),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "ml_columns": int(len(ml_cols)),
        "column_list": list(df.columns),
        "target_column": "readmit_30d",
        "ml_task": "Binary classification (predict 30-day hospital readmission)",
        "missing_values_remaining": int(df.isnull().sum().sum()),
        "description": (
            "Clinical records from 130 US hospitals (1999-2008) spanning ~100K inpatient "
            "encounters for patients with diabetes. Target is whether the patient was "
            "readmitted within 30 days of discharge. Features include demographics, "
            "admission type, diagnoses, lab results, medication changes, and prior visits."
        ),
        "transformations": [
            "Dropped IDs (encounter_id, patient_nbr)",
            "Dropped high-missing columns (weight, payer_code, examide, citoglipton)",
            "Removed duplicate rows",
            "Encoded age bins as numeric midpoint (age_mid)",
            "Encoded gender as binary (is_female)",
            "One-hot encoded race into 5 indicator columns",
            "One-hot encoded admission type into 8 indicator columns",
            "Encoded A1C result as ordered level (0-3)",
            "Encoded max glucose serum as ordered level (0-3)",
            "Encoded medication columns as ordinal (0=No, 1=Down, 2=Steady, 3=Up)",
            "One-hot encoded top medical specialties (13 categories + Other/Unknown)",
            "Filled missing diagnoses with 'Unknown'",
            "Filled missing race with mode",
            "Binary target: readmitted <30 days = 1, else 0",
            "Train/test split 80/20 stratified by target",
            "StandardScaler normalization on all features"
        ]
    }
    meta_path = BASE / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata: {meta_path}")


def main():
    df = load_data()
    run_eda(df)
    df_clean = clean_dataset(df)
    df_feat = engineer_features(df_clean)
    ml_cols = prepare_ml(df_feat)
    generate_metadata(df_feat, len(df), ml_cols)
    print(f"\n✓ Done — {DATASET_NAME} is clean and ML-ready")


if __name__ == "__main__":
    main()
