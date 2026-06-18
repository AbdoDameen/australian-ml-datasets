# Dataset #19: Beachwatch Water Quality

**Domain:** Oceanography
**ML Task:** Classification
**Source:** NSW Gov
**Description:** 50K+ water samples

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
cd daily-datasets/oceanography/beachwatch-water-quality
python3 prepare_dataset.py
```
