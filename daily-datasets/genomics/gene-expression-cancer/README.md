# Dataset #2: Gene Expression Cancer

**Domain:** Genomics
**ML Task:** Classification
**Source:** UCI
**Description:** 801 patients, 20K genes, 5 cancer types

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
cd daily-datasets/genomics/gene-expression-cancer
python3 prepare_dataset.py
```
