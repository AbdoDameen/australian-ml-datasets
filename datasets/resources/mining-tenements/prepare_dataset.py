#!/usr/bin/env python3
"""
prepare_dataset.py — Standardized ML Pipeline for WA Mining Tenements

Loads raw CSV, cleans, standardizes, creates features, and saves:
  - processed/mining_tenements_clean.csv  (cleaned dataframe)
  - features/mining_tenements_ml.csv      (scaled ML-ready features)
  - features/scaler.pkl                   (fitted StandardScaler)

Usage:
    cd /path/to/mining-tenements/
    python3 prepare_dataset.py
"""

import os
import sys
import pickle
import warnings
import logging
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("prepare_dataset")

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
FEATURES_DIR = os.path.join(BASE_DIR, "features")

RAW_CSV = os.path.join(RAW_DIR, "mining_tenements_sample.csv")
CLEAN_CSV = os.path.join(PROCESSED_DIR, "mining_tenements_clean.csv")
ML_CSV = os.path.join(FEATURES_DIR, "mining_tenements_ml.csv")
SCALER_PKL = os.path.join(FEATURES_DIR, "scaler.pkl")

# Columns to drop entirely (internal IDs, geometry, raw address/holder detail)
DROP_COLUMNS = [
    "GmlId",
    "oid",
    "gid",
    "tenid",
    "Shape",
    # Time-only components (date features extracted separately)
    "granttime",
    "starttime",
    "endtime",
    # Raw address/holder detail columns — too granular for general ML
    "addr1",
    "addr2",
    "addr3",
    "addr4",
    "addr5",
    "addr6",
    "addr7",
    "addr8",
    "addr9",
    "holder1",
    "holder2",
    "holder3",
    "holder4",
    "holder5",
    "holder6",
    "holder7",
    "holder8",
    "holder9",
    # Special interest / extraction date — operational metadata
    "special_in",
    "extract_da",
]

# Date columns to parse and expand into features
DATE_COLUMNS = ["grantdate", "startdate", "enddate"]

# Columns to keep as-is (or use for target/categorical encoding later)
CATEGORICAL_LOW_CARD = ["type", "survstatus"]  # one-hot encode
CATEGORICAL_HIGH_CARD = ["fmt_tenid"]  # frequency-encode

# Target definition
TARGET_COL = "is_live"


def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV with appropriate parsing."""
    log.info("Loading: %s", path)
    df = pd.read_csv(
        path,
        dtype_backend="numpy_nullable",
        low_memory=False,
    )
    log.info("Loaded %d rows x %d columns", df.shape[0], df.shape[1])
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to lowercase, replace special chars with underscores."""
    rename_map = {}
    for col in df.columns:
        new = (
            col.lower()
            .replace("(", "_")
            .replace(")", "")
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "_")
            .replace("__", "_")
            .strip("_")
        )
        if new != col.lower():
            rename_map[col] = new
    if rename_map:
        log.info("Standardising %d column names", len(rename_map))
        df = df.rename(columns=rename_map)
    return df


def parse_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    """Convert date strings to datetime, flag parse failures per column."""
    for col in date_cols:
        if col not in df.columns:
            log.warning("Date column '%s' not found — skipping", col)
            continue
        orig_null = df[col].isna().sum()
        df[col] = pd.to_datetime(df[col], errors="coerce")
        new_null = df[col].isna().sum()
        if new_null > orig_null:
            log.warning(
                "  %s: %d additional NaT after parsing (out of %d rows)",
                col,
                new_null - orig_null,
                len(df),
            )
    return df


