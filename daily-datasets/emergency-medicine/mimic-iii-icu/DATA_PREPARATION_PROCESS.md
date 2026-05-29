# MIMIC-III ICU (Emergency) — Data Preparation Process

## Source

Kaggle dataset `ihssanened/mimic-iii-clinical-databaseopen-access`, a publicly available subset of the PhysioNet MIMIC-III Clinical Database. Contains 129 admissions and 76,074 lab events for 100 patients.

## Approach

### 1. SQLite ingestion

Loaded 4 CSVs into a local SQLite database:

```
ADMISSIONS (129 rows)  →  admissions table
PATIENTS  (100 rows)   →  patients table
D_LABITEMS (753 rows)  →  lab code lookup
LABEVENTS  (76,074)    →  lab measurements
```

### 2. Emergency admission filter

Kept only `admission_type = 'EMERGENCY'` — 119 admissions, 39 in-hospital deaths (32.8% mortality rate).

### 3. Feature engineering

**Demographics:**
- `age`: computed from DOB and admission date
- `gender`: M/F

**Admission info:**
- `admission_location`, `insurance`, `ethnicity`, `religion`, `marital_status`, `diagnosis`
- `ed_los_hours`: emergency department stay (edouttime - edregtime)

**Lab values:**
- First-measured value of the 20 most common lab tests per admission (potassium, hematocrit, creatinine, anion gap, WBC, platelets, etc.)

### 4. Cleaning & encoding

- Median imputation for missing lab values and ED_LOS
- Rare diagnosis categories (<2 occurrences) collapsed to "OTHER"
- Ethnicity simplified to first segment before "/"
- Missing categoricals filled with "Unknown"
- One-hot encoding for low-cardinality categoricals (<10 unique values)
- Frequency encoding for high-cardinality categoricals

### 5. ML preparation

- Target: `hospital_expire_flag` (1 = died in hospital)
- 71 features total
- Stratified 80/20 train-test split (64 alive / 31 dead in train, 16 alive / 8 dead in test)
- StandardScaler normalization

## Output files

| File | Location | Description |
|------|----------|-------------|
| `mimic-iii-icu_clean.csv` | `processed/` | Fully encoded 119 × 72 dataset |
| `mimic-iii-icu_features.csv` | `processed/` | Same as clean |
| `X_train_scaled.csv` | `features/` | 95 × 71 scaled training features |
| `X_test_scaled.csv` | `features/` | 24 × 71 scaled test features |
| `y_train.csv` | `features/` | Training labels (64 alive, 31 dead) |
| `y_test.csv` | `features/` | Test labels (16 alive, 8 dead) |
| `scaler.pkl` | `features/` | Fitted StandardScaler |
| `mimic_icu.db` | dataset root | SQLite database (reproducible from raw CSVs) |

## Limitations

- Small dataset (119 emergency admissions) — high risk of overfitting with 71 features
- Demo subset of full MIMIC-III — training a production model requires the complete 53,000+ admission dataset
- First-value-only lab aggregation misses temporal trends and last-measured values
