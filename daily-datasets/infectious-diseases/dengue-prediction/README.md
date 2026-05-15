# Dataset #7: Dengue Prediction

**Domain:** Infectious-Diseases
**ML Task:** Regression
**Source:** DrivenData
**Description:** 1,456 weekly dengue cases

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
cd daily-datasets/infectious-diseases/dengue-prediction
python3 prepare_dataset.py
```
