# Data Preparation Process — Bushfire History

## Source

ABARES National Forest Inventory — Fire_For16-21_Attributes.csv. Downloaded from the Australian Government's Forest Data portal.

## Raw Data

- 38,455 rows × 15 columns
- Columns: OID, VALUE, COUNT, FOR_TEN (tenure), FOR_CATEGO (category), FOREST (binary), STATE, FIRE_1617–FIRE_2021 (annual burn codes), ALL_FIRE, FOR_BURNS, FOR_BURN_T
- Fire codes: `U` = unplanned fire, `P` = planned/prescribed burn, blank = no fire
- `FOR_BURNS`: 0–5, with -9 as unknown/missing
- 6,086 duplicate rows identified

## Cleaning Steps

1. **Standardised column names** → lowercase, underscores
2. **Dropped index columns** OID and VALUE (non-informative IDs)
3. **Converted blank strings** to NaN across all object columns
4. **Removed 6,086 duplicate rows** → 32,369 unique polygons
5. **Filled NaN**:
   - Categorical → 'Unknown'
   - FOR_BURNS (-9) → 0 (no burn information)
6. **Outlier capping**: IQR 1.5× on numeric columns (clipped at bounds)

## Feature Engineering

1. **Per-year fire indicators** (for each of 5 years):
   - `fire_XXXX_any_fire` — binary
   - `fire_XXXX_unplanned` — binary
   - `fire_XXXX_planned` — binary
2. **Aggregate counts**:
   - `total_years_burned` (0–5)
   - `total_unplanned_burns` (0–5)
   - `total_planned_burns` (0–5)
3. **Binary flags**:
   - `any_unplanned_fire` — ever had wildfire
   - `always_burned` — burned all 5 years
4. **Dropped redundant columns**: ALL_FIRE (concatenation of year codes), FOR_BURN_T (text description)
5. **One-hot encoded**: FOR_TEN (7 → 6), FOR_CATEGO (4 → 3), STATE (9 → 8) — drop_first

## ML Preparation

- **Target**: `for_burns` — 6 classes (0–5)
- **Features**: 39 numeric features
- **Split**: 80/20 train/test with stratification on target
- **Scaling**: StandardScaler fitted on training data
- **Output**: X_train_scaled.csv (25,895), X_test_scaled.csv (6,474), scaler.pkl
