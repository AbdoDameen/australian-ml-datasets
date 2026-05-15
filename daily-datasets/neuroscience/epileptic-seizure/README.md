# Dataset #6: Epileptic Seizure

**Domain:** Neuroscience
**ML Task:** Classification
**Source:** UCI
**Description:** 11,500 EEG readings

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
cd daily-datasets/neuroscience/epileptic-seizure
python3 prepare_dataset.py
```
