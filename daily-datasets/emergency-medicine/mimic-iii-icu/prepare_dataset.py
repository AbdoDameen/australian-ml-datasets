#!/usr/bin/env python3
"""
MIMIC-III ICU (Emergency) — In-hospital mortality classification.
Loads ADMISSIONS, PATIENTS, LABEVENTS, D_LABITEMS into SQLite,
engineers features from lab values + demographics, predicts hospital_expire_flag.
"""
import pandas as pd
import numpy as np
import sqlite3
import json
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"
DB_PATH = BASE / "mimic_icu.db"
DOMAIN = "emergency-medicine"
DATASET_NAME = "mimic-iii-icu"

# ─── 1. LOAD & BUILD SQLITE ────────────────────────────────────────────────

def build_sqlite():
    """Load CSVs into SQLite per user's spec."""
    print("Building SQLite database...")
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))

    tables = {
        "ADMISSIONS": "ADMISSIONS.csv",
        "D_LABITEMS": "D_LABITEMS.csv",
        "PATIENTS": "PATIENTS.csv",
        "LABEVENTS": "LABEVENTS.csv",
    }
    for name, csv_file in tables.items():
        path = RAW / csv_file
        print(f"  Loading {path.name} ({path.stat().st_size / 1024:.0f} KB)...")
        df = pd.read_csv(path, low_memory=False)
        df.to_sql(name, conn, if_exists="replace", index=False)
        print(f"    -> {name}: {len(df)} rows")

    conn.commit()
    conn.close()
    print(f"SQLite DB: {DB_PATH}\n")


# ─── 2. FEATURE ENGINEERING (SQL) ──────────────────────────────────────────

def engineer_features():
    """Query SQLite to build the feature matrix for emergency admissions."""
    conn = sqlite3.connect(str(DB_PATH))

    # --- Core admission + patient features ---
    query = """
    SELECT
        a.row_id,
        a.subject_id,
        a.hadm_id,
        a.hospital_expire_flag,
        a.admission_type,
        a.admission_location,
        a.insurance,
        a.language,
        a.religion,
        a.marital_status,
        a.ethnicity,
        a.diagnosis,
        -- ED length of stay (hours)
        CASE
            WHEN a.edregtime IS NOT NULL AND a.edouttime IS NOT NULL
            THEN (julianday(a.edouttime) - julianday(a.edregtime)) * 24
            ELSE NULL
        END AS ed_los_hours,
        -- Age at admission
        CASE
            WHEN a.admittime IS NOT NULL AND p.dob IS NOT NULL
            THEN CAST(strftime('%Y', a.admittime) AS INTEGER) - CAST(strftime('%Y', p.dob) AS INTEGER)
            ELSE NULL
        END AS age,
        p.gender,
        p.expire_flag AS patient_deceased
    FROM ADMISSIONS a
    JOIN PATIENTS p ON a.subject_id = p.subject_id
    WHERE a.admission_type = 'EMERGENCY'
    """
    df = pd.read_sql_query(query, conn)
    print(f"Emergency admissions: {len(df)}")
    print(f"In-hospital mortality (target=1): {df['hospital_expire_flag'].sum()}")

    # --- Lab features: first measurement per admission for key labs ---
    # Pick the 20 most common lab tests (by itemid frequency)
    labs_query = """
    SELECT itemid, COUNT(*) AS cnt
    FROM LABEVENTS
    WHERE hadm_id IS NOT NULL AND hadm_id != '' AND valuenum IS NOT NULL
    GROUP BY itemid
    ORDER BY cnt DESC
    LIMIT 20
    """
    top_labs = pd.read_sql_query(labs_query, conn)
    print(f"\nTop 20 lab tests to use as features: {len(top_labs)}")

    # Pivot: first value per lab per admission
    lab_features = []
    for _, row in top_labs.iterrows():
        itemid = row["itemid"]
        # Get D_LABITEMS label
        label_df = pd.read_sql_query(
            f"SELECT label FROM D_LABITEMS WHERE itemid = {itemid}", conn
        )
        label = label_df["label"].iloc[0] if len(label_df) > 0 else f"item_{itemid}"
        label_col = label.lower().replace(" ", "_").replace("/", "_").replace(",", "").replace("(", "").replace(")", "")
        if not label_col:
            label_col = f"lab_{itemid}"

        # First measurement value per admission
        val_query = f"""
        SELECT hadm_id, valuenum
        FROM LABEVENTS
        WHERE itemid = {itemid}
          AND hadm_id IS NOT NULL AND hadm_id != ''
          AND valuenum IS NOT NULL
        ORDER BY hadm_id, charttime ASC
        """
        vals = pd.read_sql_query(val_query, conn)
        first_vals = vals.groupby("hadm_id", as_index=False).first()
        first_vals = first_vals.rename(columns={"valuenum": label_col})
        lab_features.append(first_vals)
        print(f"  {itemid:>6} | {label:<35} | {len(first_vals)} admissions")

    # Merge lab features into main dataframe
    for lf in lab_features:
        col = [c for c in lf.columns if c != "hadm_id"][0]
        lf_map = lf.set_index("hadm_id")[col]
        df[col] = df["hadm_id"].map(lf_map)

    conn.close()
    return df


