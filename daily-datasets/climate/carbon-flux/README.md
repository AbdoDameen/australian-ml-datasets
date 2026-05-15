# Dataset #45: Carbon Flux (OzFlux)

**Domain:** Climate
**ML Task:** Regression
**Source:** OzFlux
**Description:** 500K+ CO2 flux measurements

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
cd daily-datasets/climate/carbon-flux
python3 prepare_dataset.py
```
