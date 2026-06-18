# Dataset #23: EEG Brainwave (Alcoholism)

**Domain:** Neurology
**ML Task:** Classification
**Source:** UCI
**Description:** 14,980 recordings, 122 subjects

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
cd daily-datasets/neurology/eeg-brainwave
python3 prepare_dataset.py
```
