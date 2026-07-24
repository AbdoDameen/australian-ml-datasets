# Bushfire History — Australia (2016–2021)

Broad-scale fire history across Australian forests, sourced from the National Forest Inventory. Each row is a forest polygon with 5 years of annual burn records (planned/prescribed vs unplanned/wildfire).

**Source:** [ABARES — Forests Australia](https://www.agriculture.gov.au/abares/forestsaustralia/forest-data)

## Data

- 32,369 unique forest polygons
- 39 engineered features
- 6-class target: total burn count (0–5)

### Features

| Feature | Description |
|---|---|
| `count` | Area weight (grid cells per polygon) |
| `forest` | Is forest (1) or non-forest (0) |
| `for_ten_*` | Forest tenure (one-hot: lease, private, state, etc.) |
| `for_catego_*` | Forest category (native, plantation, etc.) |
| `state_*` | State/territory (one-hot) |
| `fire_XXXX_any_fire` | Binary: any burn that year |
| `fire_XXXX_unplanned` | Binary: unplanned burn that year |
| `fire_XXXX_planned` | Binary: planned burn that year |
| `total_years_burned` | Count of years with any burn (0–5) |
| `total_unplanned_burns` | Count of years with unplanned fire |
| `total_planned_burns` | Count of years with planned fire |
| `any_unplanned_fire` | Binary: ever had an unplanned fire |
| `always_burned` | Binary: burned all 5 years |

### Target

`for_burns` — total number of times burned (0–5). Suitable for multiclass classification.

## ML-Ready Files (`features/`)

| File | Description |
|---|---|
| `X_train_scaled.csv` | Training features (25,895 × 39) |
| `X_test_scaled.csv` | Test features (6,474 × 39) |
| `y_train.csv` | Training labels |
| `y_test.csv` | Test labels |
| `scaler.pkl` | Fitted StandardScaler |
| `feature_names.json` | Feature column names |

## Usage

```python
import pandas as pd
import pickle

X_train = pd.read_csv("features/X_train_scaled.csv")
y_train = pd.read_csv("features/y_train.csv")

with open("features/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
```

## Files

| Path | Description |
|---|---|
| `raw/Fire_For16-21_Attributes.csv` | Original source data |
| `processed/bushfire-history_clean.csv` | Cleaned + feature-engineered dataset |
| `features/` | ML-ready train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |
| `metadata.json` | Dataset metadata |
