# SEIFA Australia — Socio-Economic Indexes for Areas (1996-2021)

## Overview
Annual SEIFA data for **59,421 Statistical Area 1 (SA1) regions** across Australia, from 1996 to 2021. Contains **1.54 million rows** covering four socioeconomic indexes with score, rank, decile, and percentile for each.

## Source
- **Source**: Australian Bureau of Statistics (ABS)
- **Website**: https://www.abs.gov.au/statistics/people/people-communities/socio-economic-indexes-areas-seifa
- **License**: © Commonwealth of Australia, CC BY 4.0

## Indexes

| Index | Full Name | Description |
|-------|-----------|-------------|
| **IRSD** | Index of Relative Socio-economic Disadvantage | Measures disadvantage (low score = more disadvantaged) |
| **IER** | Index of Economic Resources | Measures economic resources (income, housing) |
| **IEO** | Index of Education and Occupation | Measures education and occupational skills |
| **IRSAD** | Index of Relative Socio-economic Advantage and Disadvantage | Measures both advantage and disadvantage (available from 2001) |

Each index has four metrics: **Score**, **Rank**, **Decile** (1-10), and **Percentile**.

## Dataset Contents

### Raw Data
- `raw/Annual_SEIFA_data_1996_to_2021.xlsx` — Original ABS Excel (200 MB, 12 sheets)

### Processed Data
- `processed/seifa_1996_2021_clean.csv` — Cleaned dataset (1,539,779 × 25, 337 MB)

### ML-Ready Data
- `features/X_train_scaled.csv` — Scaled training features (1,231,823 × 27)
- `features/X_test_scaled.csv` — Scaled test features (307,956 × 27)
- `features/y_train.csv` — Training target (irsd_score)
- `features/y_test.csv` — Test target
- `features/scaler.pkl` — Fitted StandardScaler

## Key Columns

| Column | Description |
|--------|-------------|
| `sa1_code` | Statistical Area 1 code |
| `year` | Year (1996-2021) |
| `state_name` | State or territory name |
| `irsd_score` / `ier_score` / `ieo_score` / `irsad_score` | Index scores |
| `irsd_decile` / `ier_decile` / `ieo_decile` / `irsad_decile` | Decile (1-10) |
| `irsd_percentile` | Percentile rank |
| `composite_advantage` | Mean of all 4 index scores |
| `ieo_ier_gap` | Education minus Economic Resources score |
| `irsd_tier` | Disadvantaged / Middle / Advantaged |

## ML Use Cases
- **Regression**: Predict socioeconomic disadvantage scores
- **Classification**: Socioeconomic tier prediction
- **Time-series**: Socioeconomic trends over 25 years
- **Geospatial**: Regional inequality analysis

## Data Notes
- IRSAD was introduced in 2001 (missing pre-2001 values filled with yearly medians)
- ~5,000 SA1 areas with missing core scores removed
- 59,421 unique SA1 areas tracked annually

## Reproducibility
```bash
cd datasets/socioeconomic/seifa-1996-2021
python3 prepare_dataset.py
```
