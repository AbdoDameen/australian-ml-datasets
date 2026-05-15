# Dataset #8: Breast Cancer Wisconsin

**Domain:** Cancer
**ML Task:** Classification
**Source:** UCI
**Description:** 569 patients, malignant vs benign

## Status

📥 RAW DATA ONLY

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/cancer/breast-cancer-wisconsin
python3 prepare_dataset.py
```
