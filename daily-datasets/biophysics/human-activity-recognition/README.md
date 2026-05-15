# Dataset #13: Human Activity Recognition

**Domain:** Biophysics
**ML Task:** Classification
**Source:** UCI
**Description:** 10,299 smartphone sensor samples

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
cd daily-datasets/biophysics/human-activity-recognition
python3 prepare_dataset.py
```
