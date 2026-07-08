# Forest Fires (Portugal) — Daily ML Dataset

**Domain:** Forestry, Environmental Science  
**ML Task:** Regression (predict burned area)  
**Source:** [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Forest+Fires)  
**Rows:** 513 (after cleanup: 517 → 513, 4 duplicates removed)  
**Features:** 20 (spatial, weather, fire indices, temporal, interactions)

## Data

517 fire records from Montesinho Natural Park, Portugal (Jan 2000–Dec 2003). Each record is a fire with spatial coordinates, weather conditions, fire weather indices, and the total burned area.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| `x`, `y` | numeric | Spatial coordinates within park grid |
| `month`, `day` | categorical | Month and day of week |
| `ffmc`, `dmc`, `dc` | numeric | Fire Weather Index components (Fine Fuel Moisture Code, Duff Moisture Code, Drought Code) |
| `isi` | numeric | Initial Spread Index |
| `temp` | numeric | Temperature (°C) |
| `rh` | numeric | Relative humidity (%) |
| `wind` | numeric | Wind speed (km/h) |
| `rain` | numeric | Rain (mm/m²) |
| `area` | numeric | **Target** — burned area (hectares, highly skewed: 48% zero) |
| `area_log` | numeric | log1p-transformed area (for regression) |

## Files

```
forestry/forest-fires/
├── raw/forestfires.csv         # Original source data
├── processed/forest-fires_clean.csv  # Cleaned + feature-engineered
├── features/X_train_scaled.csv      # 410 samples, 20 features (scaled)
├── features/X_test_scaled.csv       # 103 samples, 20 features (scaled)
├── features/y_train.csv             # Training targets (area_log)
├── features/y_test.csv              # Test targets (area_log)
├── features/scaler.pkl              # Fitted StandardScaler
├── prepare_dataset.py               # Reproducible pipeline
├── metadata.json                    # Dataset metadata
└── README.md                        # This file
```

## Run the pipeline

```bash
cd daily-datasets/forestry/forest-fires
python3 prepare_dataset.py
```

## Citation

Cortez, P., & Morais, A. (2007). A data mining approach to predict forest fires using meteorological data.
