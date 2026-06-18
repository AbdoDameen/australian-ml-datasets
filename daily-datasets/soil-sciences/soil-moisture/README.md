# Dataset #51: Soil Moisture (TERN)

**Domain:** Soil-Sciences
**ML Task:** Regression
**Source:** TERN
**Description:** 100K+ soil moisture readings

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
cd daily-datasets/soil-sciences/soil-moisture
python3 prepare_dataset.py
```
