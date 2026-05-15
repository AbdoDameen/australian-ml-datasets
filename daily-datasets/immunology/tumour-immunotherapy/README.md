# Dataset #52: Tumour Immunotherapy

**Domain:** Immunology
**ML Task:** Classification
**Source:** NCBI GEO
**Description:** 2,000+ tumour samples

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
cd daily-datasets/immunology/tumour-immunotherapy
python3 prepare_dataset.py
```
