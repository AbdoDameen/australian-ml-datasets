# Chronic Kidney Disease — Data Preparation Process

## Source

**UCI Machine Learning Repository — Dataset #336**
Rubini, L., Soundarapandian, P., & Eswaran, P. (2015).
https://archive.ics.uci.edu/dataset/336/chronic_kidney_disease

## Raw Data

- **Format:** CSV (from Kaggle mirror — mansoordaku/ckdisease)
- **Size:** 400 rows × 25 columns (24 features + 1 target)
- **Target:** `classification` → binary: ckd / notckd
- **Missing values:** ~2-10% per column, coded as blanks

## Pipeline Steps

### 1. Loading (prepare_dataset.py → load_data)
Loaded `raw/kidney_disease.csv` via pandas.

### 2. Cleaning (prepare_dataset.py → clean_data)
| Step | Detail |
|------|--------|
| Drop ID | `id` column removed (not predictive) |
| Rename | `wc→wbcc`, `rc→rbcc`, `classification→class` |
| Column names | Lowercased, spaces → underscores |
| Duplicates | Removed (0 found) |
| Numeric NaNs | Filled with column median |
| Categorical NaNs | Filled with column mode |
| Outlier capping | IQR ×1.5 capped on: age, bgr, bu, sc, sod, pot, hemo, pcv, wbcc, rbcc |

### 3. Feature Engineering (prepare_dataset.py → engineer_features)
| Feature | Description |
|---------|-------------|
| Binary encoding | rbc, pc, pcc, ba, htn, dm, cad, appet, pe, ane → 0/1 |
| Target encoding | class: ckd→1, notckd→0 |
| eGFR approx | 175 × sc^-1.154 × age^-0.203 |
| BUN/creatinine ratio | bu ÷ sc |
| Hemoglobin × PCV | Interaction for anaemia severity |
| Comorbidity count | Sum of htn + dm + cad + ane + pe |
| Anemia severity | Ordinal: severe/moderate/mild/normal from hemo thresholds |
| Ordinal encoding | sg, al, su encoded on their natural scales |
| Factorized | Remaining object columns → integer codes |

### 4. ML Preparation (prepare_dataset.py → prepare_ml)
- **Scaler:** StandardScaler
- **Split:** 80/20 stratified (maintains class balance in train/test)
- **Outputs:**
  - `features/X_train_scaled.csv` — scaled training features
  - `features/X_test_scaled.csv` — scaled testing features
  - `features/y_train.csv` — training labels
  - `features/y_test.csv` — testing labels
  - `features/scaler.pkl` — fitted scaler for inference

## Output Files

| Path | Description |
|------|-------------|
| `processed/chronic_kidney_disease_clean.csv` | Cleaned + feature-engineered data |
| `features/*` | ML-ready train/test splits |
| `metadata.json` | Column descriptions + pipeline log |
| `prepare_dataset.py` | Reproducible pipeline |

## Model Suggestion

This dataset is well-suited for:
- **Logistic Regression** (interpretable, good baseline)
- **Random Forest** (handles feature interactions)
- **XGBoost** (best performance on small medical datasets)

The data has high class separability — many lab values (sc, hemo, sg, al) are strong predictors of CKD.
