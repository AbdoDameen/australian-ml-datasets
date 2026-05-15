# Dataset #15: Protein Tertiary Structure

**Domain:** Biochemistry
**ML Task:** Regression
**Source:** UCI
**Description:** 45,730 proteins, RMSD prediction

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
cd daily-datasets/biochemistry/protein-tertiary-structure
python3 prepare_dataset.py
```
