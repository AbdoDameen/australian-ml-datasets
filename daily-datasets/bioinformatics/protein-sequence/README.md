# Dataset #57: Protein Sequence (Bioinfo)

**Domain:** Bioinformatics
**ML Task:** Classification
**Source:** UCI
**Description:** 15K+ protein sequences

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
cd daily-datasets/bioinformatics/protein-sequence
python3 prepare_dataset.py
```