def extract_date_features(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    """Extract year, month, day, dayofweek, quarter from each date column."""
    for col in date_cols:
        if col not in df.columns:
            continue
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        base = col.replace("date", "")
        df[f"{base}year"] = df[col].dt.year.astype("Int64")
        df[f"{base}month"] = df[col].dt.month.astype("Int64")
        df[f"{base}day"] = df[col].dt.day.astype("Int64")
        df[f"{base}dayofweek"] = df[col].dt.dayofweek.astype("Int64")
        df[f"{base}quarter"] = df[col].dt.quarter.astype("Int64")
        log.info(
            "  %s -> year/month/day/dayofweek/quarter (%d non-null)",
            col,
            df[col].notna().sum(),
        )
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values:
      - object/string/category -> 'Unknown'
      - numeric -> median (column-wise)
    """
    text_cols = df.select_dtypes(include=["object", "string", "category"]).columns
    num_cols = df.select_dtypes(include=["number", "Int64", "Float64"]).columns

    for col in text_cols:
        n_miss = df[col].isna().sum()
        if n_miss:
            df[col] = df[col].fillna("Unknown")
            log.info("  %s: filled %d NaN -> 'Unknown'", col, n_miss)

    for col in num_cols:
        n_miss = df[col].isna().sum()
        if n_miss:
            med = df[col].median(skipna=True)
            if pd.isna(med):
                med = 0
            df[col] = df[col].fillna(med)
            log.info("  %s: filled %d NaN -> median=%.4f", col, n_miss, med)

    return df


def drop_columns(df: pd.DataFrame, drop_list: list) -> pd.DataFrame:
    """Drop columns that exist in the dataframe."""
    existing = [c for c in drop_list if c in df.columns]
    if existing:
        log.info("Dropping %d columns: %s", len(existing), existing)
        df = df.drop(columns=existing)
    return df


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create binary target is_live from tenstatus."""
    if "tenstatus" in df.columns:
        df[TARGET_COL] = (df["tenstatus"].str.strip().str.upper() == "LIVE").astype(int)
        log.info(
            "Target created: is_live — %d LIVE, %d other (out of %d)",
            df[TARGET_COL].sum(),
            (df[TARGET_COL] == 0).sum(),
            len(df),
        )
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-hot encode low-cardinality categorical columns.
    Frequency-encode high-cardinality columns.
    Drops the original text column after encoding.
    """
    # ── One-hot encode ───────────────────────────────────────────────────
    for col in CATEGORICAL_LOW_CARD:
        if col not in df.columns:
            log.warning("Low-card column '%s' not found — skipping", col)
            continue
        dummies = pd.get_dummies(df[col], prefix=col, dummy_na=False)
        df = pd.concat([df, dummies.astype(int)], axis=1)
        log.info("  %s: one-hot encoded -> %d columns", col, dummies.shape[1])
        if col in df.columns:
            df = df.drop(columns=[col])

    # ── Frequency encode ─────────────────────────────────────────────────
    for col in CATEGORICAL_HIGH_CARD:
        if col not in df.columns:
            log.warning("High-card column '%s' not found — skipping", col)
            continue
        freq = df[col].value_counts(normalize=True)
        df[f"{col}_freq"] = df[col].map(freq)
        unknown_mask = df[col].isna()
        if unknown_mask.any():
            df.loc[unknown_mask, f"{col}_freq"] = 0.0
        log.info(
            "  %s: frequency-encoded (%d unique values, %.1f%% coverage by top-10)",
            col,
            len(freq),
            freq.head(10).sum() * 100,
        )
        df = df.drop(columns=[col])

    return df


def save_clean_data(df: pd.DataFrame, path: str):
    """Save cleaned dataset to processed/."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    log.info("Saved cleaned data: %s (%d rows x %d cols)", path, df.shape[0], df.shape[1])


def create_ml_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select numeric features, apply StandardScaler, save ML-ready data.
    Excludes the target column from scaling (kept as-is).
    """
    from sklearn.preprocessing import StandardScaler

    # Identify feature columns (numeric, exclude target, exclude pure IDs)
    exclude_patterns = ["tenstatus", TARGET_COL]
    feature_cols = [
        c
        for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c])
        and c not in exclude_patterns
        and not any(p in c.lower() for p in ["tenstatus"])
    ]

    # Drop any that are all-NaN
    feature_cols = [c for c in feature_cols if df[c].notna().sum() > 0]

    log.info("ML features: %d numeric columns selected", len(feature_cols))

    X = df[feature_cols].copy()

    # Final NA fill (safety net)
    for c in X.columns:
        if X[c].isna().any():
            med = X[c].median(skipna=True)
            X[c] = X[c].fillna(0 if pd.isna(med) else med)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols, index=df.index)

    # Add target back
    X_scaled_df[TARGET_COL] = df[TARGET_COL].values

    # Save scaler
    os.makedirs(FEATURES_DIR, exist_ok=True)
    with open(SCALER_PKL, "wb") as f:
        pickle.dump(scaler, f)
    log.info("Scaler saved: %s", SCALER_PKL)

    return X_scaled_df


def main():
    log.info("=" * 60)
    log.info("WA Mining Tenements — Dataset Preparation Pipeline")
    log.info("=" * 60)

    # 1. Load
    df = load_data(RAW_CSV)

    # 2. Standardize column names
    df = standardize_columns(df)

    # 3. Drop internal / unwanted columns
    df = drop_columns(df, DROP_COLUMNS)

    # 4. Parse dates
    df = parse_dates(df, DATE_COLUMNS)

    # 5. Extract date features
    df = extract_date_features(df, DATE_COLUMNS)

    # 6. Drop raw date columns now that features are extracted
    raw_date_cols_existing = [c for c in DATE_COLUMNS if c in df.columns]
    if raw_date_cols_existing:
        df = df.drop(columns=raw_date_cols_existing)
        log.info("Dropped raw date columns: %s", raw_date_cols_existing)

    # 7. Create target
    df = create_target(df)

    # 8. Handle missing values
    log.info("Handling missing values...")
    df = handle_missing_values(df)

    # 9. Encode categoricals
    log.info("Encoding categorical features...")
    df = encode_categoricals(df)

    # 10. Drop tenstatus (now that target is derived)
    if "tenstatus" in df.columns:
        df = df.drop(columns=["tenstatus"])
        log.info("Dropped raw tenstatus column (target derived)")

    # 11. Drop st_area_the_geom and st_perimeter_the_geom if present
    #     (geometric attributes derived from raw geometry)
    for geo_col in ["st_area_the_geom", "st_perimeter_the_geom"]:
        if geo_col in df.columns:
            df = df.drop(columns=[geo_col])
            log.info("Dropped geometry-derived column: %s", geo_col)

    # 12. Drop unit_of_me (constant or near-constant)
    if "unit_of_me" in df.columns:
        df = df.drop(columns=["unit_of_me"])
        log.info("Dropped unit_of_me column")

    # 13. Save clean data
    save_clean_data(df, CLEAN_CSV)

    # 14. Create ML features with StandardScaler
    log.info("Creating ML-ready features...")
    ml_df = create_ml_features(df)
    ml_df.to_csv(ML_CSV, index=False)
    log.info("Saved ML features: %s (%d rows x %d cols)", ML_CSV, ml_df.shape[0], ml_df.shape[1])

    log.info("=" * 60)
    log.info("Pipeline complete!")
    log.info("  Clean data:  %s", CLEAN_CSV)
    log.info("  ML features: %s", ML_CSV)
    log.info("  Scaler:      %s", SCALER_PKL)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
