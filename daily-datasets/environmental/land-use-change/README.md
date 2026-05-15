# Dataset #53: Land Use Change (NSW)

**Domain:** Environmental
**ML Task:** Classification
**Source:** SEED NSW
**Description:** 500K+ land parcels

## Status

⬜ EMPTY

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/environmental/land-use-change
python3 prepare_dataset.py
```
