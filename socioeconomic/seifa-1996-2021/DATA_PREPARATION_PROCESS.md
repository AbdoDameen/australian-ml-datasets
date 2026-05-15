# Data Preparation Process — SEIFA Australia 1996-2021

## Objective
Clean, combine, and prepare the ABS SEIFA dataset — annual socioeconomic index data for 59,421 Australian SA1 regions across 26 years (1996-2021).

## Methodology
Sheet-by-sheet extraction → combine → clean → feature engineer → ML-ready

## Step-by-Step Process

### 1. Data Extraction
- **Source**: ABS Excel workbook (200 MB, 12 sheets)
- **Structure**: One sheet per state/territory (NSW, VIC, QLD, SA, WA, TAS, NT, ACT, OT + metadata)
- **Each sheet**: 18 columns — SA1 code, year, 4 indexes × 4 metrics each
- **Combined**: 1,544,946 rows from 9 state sheets

### 2. Data Understanding
| Metric | Value |
|--------|-------|
| SA1 Areas | 59,421 |
| Years | 1996-2021 (26 years) |
| States/Territories | 9 |
| Indexes | IRSD, IER, IEO, IRSAD |
| Missing (pre-2001 IRSAD) | 306,331 rows (19.8%) |

### 3. Data Cleaning
1. **Combined sheets**: Merged 9 state sheets into unified dataset
2. **Missing IRSAD**: 306,331 rows missing IRSAD (not available before 2001) — filled with yearly medians
3. **Missing core scores**: 5,167 rows removed (areas with no index data)
4. **Data types**: SA1 codes to int64, year to int
5. **Outlier treatment**: 3× IQR capping on index scores

### 4. Feature Engineering
| Feature | Description |
|---------|-------------|
| `census_year` | Flag for census years (1996, 2001, 2006, 2011, 2016, 2021) |
| `irsd_tier` | Socioeconomic tier (disadvantaged/middle/advantaged) |
| `composite_advantage` | Mean of all 4 index scores |
| `ieo_ier_gap` | Education minus Economic Resources score |
| `region` | Broader geographic grouping |
| `has_irsad` | IRSAD availability flag (post-2001) |

### 5. ML Preparation
- **Features**: 27 numeric features
- **Default Target**: irsd_score (socioeconomic disadvantage)
- **Split**: 80/20 train/test (1,231,823 / 307,956)
- **Scaling**: StandardScaler

### 6. Files Created
| File | Size | Description |
|------|------|-------------|
| `raw/Annual_SEIFA_data_1996_to_2021.xlsx` | 200 MB | Original ABS data |
| `processed/seifa_1996_2021_clean.csv` | 337 MB | Cleaned dataset |
| `features/X_train_scaled.csv` | Scaled training features |
| `features/X_test_scaled.csv` | Scaled test features |
| `features/y_train.csv` | Training target |
| `features/y_test.csv` | Test target |
| `features/scaler.pkl` | Fitted StandardScaler |

## Reproducibility
```bash
cd datasets/socioeconomic/seifa-1996-2021
python3 prepare_dataset.py
```
