# Dataset #27: Species Distribution (GBIF)

**Domain:** Ecology
**ML Task:** Classification
**Source:** GBIF
**Description:** 1M+ species occurrence records

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
cd daily-datasets/ecology/species-distribution
python3 prepare_dataset.py
```
