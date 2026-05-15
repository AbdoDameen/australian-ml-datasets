# Dataset #42: Cervical Cancer Risk

**Domain:** Oncology
**ML Task:** Classification
**Source:** UCI
**Description:** 858 patients, 36 risk factors

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
cd daily-datasets/oncology/cervical-cancer-risk
python3 prepare_dataset.py
```
