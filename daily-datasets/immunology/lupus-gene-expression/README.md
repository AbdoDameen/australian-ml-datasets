# Dataset #49: Lupus Gene Expression

**Domain:** Immunology
**ML Task:** Classification
**Source:** NCBI GEO
**Description:** 1,200+ samples

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
cd daily-datasets/immunology/lupus-gene-expression
python3 prepare_dataset.py
```
