# Data Preparation Process — Thyroid Disease

## Source

UCI Machine Learning Repository — Thyroid Disease database. Donated by Ross Quinlan (Garavan Institute, Sydney, 1987) and later preprocessed by Randolf Werner (Daimler-Benz, 1992) as the `ann-thyroid` subset for backpropagation benchmarking.

URL: https://archive.ics.uci.edu/dataset/102/thyroid+disease

## Files Used

- `ann-train.data` — 3,772 training examples (pre-normalised, space-separated)
- `ann-test.data` — 3,428 testing examples (pre-normalised, space-separated)
- `ann-thyroid.names` — Schema description (21 attributes: 15 binary + 6 continuous, 3 classes)

## Steps

### 1. Data Loading

Both `.data` files were loaded with `numpy.loadtxt()`. They are space-separated, headerless numeric files with 22 columns per row (21 attributes + 1 class). No `?` missing values were found. No pipe-separated IDs (the ann subset was already cleaned of those).

### 2. Column Naming

Column names were assigned based on the hypothyroid schema (Quinlan's attribute set):

| Col | Name | Type | Notes |
|-----|------|------|-------|
| 0 | age | continuous | Normalised [0, 1] |
| 1-15 | sex, on_thyroxine, ..., tt4_measured | binary | 0/1 |
| 16-20 | tsh, t3, tt4, t4u, fti | continuous | Normalised [0, 1] |
| 21 | thyroid_class | target | 1=normal, 2=hyperfunction, 3=subnormal |

### 3. Exploratory Data Analysis

- **Shape:** 7,200 rows × 22 columns (before feature engineering)
- **Missing values:** 0 — the ann subset was pre-cleaned
- **Duplicates:** 71 rows (kept as-is for benchmark reproducibility)
- **Class distribution:** Highly imbalanced — 92.6% normal, 5.1% hyperfunction, 2.3% subnormal
- **Continuous ranges:** All features normalised to [0, 1]

### 4. Cleaning

No cleaning needed — the data was already preprocessed:
- No missing values
- No encoding needed (all numeric)
- No outlier clipping (intentionally kept as benchmark)

### 5. Feature Engineering

Two clinical-ratio features added:
- `tsh_t3_ratio` — TSH divided by T3 (TSH/T3 ratio is used clinically to assess thyroid feedback)
- `calculated_fti` — TT4 × T4U (free thyroxine index, replicated)

### 6. ML Preparation

- **Split:** 80/20 stratified train/test split (preserving class distribution)
- **Scaler:** StandardScaler (fit on training, transform both sets)
- **Files saved:** `X_train_scaled.csv`, `X_test_scaled.csv`, `y_train.csv`, `y_test.csv`, `scaler.pkl`
- **Baseline model:** Random Forest (100 trees) — 99.7% accuracy

### 7. File Organization

```
endocrinology/thyroid-disease/
├── raw/
│   ├── ann-train.data       # Raw training data (3,772 rows)
│   ├── ann-test.data        # Raw test data (3,428 rows)
│   ├── ann-thyroid.names    # Schema documentation
│   ├── ann-Readme           # Dataset description
│   ├── hypothyroid.*        # Related sub-datasets
│   ├── allbp.* / allhyper.* / allhypo.* / allrep.* / dis.* / sick.*
│   └── ...                  # Other UCI thyroid sub-datasets
├── processed/
│   └── thyroid_disease_clean.csv    # Cleaned + engineered features
├── features/
│   ├── X_train_scaled.csv           # ML-ready training features (5,760 × 23)
│   ├── X_test_scaled.csv            # ML-ready test features (1,440 × 23)
│   ├── y_train.csv                  # Training labels
│   ├── y_test.csv                   # Test labels
│   └── scaler.pkl                   # Fitted StandardScaler
├── prepare_dataset.py               # Full pipeline script
├── README.md                        # Dataset overview
├── DATA_PREPARATION_PROCESS.md      # This file
└── metadata.json                    # Dataset metadata
```
