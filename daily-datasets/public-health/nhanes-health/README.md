# Dataset #46: NHANES Health Survey

**Domain:** Public-Health
**ML Task:** Regression
**Source:** CDC
**Description:** 50K+ participants, 500+ features

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
cd daily-datasets/public-health/nhanes-health
python3 prepare_dataset.py
```
