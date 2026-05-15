# Dataset #59: Bushfire Risk (Australia)

**Domain:** Climate
**ML Task:** Classification
**Source:** BNHCRC
**Description:** 50K+ historical bushfire records

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
cd daily-datasets/climate/bushfire-risk
python3 prepare_dataset.py
```
