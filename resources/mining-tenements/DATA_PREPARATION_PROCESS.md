# Data Preparation Process

## Overview
This document details the steps applied in `prepare_dataset.py` to transform the raw WA Mining Tenements CSV into cleaned and ML-ready datasets.

## Pipeline Steps

### 1. Load Raw Data
- Load `raw/mining_tenements_sample.csv` (5000 rows, 40 columns)
- Uses `dtype_backend='numpy_nullable'` for efficient NA handling

### 2. Column Name Standardisation
- Convert all column names to lowercase
- Replace special characters (spaces, parentheses, hyphens, dots) with underscores
- Collapse consecutive underscores into one

**Example**: `st_area(the_geom)` → `st_area_the_geom`

### 3. Drop Internal / Redundant Columns (28 removed)
The following columns are dropped because they contain internal IDs, raw geometry, detailed personally-identifiable holder/address info, or operational metadata unsuitable for general ML:

- **Internal IDs**: `GmlId`, `oid`, `gid`, `tenid`
- **Raw Geometry**: `Shape` (complex multipolygon WKT)
- **Time-Only Components**: `granttime`, `starttime`, `endtime` (date components extracted separately)
- **Holder Details**: `holder1`–`holder9` (names of tenement holders)
- **Address Details**: `addr1`–`addr9` (postal addresses)
- **Operational Metadata**: `special_in`, `extract_da` (internal flags, extraction timestamps)

### 4. Date Parsing
- Columns `grantdate`, `startdate`, `enddate` are parsed with `pd.to_datetime(..., errors='coerce')`
- Records with unparseable dates become NaT and are handled in the missing-value step
- Note: ~1656 records have missing/unparseable grant and end dates (typically newer or pending tenements)

### 5. Date Feature Extraction
From each date column, five numeric features are extracted:

| Feature | Description |
|---------|-------------|
| `{base}year` | Year (e.g., 2020) |
| `{base}month` | Month (1–12) |
| `{base}day` | Day of month (1–31) |
| `{base}dayofweek` | Day of week (0=Monday, 6=Sunday) |
| `{base}quarter` | Quarter (1–4) |

After extraction, the raw date columns are dropped.

### 6. Target Variable Creation
- `is_live`: Binary indicator where `1` = tenement status is `LIVE`, `0` = otherwise
- Derived from the `tenstatus` column (stripped, upper-cased comparison)
- **Distribution**: 3344 LIVE (66.9%), 1656 other (33.1%) — moderately imbalanced

### 7. Missing Value Imputation

| Column Type | Strategy | Reason |
|-------------|----------|--------|
| **Text/Categorical** | Fill with `'Unknown'` | Preserves the fact that a value was missing without distorting frequencies |
| **Numeric** | Fill with column **median** | Robust to outliers; preserves central tendency |

Imputed columns: `grantyear/month/day/dow/qtr`, `endyear/month/day/dow/qtr` (all from the 1656 records without grant/end dates)

### 8. Categorical Encoding

**Low-Cardinality (One-Hot Encoding)**:
- `type`: 2 unique values → `type_COAL MINING LEASE`, `type_EXPLORATION LICENCE`
- `survstatus`: 2 unique values → `survstatus_SURVEYED`, `survstatus_UNSURVEYED`

**High-Cardinality (Frequency Encoding)**:
- `fmt_tenid`: 5000 unique values (each tenement is unique) → frequency-encoded as `fmt_tenid_freq`
- Each value is replaced by its global frequency proportion (range: 0.0002 for unique items)
- This captures the "rareness" of a tenement ID without blowing up dimensionality

### 9. Additional Column Drops
- **`tenstatus`**: Dropped after target derivation (redundant with `is_live`)
- **`st_area_the_geom`**, **`st_perimeter_the_geom`**: Geometry-derived attributes from raw Shape — highly correlated with `legal_area`
- **`unit_of_me`**: Near-constant column (all values are "HA" or "BL")

### 10. Save Cleaned Dataset
- **File**: `processed/mining_tenements_clean.csv`
- **Shape**: 5000 rows × 23 columns
- **Size**: ~329 KB

### 11. ML Feature Scaling
Uses `sklearn.preprocessing.StandardScaler` to standardise all numeric features:
- Centers to mean=0, scales to unit variance
- The target (`is_live`) is excluded from scaling but re-joined
- Fitted scaler saved to `features/scaler.pkl` for reproducibility

**Output**: `features/mining_tenements_ml.csv` (5000 rows × 23 columns)

## Removed Data Summary

| Category | Columns Removed | Count |
|----------|----------------|-------|
| Internal IDs | GmlId, oid, gid, tenid | 4 |
| Raw Geometry | Shape | 1 |
| Time-only | granttime, starttime, endtime | 3 |
| Holder info | holder1–holder9 | 9 |
| Address info | addr1–addr9 | 9 |
| Operational | special_in, extract_da | 2 |
| Raw dates | grantdate, startdate, enddate | 3 |
| Status (raw) | tenstatus | 1 |
| Geo-derived | st_area_the_geom, st_perimeter_the_geom | 2 |
| Constant | unit_of_me | 1 |
| **Total** | | **35** |

## Notes
- The dataset is suitable for binary classification (predicting LIVE vs non-LIVE status)
- Date features enable temporal analysis and trend detection
- The scaler pickle allows exact reproduction of transformations on new/unseen data
- 1656 records with missing grant/end dates may warrant special handling (e.g., exclude from date-focused analyses)
