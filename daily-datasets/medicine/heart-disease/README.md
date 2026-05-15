# Dataset #1: Heart Disease

**Domain:** Medicine
**ML Task:** Classification
**Source:** UCI
**Description:** 303 patients, heart disease diagnosis

## Status

**Status:** ⚠️ SMALL DATASET (303 rows)
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/medicine/heart-disease
python3 prepare_dataset.py
```
