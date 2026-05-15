# Dataset #32: Chronic Kidney Disease

**Domain:** Nephrology
**ML Task:** Classification
**Source:** UCI
**Description:** 400 patients, CKD diagnosis

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
cd daily-datasets/nephrology/chronic-kidney-disease
python3 prepare_dataset.py
```
