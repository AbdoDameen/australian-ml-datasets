# Dataset #41: Wine Quality (Vinho Verde)

**Domain:** Oenology
**ML Task:** Regression
**Source:** UCI
**Description:** 4,898 wines, quality score

## Status

⬜ EMPTY

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/oenology/wine-quality
python3 prepare_dataset.py
```
