# Dataset #28: Liver Disease (ILPD)

**Domain:** Gastroenterology
**ML Task:** Classification
**Source:** UCI
**Description:** 583 patients, liver disease

## Status

📥 RAW DATA ONLY

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/gastroenterology/liver-disease
python3 prepare_dataset.py
```
