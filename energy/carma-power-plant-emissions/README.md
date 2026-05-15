# CARMA Australia Power Plant Emissions Dataset (2000, 2007, Future)

## Overview
CO2 emissions data for **481 Australian power plants** across three time periods, sourced from the Carbon Monitoring for Action (CARMA) project. Includes plant-level carbon emissions (short tons), energy output (MWh), and carbon intensity (lbs CO2/MWh).

## Source
- **Dataset**: CARMA, Australia Power Plant Emissions
- **Source**: Carbon Monitoring for Action — http://carma.org/region/detail/18
- **Citation**: carma.org — Carbon Monitoring for Action
- **Published**: November 15, 2007
- **License**: CARMA public data — Free use with attribution

## Dataset Contents

### Raw Data
- `raw/CARMA_Australia_Power_Plant_Emissions.pdf` — Original GeoJSON-embedded PDF

### Processed Data
- `processed/carma_australia_emissions_clean.csv` — Cleaned dataset (481 × 53)

### ML-Ready Data
- `features/X_train_scaled.csv` — Scaled training features (384 × 43)
- `features/X_test_scaled.csv` — Scaled test features (97 × 43)
- `features/y_train.csv` — Training target (carbon_2007)
- `features/y_test.csv` — Test target
- `features/scaler.pkl` — Fitted StandardScaler

## Key Columns

| Column | Description |
|--------|-------------|
| `name` | Power plant name |
| `plant_id` | Unique plant identifier (from CARMA) |
| `company_id` | Operating company |
| `parentcomp_id` | Parent company |
| `city_name` | City location |
| `state` | State / territory |
| `latitude`, `longitude` | Plant coordinates |
| `carbon_2000`, `carbon_2007`, `carbon_nextdecade` | CO2 emissions (short tons) |
| `energy_2000`, `energy_2007`, `energy_nextdecade` | Electricity produced (MWh/year) |
| `intensity_2000`, `intensity_2007`, `intensity_nextdecade` | Carbon intensity (lbs CO2/MWh) |
| `is_renewable` | Zero-emission plant flag |
| `carbon_change_2000_2007` | CO2 change (short tons) |

## ML Use Cases
- **Regression**: Predict CO2 emissions from plant characteristics and location
- **Classification**: Renewable vs fossil fuel classification
- **Time-series**: Emission trends 2000 → 2007 → Future projections
- **Geospatial**: Spatial analysis of emission hotspots across Australia

## Data Cleaning Applied
1. Extracted GeoJSON from PDF source
2. Cleaned plant/company names (PDF concatenation artifacts)
3. Created state codes and geographic regions
4. Classified renewable vs fossil fuel plants
5. Capped outliers using IQR method
6. Engineered temporal change features
7. One-hot encoded states, regions, intensity and size categories

## Reproducibility
```bash
cd datasets/energy/carma-power-plant-emissions
python3 prepare_dataset.py
```
