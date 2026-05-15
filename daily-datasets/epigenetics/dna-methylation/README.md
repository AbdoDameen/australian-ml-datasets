# Dataset #22: DNA Methylation (Breast Cancer)

**Domain:** Epigenetics
**ML Task:** Classification
**Source:** NCBI GEO
**Description:** 485K CpG sites, 96 samples

## Status

**Status:** ❌ MISSING
## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original source data |
| `processed/` | Cleaned and feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline script |

## To process

```bash
cd daily-datasets/epigenetics/dna-methylation
python3 prepare_dataset.py
```
