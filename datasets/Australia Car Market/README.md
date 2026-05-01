# 🚗 Australia Car Market

## Overview
This dataset contains records of cars from the Australian car market provided by the user. It includes attributes such as car ID, name, price, brand, model year, gearbox, body type, fuel type, condition, mileage (kilometers), engine displacement (CC), color, and seating capacity.

## Source
- User-provided CSV (original path in notebook: `/content/cars_info.csv`)

## Files in this folder
```
datasets/Australia Car Market/
├── raw/
│   └── cars_info.csv               # (Place the original CSV here)
├── processed/
│   └── car_market_clean.csv        # (created after running the notebook)
├── features/                       # (Optional) ML-ready files
├── Australia_Car_Market.ipynb
└── metadata.json
```

## Processing summary
- Column names standardized to `snake_case` and lowercase
- Duplicate rows removed (if present)
- Numeric missing values imputed with median
- Categorical missing values imputed with mode or 'Unknown'
- Basic outlier handling (IQR) where applicable

## How to run
1. Place the original `cars_info.csv` in the `raw/` folder.
2. Open and run the `Australia_Car_Market.ipynb` notebook. It loads from `raw/cars_info.csv` by default and writes outputs to `processed/` and `features/`.

## Usage example
```python
import pandas as pd
df = pd.read_csv('datasets/Australia Car Market/processed/car_market_clean.csv')
print(df.head())
```

## License & Citation
Original data licensing depends on the source of the CSV. Cite the original provider when redistributing.

---

_Generated and maintained as part of the australian-ml-datasets repository._
