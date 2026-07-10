# Diabetes Readmission — Data Preparation Process

## Source

**UCI Machine Learning Repository — Diabetes 130-US Hospitals (1999–2008)**
https://archive.ics.uci.edu/dataset/296/diabetes+130+us+hospitals+for+years+1999-2008

## Raw Data

- **Format:** CSV (`diabetic_data.csv`)
- **Size:** 101,766 rows × 50 columns
- **Target:** `readmitted` — `<30` (11.2%), `>30` (34.9%), `NO` (53.9%)
- **Missing data:** weight (96.8%), max_glu_serum (94.7%), A1Cresult (83.3%), medical_specialty (49.1%), payer_code (39.6%), race (2.2%), diag_1/2/3 (minor)
- **Class imbalance:** 11.2% positive rate for 30-day readmission

## Pipeline Steps

### 1. Loading
Loaded raw CSV via pandas with `na_values="?"`. Diagnosis codes kept as strings to prevent type coercion.

### 2. Cleaning

| Step | Detail |
|------|--------|
| Drop IDs | `encounter_id`, `patient_nbr` — row identifiers, no signal |
| Drop high-missing | `weight` (97%), `payer_code` (40%), `examide`/`citoglipton` (all zeros) |
| Duplicates | Checked — 0 found |
| Race NaNs | Filled with mode (`Caucasian`) — ~2% affected |
| Diagnosis NaNs | Filled with `Unknown` — 0.02%–1.4% per column |
| Column names | Standardized to lowercase with underscores |

### 3. Feature Engineering

| Feature | Description |
|---------|-------------|
| `age_mid` | Age bins (e.g. `[70-80)` → 75) encoded as numeric midpoint |
| `is_female` | Binary gender indicator |
| `race_*` | One-hot encoded race: Caucasian, AfricanAmerican, Hispanic, Asian, Other |
| `adm_type_*` | One-hot encoded admission type: Emergency, Urgent, Elective, Newborn, etc. |
| `a1c_level` | A1C result as ordinal (0=None, 1=Norm, 2=>7, 3=>8) |
| `glucose_level` | Max glucose serum as ordinal (0=None, 1=Norm, 2=>200, 3=>300) |
| `med_change` | Whether medication was changed (Ch/No → 1/0) |
| `diabetes_med` | Diabetes medication prescribed (Yes/No → 1/0) |
| 21 medication cols | Metformin, insulin, etc. encoded ordinal (0=No, 1=Down, 2=Steady, 3=Up) |
| `spec_*` | One-hot encoded top 10 medical specialties (rare ones collapsed to "Other") |

### 4. ML Preparation

- **Target:** Binary — `readmit_30d` = 1 if `readmitted == "<30"`, else 0
- **Scaler:** StandardScaler
- **Split:** 80/20 stratified by target (preserves 11.2% class ratio)
- **Features:** 60 numeric features
- **Outputs:**
  - `features/X_train_scaled.csv` — 81,412 × 60 scaled training features (121MB)
  - `features/X_test_scaled.csv` — 20,354 × 60 scaled testing features (31MB)
  - `features/y_train.csv` — training targets
  - `features/y_test.csv` — testing targets
  - `features/scaler.pkl` — fitted scaler for inference

> **Note:** Generated data files exceed GitHub's 100MB per-file limit. They are gitignored. Run `python3 prepare_dataset.py` to regenerate.

## Output Files

| Path | Description |
|------|-------------|
| `processed/diabetes-readmission_clean.csv` | Cleaned + feature-engineered data (101,766 × 66) |
| `features/*` | ML-ready train/test splits (gitignored, 165MB total) |
| `prepare_dataset.py` | Reproducible pipeline script |
| `metadata.json` | Dataset metadata and transformation log |
| `README.md` | Dataset overview and quick start |
