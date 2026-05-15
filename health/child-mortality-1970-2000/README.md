# Child Mortality Dataset — Sex Ratios & Mortality Rates (1970s-2000s)

## Overview
This dataset contains sex ratios and levels of infant, child and under-five mortality for countries across four decades (1970s, 1980s, 1990s, 2000s). It provides mortality rates disaggregated by sex and the sex ratios of mortality, enabling analysis of gender disparities in child survival.

## Source
- **Title**: Table S2 — Sex ratios and levels of infant, child and under-five mortality for countries, 1970s-2000s
- **Source**: United Nations, World Population Prospects: The 2010 Revision; UNICEF, State of the World's Children 2012
- **Access**: UN Population Division — https://www.un.org/development/desa/pd/
- **License**: UN Data — Free use with attribution

## Dataset Contents

### Raw Data
- `raw/Table_S2.xls` — Original Excel file
- Contains 2 sheets: (1) Table S2-Methods and results (main data), (2) Notes to Table S2 (explanatory notes)

### Processed Data
- `processed/child_mortality_clean.csv` — Cleaned dataset with engineered features (579 rows × 34 columns)

### ML-Ready Data
- `features/X_train_scaled.csv` — Scaled training features (463 × 28)
- `features/X_test_scaled.csv` — Scaled test features (116 × 28)
- `features/y_train.csv` — Training target (u5mr_both — under-five mortality rate)
- `features/y_test.csv` — Test target
- `features/scaler.pkl` — Fitted StandardScaler

## Key Columns

| Column | Description |
|--------|-------------|
| `iso_code` | ISO country code |
| `country` | Country or area name |
| `decade` | Decade label (1970s, 1980s, 1990s, 2000s) |
| `decade_num` | Decade as integer (1970, 1980, 1990, 2000) |
| `sex_ratio_infant` | Sex ratio of infant mortality (male/female × 100) |
| `sex_ratio_child` | Sex ratio of child mortality (male/female × 100) |
| `sex_ratio_under5` | Sex ratio of under-five mortality (male/female × 100) |
| `imr_male` / `imr_female` / `imr_both` | Infant mortality rate (deaths <1yr per 1000 live births) |
| `cmr_male` / `cmr_female` / `cmr_both` | Child mortality rate (deaths age 1-4 per 1000) |
| `u5mr_male` / `u5mr_female` / `u5mr_both` | Under-five mortality rate (deaths <5yr per 1000 live births) |
| `infant_child_ratio` | Ratio of infant to child mortality |
| `under5_child_ratio` | Ratio of under-five to child mortality |
| `imr_sex_gap` | Sex gap in infant mortality (male - female) |
| `u5mr_sex_gap` | Sex gap in under-five mortality (male - female) |
| `has_trend` | Whether trend estimates are reliable (1=Y, 0=N) |
| `method` | Estimation method (Loess, Linear, Average) |
| `region` | Geographic region |

## ML Use Cases
- **Regression**: Predict under-five mortality rate from decade, sex ratios, and derived features
- **Classification**: High/low mortality country classification
- **Time-series analysis**: Mortality trends across decades by region
- **Gender disparity analysis**: Predict sex ratio gaps based on development indicators

## Data Cleaning Applied
1. Parsed structured Excel data, removing header rows
2. Standardized column names to lowercase with underscores
3. Filled 12 missing values (Angola etc.) with median
4. Capped outliers using IQR method (1.5× IQR bounds)
5. Encoded decade as numeric
6. Derived features: mortality ratios, sex gaps, region groups

## Requirements
- pandas, numpy, scikit-learn

## Reproducibility
```bash
cd datasets/health/child-mortality-1970-2000
python3 prepare_dataset.py
```
