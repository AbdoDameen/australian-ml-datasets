# Dataset #50: PISA Global Scores

**Domain:** Education
**ML Task:** Regression
**Source:** OECD
**Description:** 600K+ students, 80 countries

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
cd daily-datasets/education/pisa-global-scores
python3 prepare_dataset.py
```
