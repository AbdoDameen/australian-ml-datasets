# Australian Car Market Dataset

## Overview

The **Australian Car Market** dataset contains listings of used and new cars for sale in the Australian market. It includes detailed specifications, pricing, and condition information for over 17,000 vehicles across 59 brands.

## Source

Raw data sourced from Australian automotive classifieds. See `DATA_PREPARATION_PROCESS.md` for the full data lineage and preparation methodology.

## Dataset Structure

```
australia-car-market/
├── raw/
│   └── australian_car_market_clean.csv     # Raw source data (17,048 rows)
├── processed/
│   ├── australian_car_market_clean_processed.csv      # Cleaned & feature-enhanced data
│   ├── australian_car_market_clean_processed.parquet  # Same data in Parquet format
│   └── summary.json                                    # Summary statistics
├── features/
│   ├── ml_features.csv             # Ready-to-use ML feature matrix
│   ├── ml_features.parquet         # Same in Parquet format
│   ├── scaler_params.json          # StandardScaler parameters (mean, std)
│   └── feature_names.json          # Column definitions
├── prepare_dataset.py              # Pipeline script
├── README.md                       # This file
├── DATA_PREPARATION_PROCESS.md     # Data preparation documentation
└── metadata.json                   # Dataset metadata
```

## Columns

| Column            | Type      | Description                                  |
|-------------------|-----------|----------------------------------------------|
| id                | int       | Unique listing identifier                    |
| brand             | str       | Vehicle manufacturer                         |
| model             | str       | Vehicle model name                           |
| variant           | str       | Trim/variant designation                     |
| series            | str       | Model series/chassis code                    |
| year              | int       | Manufacture year                             |
| decade            | str       | Derived decade (e.g., "2010s")               |
| price             | float     | Listed price in AUD                          |
| price_bracket     | str       | Price category (budget/economy/mid_range/premium/luxury) |
| kilometers        | float     | Odometer reading                             |
| odometer_category | str       | Odometer category (low/moderate/average/high/very_high) |
| type              | str       | Body type (Wagon, Sedan, Hatchback, etc.)    |
| gearbox           | str       | Transmission type (Automatic, Manual)        |
| fuel              | str       | Fuel type (Diesel, Unleaded Petrol, etc.)    |
| status            | str       | Condition (Used, Demo, New In Stock)         |
| cc                | float     | Engine capacity (cubic centimeters)          |
| color             | str       | Exterior colour                              |
| seating_capacity  | int       | Number of seats                              |

## ML Features

The `features/` directory contains a standardised feature matrix ready for machine learning:

- **17 feature columns**: scaled numeric features + one-hot encoded categoricals
- **Target**: `price` (regression task)
- **Preprocessing**: StandardScaler (z-score normalisation) applied to numeric features
- **Format**: CSV and Parquet (Apache Parquet for efficient storage/loading)

### Feature Engineering

| Feature                | Type    | Description                              |
|------------------------|---------|------------------------------------------|
| year_scaled            | numeric | Year (z-score normalised)                |
| kilometers_scaled      | numeric | Odometer reading (z-score normalised)    |
| cc_scaled              | numeric | Engine capacity (z-score normalised)     |
| seating_capacity_scaled| numeric | Seats (z-score normalised)               |
| decade_*               | binary  | One-hot encoded decade                   |
| gearbox_*              | binary  | One-hot encoded transmission             |
| fuel_*                 | binary  | One-hot encoded fuel type                |
| status_*               | binary  | One-hot encoded condition status         |

## Quick Start

```python
import pandas as pd

# Load cleaned dataset
df = pd.read_parquet("processed/australian_car_market_clean_processed.parquet")

# Load ML-ready features
X = pd.read_parquet("features/ml_features.parquet")
```

## Statistics

- **Total records**: 17,048
- **Unique brands**: 59
- **Price range**: $1,000 – $999,000 (median $29,990)
- **Year range**: 1989 – 2022
- **Odometer range**: 1 – 2,700,000 km

## License

See `metadata.json` for licensing information.
