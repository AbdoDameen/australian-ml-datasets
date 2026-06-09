# Crop Yields (Global) — Australian Extract 🇦🇺🌾

**Domain:** Agriculture  
**ML Task:** Regression (predict crop yield in kg/ha)  
**Source:** [SAGE / UW-Madison Global Crop Yield Dataset](https://sage.nelson.wisc.edu/data-and-models/datasets/global-crop-yield-dataset-5-minute-resolution/)  
**Spatial Resolution:** 5 arc-min (~9.2 km at equator)  
**Temporal Range:** 1982–2015 (34 years)

## Overview

Australian agricultural pixel data extracted from 136 global GeoTIFF rasters (4 crops × 34 years). The raw rasters cover global growing regions at ~9.2 km resolution with simulated yield values in kg/ha.

## Crops in Australia

| Crop | Australia Pixels | Yield Range (kg/ha) |
|------|-----------------|---------------------|
| 🟡 Wheat | 341,122 | 338 – 3,426 |
| 🌽 Maize | 2,584 | 1,608 – 5,947 |
| 🍚 Rice | 1,972 | 2,587 – 5,114 |

**Soybean** has no data in Australia's extent.

## Dataset Contents

- **`processed/crop_yields_australia_clean.csv`** — 345,678 rows × 16 columns
- **`features/`** — ML-ready train/test splits (scaled X, raw y, scaler)
- **`prepare_dataset.py`** — reproducible pipeline (download → extract → clean → feature engineer → ML prep)
- **Raw GeoTIFFs** available via GitHub Releases (`raw-data-v1`)

## Features

- **Temporal:** year, year_since_1982, decade, is_drought_year
- **Spatial:** latitude, longitude, abs_latitude, climate_zone (one-hot)
- **Target:** `yield_kg_ha`

## Usage

```python
import pandas as pd

df = pd.read_csv("processed/crop_yields_australia_clean.csv")
print(df.shape)  # (345678, 16)
print(df['crop_wheat'].sum(), "wheat records")
```
