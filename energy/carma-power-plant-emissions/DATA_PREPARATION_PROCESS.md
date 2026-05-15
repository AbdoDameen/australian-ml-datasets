# Data Preparation Process — CARMA Australia Power Plant Emissions

## Objective
Extract, clean, and prepare the CARMA Australia Power Plant Emissions dataset for machine learning applications — covering 481 power plants across 2000, 2007, and projected future emissions.

## Methodology
CRISP-DM framework

## Step-by-Step Process

### 1. Data Extraction
- **Source**: CARMA.org (Carbon Monitoring for Action)
- **Format**: GeoJSON embedded within a PDF file
- **Method**: Extracted raw text from PDF using pdftotext, cleaned control characters, parsed as JSON
- **Original Records**: 481 power plants, each with 19 property fields

### 2. Data Understanding
- **Coverage**: All Australian states and territories
- **Time Periods**: 2000 (Annual Report), 2007 (Present), Future (projected)
- **Plant Types**: 
  - 178 renewable (zero-emission) plants — 37%
  - 303 fossil fuel plants — 63%
- **Top States**: Western Australia (104), Queensland (95), NSW (97 total), Victoria (81)
- **Emissions Range**: 0 to 20.2M short tons CO2/year
- **Key Companies**: Western Power (20 plants), Ergon Energy (14), Power and Water Corp (14)

### 3. Data Cleaning
- **Name cleaning**: Fixed PDF concatenation artifacts in plant/company names
- **Duplicate check**: No duplicate plant_ids found
- **Missing values**: None in the original dataset
- **State standardization**: Created state_code abbreviations (NSW, QLD, VIC, etc.)
- **Outlier treatment**: IQR capping for carbon, energy, and intensity columns
  - 84-91 outliers capped per column (primarily large power stations)

### 4. Feature Engineering
| Feature | Type | Description |
|---------|------|-------------|
| `is_renewable` | Binary | Zero-emission plant |
| `intensity_category` | Categorical | low (<500), medium (500-1500), high (>1500) lbs/MWh |
| `size_category` | Categorical | zero, small, medium, large, mega |
| `carbon_change_*` | Numeric | CO2 change 2000→2007, 2007→Future |
| `energy_change_*` | Numeric | Energy change 2000→2007, 2007→Future |
| `carbon_growing/declining` | Binary | Emission trend flags |
| `is_high_emitter` | Binary | Above median CO2 emissions |
| `company_plants_count` | Numeric | Frequency encoding of company |
| `parent_plants_count` | Numeric | Frequency encoding of parent company |
| `region_*` | One-hot | Geographic region |
| `state_*` | One-hot | State/territory |

### 5. ML Preparation
- **Features**: 43 numeric features
- **Default Target**: carbon_2007 (CO2 emissions in short tons)
- **Split**: 80/20 train/test with random_state=42
- **Scaling**: StandardScaler (z-score normalization)
- **Train set**: 384 rows × 43 features
- **Test set**: 97 rows × 43 features

### 6. Result
- 481 power plants, 53 cleaned columns, 43 ML-ready features
- Zero missing values
- 178 renewable + 303 fossil fuel plants identified
- Full temporal coverage: 2000, 2007, Future projections

### 7. Files Created
| File | Description |
|------|-------------|
| `raw/CARMA_Australia_Power_Plant_Emissions.pdf` | Original CARMA dataset |
| `processed/carma_australia_emissions_clean.csv` | Cleaned dataset (53 columns) |
| `features/X_train_scaled.csv` | Scaled training features |
| `features/X_test_scaled.csv` | Scaled test features |
| `features/y_train.csv` | Training target |
| `features/y_test.csv` | Test target |
| `features/scaler.pkl` | Fitted StandardScaler |
| `metadata.json` | Dataset metadata |
| `README.md` | Dataset documentation |
| `DATA_PREPARATION_PROCESS.md` | This document |
| `prepare_dataset.py` | Reproducible pipeline |

## Reproducibility
```bash
cd datasets/energy/carma-power-plant-emissions
python3 prepare_dataset.py
```
