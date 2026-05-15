# Dataset #5: Mushroom Classification

**Domain:** Biology
**ML Task:** Classification
**Source:** UCI
**Description:** 8,124 mushrooms, edible vs poisonous

## Status

**Status:** 📥 HAS DATA
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/biology/mushroom-classification
python3 prepare_dataset.py
```
