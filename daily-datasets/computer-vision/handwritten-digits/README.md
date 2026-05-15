# Dataset #10: Handwritten Digits

**Domain:** Computer-Vision
**ML Task:** Classification
**Source:** UCI
**Description:** 7,400 digits, 64 features

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
cd daily-datasets/computer-vision/handwritten-digits
python3 prepare_dataset.py
```
