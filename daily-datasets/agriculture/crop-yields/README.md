# Dataset #29: Crop Yields (Global)

**Domain:** Agriculture
**ML Task:** Regression
**Source:** OWID
**Description:** 80K+ records, 100+ crops

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
cd daily-datasets/agriculture/crop-yields
python3 prepare_dataset.py
```
