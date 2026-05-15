# Dataset #43: Kangaroo Tracking (ALA)

**Domain:** Wildlife
**ML Task:** Classification
**Source:** ALA
**Description:** 50K+ species occurrences

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
cd daily-datasets/wildlife/kangaroo-tracking
python3 prepare_dataset.py
```
