#!/usr/bin/env python3
"""
PISA Global Scores - ML-Ready Pipeline

Extracts SAS files from zips, reads questionnaire + cognitive data,
merges on CNTSTUID, creates binary math proficiency classification,
saves processed/ and features/ outputs, cleans up extracted files.

Usage:
    /tmp/pisa_venv/bin/python3 prepare_dataset.py
"""

import os
import sys
import json
import zipfile
import warnings
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
DATASET_DIR = BASE_DIR
EXTRACT_DIR = Path("/home/abdodameen/pisa_extract")
PROCESSED_DIR = BASE_DIR / "processed"
FEATURES_DIR = BASE_DIR / "features"
METADATA_PATH = BASE_DIR / "metadata.json"

EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
FEATURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Config ─────────────────────────────────────────────────────────────────
SAMPLE_SIZE = 100_000
RANDOM_STATE = 42
OECD_AVG_MATH = 489  # PISA 2022 OECD average in math


def log(msg):
    print(f"[PISA] {msg}")


def extract_sas_from_zip(zip_name, expected_sas_name, extract_to):
    """Extract a SAS file from a zip archive."""
    zip_path = DATASET_DIR / zip_name
    sas_path = extract_to / expected_sas_name

    if sas_path.exists():
        log(f"  {expected_sas_name} already extracted, reusing")
        return sas_path

    if not zip_path.exists():
        log(f"  WARNING: {zip_name} not found, skipping")
        return None

    log(f"  Extracting {zip_name} -> {expected_sas_name} ...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        members = zf.namelist()
        log(f"  Zip contents: {members}")
        zf.extract(expected_sas_name, extract_to)

    if sas_path.exists():
        size_gb = sas_path.stat().st_size / (1024**3)
        log(f"  Extracted {expected_sas_name} ({size_gb:.1f} GB)")
    return sas_path


def read_sas_with_limit(path, columns, limit=None):
    """Read a SAS7BDAT file with pyreadstat, selecting columns and optionally limiting rows."""
    import pyreadstat

    size_gb = path.stat().st_size / (1024**3)
    log(f"  Reading {path.name} ({size_gb:.1f} GB)")
    log(f"  Selecting {len(columns)} columns: {columns[:5]}...")
    log(f"  Row limit: {limit or 'all'}")

    df, meta = pyreadstat.read_sas7bdat(
        path,
        usecols=columns,
        row_limit=limit or 0,
    )

    log(f"  Read {len(df)} rows, {len(df.columns)} columns")
    return df


def load_questionnaire_data():
    """Load student background questionnaire data (contains PV scores + weights)."""
    log("─" * 60)
    log("STEP 1: Extract and load Student Questionnaire (QQQ)")

    zip_name = "STU_QQQ_SAS.zip"
    expected_sas = "CY08MSP_STU_QQQ.SAS7BDAT"
    sas_path = extract_sas_from_zip(zip_name, expected_sas, EXTRACT_DIR)

    if not sas_path or not sas_path.exists():
        log("  ERROR: QQQ SAS file not available")
        sys.exit(1)

    # Actual column names discovered from file exploration
    qqq_columns = [
        # Identifiers
        'CNT',           # Country code
        'CNTSTUID',      # Student ID (composite key)
        # Demographics
        'ST004D01T',     # Gender
        'ST005Q01JA',    # Birth year (note: JA suffix, not TA_0)
        'ST022Q01TA',    # Immigrant background
        'LANGN',         # Language at home
        'IMMIG',         # Immigrant status (derived)
        # SES
        'HISEI',         # Socioeconomic index
        'PAREDINT',      # Parents education (integer)
        'HOMEPOS',       # Home possessions index (derived)
        # Home resources
        'ST250Q01JA',    # Computer at home
        'ST251Q01JA',    # Internet at home
        'ST034Q01TA',    # Home possessions item
        # School belonging and support
        'BELONG',        # Belonging
        'FAMSUP',        # Family support
        'TEACHSUP',      # Teacher support
        # Math affect
        'MATHPREF',      # Math preference
        'MATHEASE',      # Math ease
        'MATHMOT',       # Math motivation
        'MATHEFF',       # Math self-efficacy
        'ANXMAT',        # Math anxiety
        'MATHPERS',      # Math persistence
        # Effort
        'EFFORT1',       # Effort measure 1
        # Plausible Values - Math (use first 5)
        'PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH',
        # Plausible Values - Reading (use first 5)
        'PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ',
        # Plausible Values - Science (use first 5)
        'PV1SCIE', 'PV2SCIE', 'PV3SCIE', 'PV4SCIE', 'PV5SCIE',
        # Weights
        'W_FSTUWT',      # Final student weight
        'SENWT',         # Senate weight
    ]

    df = read_sas_with_limit(sas_path, qqq_columns, limit=SAMPLE_SIZE)
    log(f"  QQQ loaded: {len(df)} rows")
    log(f"  Columns: {list(df.columns)}")
    return df


def load_cognitive_data():
    """Load cognitive item response data (cross-reference with QQQ via CNTSTUID).
    
    COG has 5023 columns of item-level responses. We only need CNTSTUID for 
    cross-referencing. PV scores are in the QQQ file.
    """
    log("─" * 60)
    log("STEP 2: Load Cognitive Scores (COG) - cross-reference")

    # Check if COG SAS is already in the dataset dir or extract dir
    cog_sas_in_dir = DATASET_DIR / "CY08MSP_STU_COG.SAS7BDAT"
    cog_sas_in_extract = EXTRACT_DIR / "CY08MSP_STU_COG.SAS7BDAT"
    cog_zip_path = DATASET_DIR / "STU_COG_SAS.zip"

    sas_path = None
    if cog_sas_in_dir.exists():
        sas_path = cog_sas_in_dir
        log(f"  Using existing COG SAS file ({sas_path.stat().st_size / (1024**3):.1f} GB)")
    elif cog_sas_in_extract.exists():
        sas_path = cog_sas_in_extract
    elif cog_zip_path.exists():
        log(f"  Extracting {cog_zip_path.name}...")
        with zipfile.ZipFile(cog_zip_path, 'r') as zf:
            zf.extract("CY08MSP_STU_COG.SAS7BDAT", EXTRACT_DIR)
        sas_path = EXTRACT_DIR / "CY08MSP_STU_COG.SAS7BDAT"

    if sas_path and sas_path.exists():
        # COG has 5023 columns of item-level responses.
        # We only read CNTSTUID for cross-referencing.
        import pyreadstat
        log(f"  Reading CNTSTUID from COG for cross-reference")
        df, _ = pyreadstat.read_sas7bdat(sas_path, usecols=['CNTSTUID'], row_limit=SAMPLE_SIZE)
        log(f"  COG loaded: {len(df)} rows with CNTSTUID cross-reference")
        return df
    else:
        log("  WARNING: COG SAS file not found, will use QQQ-only data")
        return None


def clean_data(qqq_df, cog_df=None):
    """Clean data, merge if possible, handle missing values."""
    log("─" * 60)
    log("STEP 3: Clean and merge data")

    df = qqq_df.copy()

    # If we have COG data, merge on CNTSTUID to cross-reference
    if cog_df is not None:
        log(f"  QQQ rows: {len(df)}, COG rows: {len(cog_df)}")
        merged = pd.merge(df, cog_df, on='CNTSTUID', how='inner')
        log(f"  Cross-referenced with COG: {len(merged)} rows (dropped {len(df) - len(merged)} without COG match)")
        df = merged

    # Drop rows missing target (PV1MATH)
    before = len(df)
    df = df.dropna(subset=['PV1MATH'])
    log(f"  Dropped {before - len(df)} rows with missing PV1MATH")

    # Define demographic columns for imputation
    cat_cols = ['ST004D01T', 'ST022Q01TA', 'LANGN', 'IMMIG',
                'ST250Q01JA', 'ST251Q01JA', 'MATHPREF', 'MOTIVAT']
    num_cols = ['HISEI', 'PAREDINT', 'HOMEPOS', 'BELONG',
                'FAMSUP', 'TEACHSUP', 'MATHEASE', 'MATHMOT',
                'MATHEFF', 'ANXMAT', 'MATHPERS',
                'ST034Q01TA', 'ST005Q01JA', 'EFFORT1']

    # Only process columns that actually exist
    for col in cat_cols:
        if col in df.columns:
            na = df[col].isna().sum()
            if na > 0:
                mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else 'missing'
                df[col] = df[col].fillna(mode_val)
                log(f"  Imputed {col}: {na} -> mode '{mode_val}'")

    for col in num_cols:
        if col in df.columns:
            na = df[col].isna().sum()
            if na > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                log(f"  Imputed {col}: {na} -> median {median_val:.2f}")

    log(f"  Final shape: {df.shape}")
    return df


def create_targets(df):
    """Create classification target based on OECD average."""
    log("─" * 60)
    log("STEP 4: Create classification target")

    # Binary target: above/below OECD average (489)
    df['math_proficiency'] = np.where(df['PV1MATH'] >= OECD_AVG_MATH, 1, 0)
    above = df['math_proficiency'].sum()
    below = len(df) - above
    log(f"  OECD avg threshold: {OECD_AVG_MATH}")
    log(f"  Above: {above} ({above/len(df)*100:.1f}%)")
    log(f"  Below: {below} ({below/len(df)*100:.1f}%)")

    # Quartile-based levels for reference
    q1, q2, q3 = df['PV1MATH'].quantile([0.25, 0.50, 0.75])
    log(f"  PV1MATH quartiles: Q1={q1:.0f}, Q2={q2:.0f} (median), Q3={q3:.0f}")

    def math_level(pv):
        if pv <= q1:
            return 'low'
        elif pv <= q2:
            return 'low_medium'
        elif pv <= q3:
            return 'medium_high'
        else:
            return 'high'

    df['math_level'] = df['PV1MATH'].apply(math_level)
    return df


def engineer_features(df):
    """Feature engineering: one-hot encode categoricals, prepare numeric features."""
    log("─" * 60)
    log("STEP 5: Feature engineering")

    # One-hot encode country
    cnt_dummies = pd.DataFrame(index=df.index)
    if 'CNT' in df.columns:
        cnt_dummies = pd.get_dummies(df['CNT'], prefix='country', drop_first=False)
        log(f"  CNT: {df['CNT'].nunique()} countries -> {cnt_dummies.shape[1]} features")

    # One-hot encode gender
    gender_dummies = pd.DataFrame(index=df.index)
    if 'ST004D01T' in df.columns:
        gender_dummies = pd.get_dummies(df['ST004D01T'], prefix='gender', drop_first=True)
        log(f"  GENDER: {gender_dummies.shape[1]} features")

    # Select numeric features
    numeric_candidates = [
        'HISEI', 'PAREDINT', 'HOMEPOS', 'BELONG',
        'FAMSUP', 'TEACHSUP', 'MATHEASE', 'MATHMOT',
        'MATHEFF', 'ANXMAT', 'MATHPERS',
        'ST005Q01JA', 'EFFORT1', 'ST034Q01TA',
        'ST250Q01JA', 'ST251Q01JA',
    ]
    available_numeric = [c for c in numeric_candidates if c in df.columns]
    log(f"  Numeric features available: {len(available_numeric)}")

    X_numeric = df[available_numeric].copy()

    # Combine
    X = pd.concat([cnt_dummies, gender_dummies, X_numeric], axis=1)

    # Handle any remaining NaN
    nan_before = X.isna().sum().sum()
    if nan_before > 0:
        X = X.fillna(X.median())
        log(f"  Filled {nan_before} remaining NaN values")

    log(f"  Total feature matrix: {X.shape[0]} rows, {X.shape[1]} columns")
    return X, available_numeric


def ml_prep(X, y, df, numeric_features):
    """Stratified 80/20 split, StandardScaler, save all outputs."""
    log("─" * 60)
    log("STEP 6: ML prep - stratified split + scaling")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    log(f"  Train: {len(X_train)}, Test: {len(X_test)}")
    log(f"  Train distribution: {y_train.value_counts().to_dict()}")
    log(f"  Test distribution: {y_test.value_counts().to_dict()}")

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )

    log("─" * 60)
    log("STEP 7: Saving outputs")

    # Save processed data (cleaned CSV subset)
    processed_cols = ['CNTSTUID', 'CNT', 'PV1MATH', 'PV2MATH', 'PV3MATH',
                      'PV4MATH', 'PV5MATH', 'PV1READ', 'PV2READ', 'PV3READ',
                      'PV4READ', 'PV5READ', 'PV1SCIE', 'PV2SCIE', 'PV3SCIE',
                      'PV4SCIE', 'PV5SCIE',
                      'math_proficiency', 'math_level',
                      'ST004D01T', 'HISEI', 'PAREDINT', 'HOMEPOS', 'BELONG',
                      'W_FSTUWT', 'SENWT']
    available_processed = [c for c in processed_cols if c in df.columns]
    processed_path = PROCESSED_DIR / "pisa_cleaned.parquet"
    df[available_processed].to_parquet(processed_path, index=False)
    log(f"  Saved processed: {processed_path} ({len(df)} rows)")

    # Save train/test features
    train_path = FEATURES_DIR / "X_train.parquet"
    test_path = FEATURES_DIR / "X_test.parquet"
    y_train_path = FEATURES_DIR / "y_train.parquet"
    y_test_path = FEATURES_DIR / "y_test.parquet"
    scaler_path = FEATURES_DIR / "scaler.pkl"

    X_train_scaled.to_parquet(train_path, index=False)
    X_test_scaled.to_parquet(test_path, index=False)
    y_train.to_frame(name='math_proficiency').to_parquet(y_train_path, index=False)
    y_test.to_frame(name='math_proficiency').to_parquet(y_test_path, index=False)

    import joblib
    joblib.dump(scaler, scaler_path)

    log(f"  X_train: {train_path} {X_train_scaled.shape}")
    log(f"  X_test: {test_path} {X_test_scaled.shape}")
    log(f"  y_train: {y_train_path} ({len(y_train)})")
    log(f"  y_test: {y_test_path} ({len(y_test)})")

    # Feature info
    info = {
        'n_features': X.shape[1],
        'n_train': len(X_train),
        'n_test': len(X_test),
        'feature_names': list(X.columns),
        'numeric_features': numeric_features,
        'target': 'math_proficiency',
        'target_type': 'binary (above/below OECD avg 489)',
        'target_distribution_train': {str(k): int(v) for k, v in y_train.value_counts().items()},
        'target_distribution_test': {str(k): int(v) for k, v in y_test.value_counts().items()},
        'oecd_avg_threshold': OECD_AVG_MATH,
        'scaler_mean': scaler.mean_.tolist(),
        'scaler_scale': scaler.scale_.tolist(),
    }

    # Need available_numeric from outer scope
    info_path = FEATURES_DIR / "feature_info.json"
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2, default=str)
    log(f"  Feature info: {info_path}")


