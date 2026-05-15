# Dataset #21: Beijing Air Quality

**Domain:** Environmental
**ML Task:** Regression
**Source:** UCI
**Description:** 43,824 hourly PM2.5 readings

## Status

**Status:** 📥 HAS DATA
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/environmental/beijing-air-quality
python3 prepare_dataset.py
```
