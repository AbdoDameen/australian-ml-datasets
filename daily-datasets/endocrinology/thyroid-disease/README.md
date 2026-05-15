# Dataset #38: Thyroid Disease

**Domain:** Endocrinology
**ML Task:** Classification
**Source:** UCI
**Description:** 7,200 patients, hyperthyroid

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
cd daily-datasets/endocrinology/thyroid-disease
python3 prepare_dataset.py
```
