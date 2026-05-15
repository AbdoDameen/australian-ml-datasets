# Dataset #44: Student Performance

**Domain:** Education
**ML Task:** Regression
**Source:** UCI
**Description:** 1,044 students, grade prediction

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
cd daily-datasets/education/student-performance
python3 prepare_dataset.py
```