def update_metadata(n_features=None):
    """Update metadata.json to PROCESSED status."""
    log("─" * 60)
    log("STEP 8: Update metadata.json")

    metadata = {
        "dataset_id": 17,
        "name": "PISA Global Scores",
        "folder": "education/pisa-global-scores",
        "domain": "Education",
        "ml_task": "Classification",
        "source": "OECD",
        "description": "600K+ students, 80 countries - Math proficiency classification",
        "status": "✅ PROCESSED",
        "has_raw_data": True,
        "has_pipeline": True,
        "n_samples": SAMPLE_SIZE,
        "n_features_after_encoding": n_features,
        "target": "math_proficiency",
        "target_type": "binary (above/below OECD avg 489)",
        "oecd_avg_math": OECD_AVG_MATH,
    }

    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=2)
    log(f"  Updated {METADATA_PATH}")


def cleanup():
    """Delete all extracted SAS files to free ~20 GB."""
    log("─" * 60)
    log("STEP 9: Cleanup - delete extracted SAS files")

    total_freed = 0
    if EXTRACT_DIR.exists():
        for f in EXTRACT_DIR.iterdir():
            if f.suffix in ('.sas7bdat',):
                size = f.stat().st_size
                f.unlink()
                total_freed += size
                log(f"  Deleted {f.name} ({size / (1024**3):.1f} GB)")

        remaining = list(EXTRACT_DIR.iterdir())
        if not remaining:
            EXTRACT_DIR.rmdir()
            log(f"  Removed empty {EXTRACT_DIR}")
        else:
            log(f"  {len(remaining)} files remain in {EXTRACT_DIR}")

    log(f"  Total freed: {total_freed / (1024**3):.1f} GB")


def main():
    log("=" * 60)
    log("PISA GLOBAL SCORES - ML PIPELINE")
    log("=" * 60)

    # 1. Load questionnaire (QQQ) - contains PV scores, demographics, weights
    qqq_df = load_questionnaire_data()

    # 2. Load cognitive (COG) - cross-reference only (item responses not needed)
    cog_df = load_cognitive_data()

    # 3. Clean and merge
    df = clean_data(qqq_df, cog_df)

    # 4. Create targets
    df = create_targets(df)

    # 5. Feature engineering
    X, available_numeric = engineer_features(df)
    y = df['math_proficiency']

    # 6. ML prep
    ml_prep(X, y, df, available_numeric)

    # 7. Update metadata
    update_metadata(n_features=X.shape[1])

    # 8. Cleanup
    cleanup()

    log("=" * 60)
    log("PIPELINE COMPLETE!")
    log(f"  Processed: {PROCESSED_DIR / 'pisa_cleaned.parquet'}")
    log(f"  Features: {FEATURES_DIR}")
    log(f"  Target: math_proficiency (binary, threshold={OECD_AVG_MATH})")
    log("=" * 60)


if __name__ == '__main__':
    _num_feats = None
    main()
