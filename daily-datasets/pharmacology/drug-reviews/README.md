# Dataset #12: Drug Reviews

**Domain:** Pharmacology
**ML Task:** NLP
**Source:** UCI
**Description:** 215K drug reviews, sentiment analysis

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
cd daily-datasets/pharmacology/drug-reviews
python3 prepare_dataset.py
```
