# Dataset #9: E. coli Protein Localization

**Domain:** Microbiology
**ML Task:** Classification
**Source:** UCI
**Description:** 336 proteins, 8 classes

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
cd daily-datasets/microbiology/ecoli-protein-localization
python3 prepare_dataset.py
```
