# Dataset #35: Water Potability

**Domain:** Freshwater-Ecology
**ML Task:** Classification
**Source:** Kaggle
**Description:** 3,276 water samples, quality

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
cd daily-datasets/freshwater-ecology/water-potability
python3 prepare_dataset.py
```
