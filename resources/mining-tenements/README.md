# Western Australian Mining Tenements Dataset

## Overview
This dataset contains information about mining tenements in Western Australia, sourced from the Department of Mines, Industry Regulation and Safety (DMIRS) through the SLIP WFS service.

## Source
- **Dataset Name**: Mining Tenements (DMIRS-003)
- **Source**: data.wa.gov.au
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Last Updated**: 2026-05-06

## Files

| File | Description |
|------|-------------|
| `raw/mining_tenements_sample.csv` | Original raw data (5000 rows, 40 columns) |
| `processed/mining_tenements_clean.csv` | Cleaned & feature-engineered dataset (23 columns) |
| `features/mining_tenements_ml.csv` | StandardScaler-scaled ML-ready features (23 columns) |
| `features/scaler.pkl` | Fitted StandardScaler for transform/reproduction |
| `prepare_dataset.py` | End-to-end data preparation pipeline |
| `metadata.json` | Full dataset metadata and column descriptions |
| `DATA_PREPARATION_PROCESS.md` | Detailed documentation of cleaning & transformation steps |

## Columns (Processed Dataset)

| Column | Type | Description |
|--------|------|-------------|
| `holdercnt` | numeric | Number of tenement holders |
| `legal_area` | numeric | Legal area in hectares |
| `grantyear/month/day/dow/qtr` | int | Date features from grant date |
| `startyear/month/day/dow/qtr` | int | Date features from start date |
| `endyear/month/day/dow/qtr` | int | Date features from end date |
| `is_live` | binary (0/1) | **Target**: 1 if tenement is LIVE, 0 otherwise |
| `type_*` | binary | One-hot encoded tenement type |
| `survstatus_*` | binary | One-hot encoded survey status |
| `fmt_tenid_freq` | float | Frequency-encoded tenement ID |

## Usage

```python
import pandas as pd

# Load cleaned data
df = pd.read_csv("processed/mining_tenements_clean.csv")

# Load ML-ready features with target
ml_df = pd.read_csv("features/mining_tenements_ml.csv")
X = ml_df.drop(columns=["is_live"])
y = ml_df["is_live"]
```

## Requirements
- Python 3.9+
- pandas
- numpy
- scikit-learn

## License
Creative Commons Attribution 4.0 International (CC BY 4.0)
