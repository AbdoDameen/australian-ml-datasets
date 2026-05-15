# Dataset #55: Antibiotic Resistance (AMR)

**Domain:** Microbiology
**ML Task:** Classification
**Source:** NCBI
**Description:** 500K+ bacterial isolates

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
cd daily-datasets/microbiology/antibiotic-resistance
python3 prepare_dataset.py
```
