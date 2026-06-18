# Dataset #58: Hospital Readmission

**Domain:** Health-Informatics
**ML Task:** Classification
**Source:** UCI
**Description:** 101K+ hospital records

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
cd daily-datasets/health-informatics/hospital-readmission
python3 prepare_dataset.py
```
