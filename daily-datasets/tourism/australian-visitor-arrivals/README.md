# Dataset #18: Australian Visitor Arrivals

**Domain:** Tourism
**ML Task:** Forecasting
**Source:** data.gov.au
**Description:** 10K+ monthly visitor records

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
cd daily-datasets/tourism/australian-visitor-arrivals
python3 prepare_dataset.py
```
