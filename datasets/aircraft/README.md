# 🇦🇺 Australian Aircraft Register (ACRFTREG)

## Overview
This dataset is derived from the Civil Aviation Safety Authority (CASA) Australian Aircraft Register and contains information about registered aircraft in Australia. This repository contains a processing notebook and cleaned dataset ready for analysis.

## Source
- Civil Aviation Safety Authority (CASA)
- Original data (CSV): https://services.casa.gov.au/CSV/acrftreg.csv

## Files in this folder

```
datasets/aircraft/
├── raw/
│   └── acrftreg.csv               # (Place the original CSV here)
├── processed/
│   └── aircraft_register_clean.csv
├── features/                      # (Optional) ML-ready files
├── Australian_Aircraft_Register.ipynb
└── metadata.json
```

## Processing summary
- Column names standardized to `snake_case` and lowercase
- Duplicate rows removed (if present)
- Numeric missing values imputed with median
- Categorical missing values imputed with mode or labeled `Unknown`
- Outliers removed using IQR method where applicable

## How to run
1. Place the original `acrftreg.csv` in the `raw/` folder.
2. Open and run the `Australian_Aircraft_Register.ipynb` notebook. It loads from `raw/acrftreg.csv` by default and writes outputs to `processed/` and `features/`.

## Usage examples
```python
import pandas as pd
df = pd.read_csv('datasets/aircraft/processed/aircraft_register_clean.csv')
print(df.head())
```

## License & Citation
Original data copyright: Commonwealth of Australia (CASA).
If you redistribute, follow the CASA terms and cite the original source.

---

_Generated and maintained as part of the australian-ml-datasets repository._
