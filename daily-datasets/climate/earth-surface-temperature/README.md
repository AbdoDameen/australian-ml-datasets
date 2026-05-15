# Dataset #3: Earth Surface Temperature

**Domain:** Climate
**ML Task:** Time Series
**Source:** Kaggle
**Description:** 8.5M global temp records

## Status

📥 RAW DATA ONLY

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/climate/earth-surface-temperature
python3 prepare_dataset.py
```
