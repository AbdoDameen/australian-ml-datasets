# Dataset #25: Chest X-Ray (Pneumonia)

**Domain:** Radiology
**ML Task:** Image Classification
**Source:** Kaggle
**Description:** 5,863 X-ray images

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
cd daily-datasets/radiology/chest-xray
python3 prepare_dataset.py
```
