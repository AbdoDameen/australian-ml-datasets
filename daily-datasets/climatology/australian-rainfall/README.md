# Dataset #40: Australian Rainfall (BOM)

**Domain:** Climatology
**ML Task:** Forecasting
**Source:** BOM
**Description:** 100K+ monthly rainfall records

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
cd daily-datasets/climatology/australian-rainfall
python3 prepare_dataset.py
```
