# Dataset #37: MIMIC-III ICU (Emergency)

**Domain:** Emergency-Medicine
**ML Task:** Classification
**Source:** PhysioNet
**Description:** 53,423 ICU admissions

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
cd daily-datasets/emergency-medicine/mimic-iii-icu
python3 prepare_dataset.py
```
