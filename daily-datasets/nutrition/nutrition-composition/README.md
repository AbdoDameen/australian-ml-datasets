# Dataset #24: Food Nutrition (USDA)

**Domain:** Nutrition
**ML Task:** Classification
**Source:** USDA
**Description:** 7,800+ foods, 80+ nutrients

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
cd daily-datasets/nutrition/nutrition-composition
python3 prepare_dataset.py
```
