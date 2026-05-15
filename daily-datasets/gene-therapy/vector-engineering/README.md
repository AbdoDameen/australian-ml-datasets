# Dataset #30: Gene Therapy Vectors

**Domain:** Gene-Therapy
**ML Task:** Regression
**Source:** AddGene
**Description:** 5,000+ genetic constructs

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
cd daily-datasets/gene-therapy/vector-engineering
python3 prepare_dataset.py
```
