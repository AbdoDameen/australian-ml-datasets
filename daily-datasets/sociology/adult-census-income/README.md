# Dataset #11: Adult Census Income

**Domain:** Sociology
**ML Task:** Classification
**Source:** UCI
**Description:** 48,842 individuals, income prediction

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
cd daily-datasets/sociology/adult-census-income
python3 prepare_dataset.py
```
