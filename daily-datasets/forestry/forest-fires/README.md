# Dataset #31: Forest Fires (Portugal)

**Domain:** Forestry
**ML Task:** Regression
**Source:** UCI
**Description:** 517 fire records, burned area

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
cd daily-datasets/forestry/forest-fires
python3 prepare_dataset.py
```