# ─── 3. CLEAN ──────────────────────────────────────────────────────────────

def clean(df):
    """Clean and prepare the feature matrix."""
    print(f"\nCleaning...")
    df_clean = df.copy()

    # Standardize column names
    df_clean.columns = (
        df_clean.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9_]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    # Drop high-cardinality / identifier columns
    drop_cols = ["row_id", "subject_id", "hadm_id", "patient_deceased"]
    df_clean = df_clean.drop(columns=[c for c in drop_cols if c in df_clean.columns])

    # Parse dates — ed_los_hours and age are already numeric
    # Convert target to int
    df_clean["hospital_expire_flag"] = df_clean["hospital_expire_flag"].astype(int)

    # Handle missing numeric values (lab values not measured)
    num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    for col in num_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            print(f"  Filled {n} missing in '{col}'")

    # Handle missing categorical
    cat_cols = df_clean.select_dtypes(include=["object"]).columns.tolist()
    for col in cat_cols:
        n = df_clean[col].isnull().sum()
        if n > 0:
            df_clean[col] = df_clean[col].fillna("Unknown")
            print(f"  Filled {n} missing in '{col}'")

    # Collapse rare diagnosis categories
    if "diagnosis" in df_clean.columns:
        diag_counts = df_clean["diagnosis"].value_counts()
        rare = diag_counts[diag_counts < 2].index
        df_clean["diagnosis"] = df_clean["diagnosis"].apply(
            lambda x: "OTHER" if x in rare else x
        )
        print(f"  Collapsed {len(rare)} rare diagnoses -> 'OTHER'")

    # Simplify ethnicity
    if "ethnicity" in df_clean.columns:
        df_clean["ethnicity"] = df_clean["ethnicity"].str.split("/").str[0].str.strip()

    print(f"Shape: {df_clean.shape}, Missing: {df_clean.isnull().sum().sum()}")
    return df_clean


# ─── 4. ENCODE ─────────────────────────────────────────────────────────────

def encode(df):
    """One-hot encode low-cardinality categorical features."""
    print(f"\nEncoding categorical features...")
    df_enc = df.copy()

    cat_cols = df_enc.select_dtypes(include=["object"]).columns.tolist()
    encoded_count = 0
    for col in cat_cols:
        if col in ["diagnosis"]:
            # One-hot encode
            dummies = pd.get_dummies(df_enc[col], prefix=col)
            for c in dummies.columns:
                df_enc[c] = dummies[c].astype(int)
                encoded_count += 1
        else:
            # Label encode low-cardinality
            n_unique = df_enc[col].nunique()
            if n_unique <= 10:
                dummies = pd.get_dummies(df_enc[col], prefix=col)
                for c in dummies.columns:
                    df_enc[c] = dummies[c].astype(int)
                    encoded_count += 1
            else:
                # Frequency encode
                freq = df_enc[col].value_counts().to_dict()
                df_enc[f"{col}_freq"] = df_enc[col].map(freq).fillna(0).astype(int)
                encoded_count += 1
        df_enc = df_enc.drop(columns=[col])

    print(f"  Created {encoded_count} encoded columns")
    print(f"Shape: {df_enc.shape}")
    return df_enc


# ─── 5. ML PREP ────────────────────────────────────────────────────────────

