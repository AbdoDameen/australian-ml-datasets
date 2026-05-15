# Dataset #26: Diabetes Readmission

**Domain:** Geriatrics
**ML Task:** Classification
**Source:** UCI
**Description:** 101,766 hospital records

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
cd daily-datasets/geriatrics/diabetes-readmission
python3 prepare_dataset.py
```
