# Dataset #34: Uterine Cancer Radiogenomics

**Domain:** Oncology
**ML Task:** Classification
**Source:** UCI
**Description:** 350 patients, radiomic features

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
cd daily-datasets/oncology/uterine-cancer
python3 prepare_dataset.py
```
