# Dataset #4: Wine Quality

**Domain:** Chemistry
**ML Task:** Regression
**Source:** UCI
**Description:** 4,898 wines, physicochemical properties

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
cd daily-datasets/chemistry/wine-quality
python3 prepare_dataset.py
```
