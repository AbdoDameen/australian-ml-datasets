# Dataset #45: Chronic Kidney Disease

**Domain:** Nephrology
**ML Task:** Binary Classification (ckd vs notckd)
**Source:** UCI ML Repository
**Description:** 400 patients, 24 clinical features, CKD diagnosis

## Status

**Status:** ✅ PROCESSED

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data (kidney_disease.csv) |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/nephrology/chronic-kidney-disease
python3 prepare_dataset.py
```
