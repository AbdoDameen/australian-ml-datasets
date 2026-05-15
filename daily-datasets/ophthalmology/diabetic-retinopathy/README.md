# Dataset #17: Diabetic Retinopathy

**Domain:** Ophthalmology
**ML Task:** Image Classification
**Source:** Kaggle
**Description:** 35K retina images

## Status

**Status:** ❌ MISSING
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/ophthalmology/diabetic-retinopathy
python3 prepare_dataset.py
```
