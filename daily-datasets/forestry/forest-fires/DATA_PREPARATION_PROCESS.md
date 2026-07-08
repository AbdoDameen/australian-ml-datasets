# Data Preparation Process — Forest Fires

## 1. Ingestion

- **Source:** UCI ML Repository (forestfires.csv)
- **Format:** CSV with header row
- **Rows ingested:** 517
- **No missing values** in raw data

## 2. Cleaning

| Step | Detail |
|------|--------|
| Column names | Lowercased, spaces→underscores, special chars stripped |
| Duplicates | 4 removed → 513 rows remaining |
| Missing values | None present in raw data |
| Outlier capping | 1.5× IQR on all numeric features (excl. `area` — target) |
| Outliers capped | y(51), ffmc(53), dmc(17), dc(17), isi(14), temp(2), rh(12), wind(13), rain(8) |

## 3. Feature Engineering

**Target transformation:**
- `area` is highly right-skewed (48% zeros, max 1090ha, mean 12.85)
- Applied `log1p(area)` → `area_log` for regression

**Temporal encoding:**
- `month` → `month_num` (1–12 ordinal mapping)
- `day` → 7 one-hot binary columns (`day_mon` through `day_sun`)

**Interaction features:**
- `temp_rh_ratio` = temp / (rh + 1) — heat × dryness interaction
- `dc_isi_interaction` = dc × isi — drought × spread potential

**Final feature count:** 20

## 4. ML Preparation

- **Target:** `area_log` (log1p-transformed burned area)
- **Split:** 80/20 train/test, random_state=42
- **Scaling:** StandardScaler (fitted on training set only)
- **Output:** `X_train_scaled.csv` (410×20), `X_test_scaled.csv` (103×20)
- **Saved:** `scaler.pkl` for inference-time transformation

## 5. Key Observations

- Almost half the records have zero burned area — a two-stage model (classify fire/no-fire first, then regress on non-zero) may outperform direct regression
- The fire weather indices (FFMC, DMC, DC, ISI) capture similar information to raw weather — potential multicollinearity to watch for
- Month heavily concentrated in Aug–Sep (69% of fires in these two months — dry Portuguese summer)
- Rain is near-zero for most records — very sparse predictor
