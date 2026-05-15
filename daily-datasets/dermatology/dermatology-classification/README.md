# Dataset #33: Dermatology

**Domain:** Dermatology
**ML Task:** Classification
**Source:** UCI
**Description:** 366 patients, 6 skin diseases

## Status

**Status:** ⚠️ SMALL DATASET (366 rows)
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/dermatology/dermatology-classification
python3 prepare_dataset.py
```
