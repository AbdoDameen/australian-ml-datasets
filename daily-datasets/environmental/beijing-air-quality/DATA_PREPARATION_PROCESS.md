# Beijing Air Quality — Data Preparation Process

## Source

**UCI Machine Learning Repository**
Liang, X., et al. (2015). Beijing PM2.5 Data Set.
https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data

## Raw Data

- **Format:** CSV (PRSA_data_2010.1.1-2014.12.31.csv)
- **Size:** 43,824 rows × 13 columns
- **Target:** `pm2.5` — hourly PM2.5 concentration (µg/m³)
- **Missing values:** 2,067 (4.7%) in pm2.5 column — missing during calm/low-winter conditions

## Pipeline Steps

### 1. Loading
Loaded raw CSV via pandas. Header row 0, no skip.

### 2. Cleaning

| Step | Detail |
|------|--------|
| Drop ID | `No` column removed (row index, no signal) |
| Column names | Lowercased, spaces→underscores, special chars removed |
| Duplicates | Checked (0 found) |
| pm2.5 NaNs | Filled with (year, month) group median — preserves seasonal pattern |
| Outlier capping | IQR ×1.5 capped on: pm2.5, Iws (wind speed heavy tail), PRES, TEMP, DEWP |

### 3. Feature Engineering

| Feature | Description |
|---------|-------------|
| Datetime | Concatenated year+month+day+hour as pd.datetime |
| dayofweek | 0=Monday through 6=Sunday |
| quarter | Calendar quarter (1-4) |
| is_weekend | 1 if Saturday/Sunday, else 0 |
| season | Winter=0, Spring=1, Summer=2, Autumn=3 |
| wind_* | One-hot encoded wind direction: NE, NW, SE, cv |

### 4. ML Preparation

- **Scaler:** StandardScaler
- **Split:** 80/20 random split (random_state=42)
- **Features:** 18 numeric features (all engineered + meteorology, excluding datetime)
- **Outputs:**
  - `features/X_train_scaled.csv` — 35,059 × 18 scaled training features
  - `features/X_test_scaled.csv` — 8,765 × 18 scaled testing features
  - `features/y_train.csv` — training targets
  - `features/y_test.csv` — testing targets
  - `features/scaler.pkl` — fitted scaler for inference

## Output Files

| Path | Description |
|------|-------------|
| `processed/beijing-air-quality_clean.csv` | Cleaned + feature-engineered data (43,824 × 20) |
| `features/*` | ML-ready train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |
| `metadata.json` | Dataset metadata and transformation log |
