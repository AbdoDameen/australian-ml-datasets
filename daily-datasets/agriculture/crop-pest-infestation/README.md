# Dataset #54: Crop Pest Infestation

**Domain:** Agriculture
**ML Task:** Classification
**Source:** DAFF
**Description:** 10K+ pest records

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
cd daily-datasets/agriculture/crop-pest-infestation
python3 prepare_dataset.py
```
