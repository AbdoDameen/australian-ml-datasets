# Dataset #47: Fossil Occurrences (PBDB)

**Domain:** Palaeontology
**ML Task:** Classification
**Source:** PBDB
**Description:** 1M+ fossil records

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
cd daily-datasets/palaeontology/fossil-occurrences
python3 prepare_dataset.py
```
