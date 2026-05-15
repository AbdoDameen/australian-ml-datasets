# Data Preparation Process — NSW Dwelling Units

## Overview

This document describes the data preparation pipeline for the NSW Dwelling Units dataset. The original data is a CSV index of ABS time series metadata for dwelling unit approvals in New South Wales, Australia.

**Source:** Australian Bureau of Statistics — Building Approvals Australia

## Pipeline Steps

### 1. Load Raw Data

- Read CSV with `pandas.read_csv()`, skipping the first 2 header rows (unnamed column headers and the real header row)
- Columns renamed to: `data_item_description`, `series_type`, `series_id`, `series_start`, `series_end`, `no_obs`, `unit`, `data_type`, `freq`, `collection_month`
- Copyright/attribution rows filtered out

### 2. Exploratory Data Analysis

- 17 data rows (after filtering), 12 columns
- 1 duplicate row found (series A418458A appears twice)
- 2 blank columns (col1, col2) with all null values
- 3 series types: Original (7), Trend (6), Seasonally Adjusted (4)
- 3 building types: Houses, Dwellings excluding houses, Total (Type of Building)
- 2 sectors: Private Sector, Total Sectors
- All series start in 1983, end in 2026 (43-year span)

### 3. Data Cleaning & Parsing

- **Duplicate removal:** 1 duplicate row removed (series A418458A Original)
- **Description parsing:** The `data_item_description` field is semicolon-delimited — parsed into:
  - `building_type` (Houses, Dwellings excluding houses, or Total)
  - `sector` (Private Sector or Total Sectors)
- **Date parsing:** Converted `series_start` / `series_end` from string to datetime, extracted:
  - `start_year`, `end_year`
  - `start_decade` (floor to nearest 10)
  - `series_span_years` (end_year - start_year)
- **Missing value handling:** No missing values in this small dataset; treatment is defined for robustness

### 4. Feature Engineering

- **Series type flags:** `is_original`, `is_seasonally_adjusted`, `is_trend` (binary)
- **Sector encoding:** `sector_encoded` — Private Sector=0, Total Sectors=1
- **Building type encoding:** One-hot encoded into `bldg_Houses`, `bldg_Dwellings excluding houses`, `bldg_Total (Type of Building)`
- **Time features:**
  - `start_decade_num` — decade as numeric (e.g., 1980.0)
  - `start_month` — month of series start (1–12)
  - `era` — categorical era: pre_2000, 2000s, 2010s, 2020s
- **Series ID prefix:** First character of series ID → `prefix_freq` (frequency encoding)

### 5. ML Preparation

- **Feature set:** 16 numeric features selected for ML
- **Target:** `no_obs` — the number of observations in each series
- **Train/test split:** 80/20 with `random_state=42`
  - Training: 12 samples
  - Test: 4 samples
- **Scaling:** `StandardScaler` fitted on training data, applied to both train and test sets
- **Artifacts saved:**
  - `scaler.pkl` — fitted scaler for inference
  - `sector_mapping.csv` — sector encoding reference
  - Feature matrices: `X_train_scaled.csv`, `X_test_scaled.csv`
  - Target vectors: `y_train.csv`, `y_test.csv`

## Notes

- This is a small metadata dataset (16 series × 16 features) — suitable for demonstration, benchmarking, or as a lookup table
- The `no_obs` target is constant at 513 for all series; this dataset is better suited for classification (series type prediction) or clustering (series grouping) than regression
- To access the actual time series values, each Series ID can be used to query the ABS API or the original Excel data files
