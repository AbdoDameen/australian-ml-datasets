# Beijing Air Quality

**Domain:** Environmental  
**ML Task:** Regression (PM2.5 concentration forecasting)  
**Source:** UCI Machine Learning Repository  
**License:** CC BY 4.0  

Hourly PM2.5 and meteorological data from the US Embassy in Beijing, Jan 2010–Dec 2014. 43K+ hourly records.

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original PRSA CSV from UCI |
| `processed/` | Cleaned + feature-engineered data |
| `features/` | ML-ready scaled train/test splits |
| `prepare_dataset.py` | Reproducible pipeline |

## Columns

| Column | Description |
|--------|-------------|
| `pm2_5` | Target — PM2.5 concentration (µg/m³) |
| `year`, `month`, `day`, `hour` | Timestamp components |
| `dewp` | Dew point (°C) |
| `temp` | Temperature (°C) |
| `pres` | Atmospheric pressure (hPa) |
| `iws` | Cumulated wind speed (m/s) |
| `is` | Hours of snow |
| `ir` | Hours of rain |
| `wind_*` | One-hot encoded wind direction (NE/NW/SE/cv) |
| `dayofweek`, `quarter`, `season` | Calendar features |
| `is_weekend` | Weekend flag |

## Usage

```bash
cd daily-datasets/environmental/beijing-air-quality
python3 prepare_dataset.py
```
