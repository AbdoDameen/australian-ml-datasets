# Data Preparation Process — Wine Quality V2

## Source

UCI ML Repository, Wine Quality dataset (Vinho Verde, Portugal). Two CSV files, semicolon-separated with quoted headers: `winequality-red.csv` (1,599 rows) and `winequality-white.csv` (4,898 rows). Citation: Cortez et al., *Modeling wine preferences by data mining from physicochemical properties*, Decision Support Systems 47(4):547-553, 2009.

## Pipeline

`prepare_dataset.py` — run with `python3 prepare_dataset.py` (system Python, pandas + scikit-learn).

### 1. Load

- `pd.read_csv(sep=';')` on both files (semicolon delimiter, quoted headers)
- `wine_type` column added from source file (red/white)
- Concatenated: 6,497 rows x 13 cols

### 2. Clean

- Column names lowercased, special chars → underscore
- 1,177 duplicate rows removed (18% — white wines cluster heavily) → 5,320 rows
- No missing values present in source
- Outlier capping at 1.5x IQR per physicochemical feature (clipped, not dropped):
  - fixed_acidity 304, volatile_acidity 279, chlorides 237, sulphates 163, citric_acid 143, residual_sugar 141, free_sulfur_dioxide 44, ph 49, total_sulfur_dioxide 10, density 3, alcohol 1

### 3. Feature Engineering

- `total_acidity` = fixed + volatile + citric
- `fixed_to_volatile` — acidity harshness ratio
- `so2_ratio` — free/total sulfur dioxide (preservative profile)
- `sweetness` — residual sugar bands: dry (<1), off_dry (1-5), medium (5-20), sweet (>20)
- `alcohol_band` + `is_high_alcohol` (≥12%)
- `sugar_per_density` — sugar load proxy
- `chlorides_per_alcohol` — savory-to-strength contrast
- `quality_label` — binary target (quality ≥ 7) for classification use

### 4. ML Prep

- One-hot: wine_type, sweetness, alcohol_band → bool cast to int
- Numeric-only feature matrix (27 cols after encoding)
- 80/20 split, random_state=42 (no stratification — regression target)
- StandardScaler fit on train, transform test

### 5. Outputs

| File | Contents |
|------|----------|
| `processed/wine-quality-v2_clean.csv` | 5,320 x 22, zero missing |
| `features/X_train_scaled.csv` | 4,256 x 27 |
| `features/X_test_scaled.csv` | 1,064 x 27 |
| `features/y_train.csv` / `y_test.csv` | quality score 3-9 |
| `features/scaler.pkl` | fitted StandardScaler |

## Reproduce

```bash
cd daily-datasets/oenology/wine-quality-v2
python3 prepare_dataset.py
```

All outputs regenerate from the raw CSVs in `raw/`.