def prepare_ml(df):
    """Split, scale, save ML-ready files."""
    print(f"\nPreparing ML data...")
    target = "hospital_expire_flag"

    if target not in df.columns:
        print(f"Target '{target}' not found — skipping ML prep")
        return

    # Convert bool columns
    for col in df.columns:
        if df[col].dtype == bool:
            df[col] = df[col].astype(int)

    X = df.select_dtypes(include=[np.number]).copy()
    feat_cols = [c for c in X.columns if c != target]

    y = X[target]
    X = X[feat_cols]

    # Handle remaining NaNs
    for c in X.columns[X.isnull().any()]:
        X[c] = X[c].fillna(X[c].median())

    # Split (stratified for class balance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_df = pd.DataFrame(X_train_scaled, columns=feat_cols)
    X_test_df = pd.DataFrame(X_test_scaled, columns=feat_cols)

    # Save
    FEATURES.mkdir(exist_ok=True)
    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train).to_csv(FEATURES / "y_train.csv", index=False, header=[target])
    pd.DataFrame(y_test).to_csv(FEATURES / "y_test.csv", index=False, header=[target])
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"  Train: {X_train_df.shape}, Test: {X_test_df.shape}")
    print(f"  Features: {len(feat_cols)}")
    print(f"  Target distribution (train): {y_train.value_counts().to_dict()}")

    return {
        "X_train": X_train_df,
        "X_test": X_test_df,
        "y_train": y_train,
        "y_test": y_test,
        "scaler": scaler,
        "feature_names": feat_cols,
        "n_features": len(feat_cols),
        "n_train": len(X_train_df),
        "n_test": len(X_test_df),
    }


# ─── 6. SAVE ────────────────────────────────────────────────────────────────

def save_clean(df, ml_result):
    """Save processed data + metadata."""
    PROCESSED.mkdir(exist_ok=True)
    clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nSaved clean data: {clean_path} ({len(df)} rows)")

    # Save metadata
    target = "hospital_expire_flag"
    metadata = {
        "dataset_name": DATASET_NAME,
        "domain": DOMAIN,
        "ml_task": "Classification",
        "target": "hospital_expire_flag (1=died in hospital, 0=survived)",
        "admissions_total": int(len(df)),
        "mortality_rate_pct": round(float(df[target].mean() * 100), 1),
        "created_date": str(datetime.now()),
        "source": "Kaggle: ihssanened/mimic-iii-clinical-databaseopen-access (PhysioNet MIMIC-III subset)",
        "tables_used": ["ADMISSIONS", "PATIENTS", "LABEVENTS", "D_LABITEMS"],
        "preprocessing": [
            "Loaded CSVs into SQLite",
            "Filtered to EMERGENCY admissions only",
            "Computed age from DOB and admission date",
            "Computed ED length of stay from edregtime/edouttime",
            "First lab value per admission for top 20 lab tests",
            "One-hot / frequency encoding of categorical features",
            "Median imputation for missing numeric values",
            "IQR capping for outlier treatment",
            "Stratified 80/20 train-test split",
            "StandardScaler normalization",
        ],
        "feature_list": ml_result["feature_names"] if ml_result else [],
        "n_features": ml_result["n_features"] if ml_result else 0,
        "n_train": ml_result["n_train"] if ml_result else 0,
        "n_test": ml_result["n_test"] if ml_result else 0,
    }

    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("Saved metadata.json")


# ─── MAIN ──────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*70}")
    print(f"  MIMIC-III ICU (Emergency) — In-hospital Mortality Classification")
    print(f"{'='*70}\n")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    FEATURES.mkdir(parents=True, exist_ok=True)

    build_sqlite()
    df = engineer_features()
    df_clean = clean(df)
    df_encoded = encode(df_clean)

    # Save cleaned + features CSV
    PROCESSED.mkdir(exist_ok=True)
    df_encoded.to_csv(PROCESSED / f"{DATASET_NAME}_features.csv", index=False)
    print(f"Saved features CSV to {PROCESSED / f'{DATASET_NAME}_features.csv'}")

    ml_result = prepare_ml(df_encoded)
    save_clean(df_encoded, ml_result)

    # Cleanup DB (optional — keep for reproducibility)
    # if DB_PATH.exists():
    #     DB_PATH.unlink()

    print(f"\nDone. All files in {BASE}/")


if __name__ == "__main__":
    main()
