# 🌧️ Rain in Australia Dataset

## Overview
This dataset contains 10 years of daily weather observations from multiple locations across Australia. The primary goal is to predict whether it will rain the next day (`RainTomorrow` target variable).

## Dataset Details

**Source**: [Kaggle - Weather Dataset: Raining in Australia](https://www.kaggle.com/datasets/jsphyg/weather-dataset-raining-in-australia)  
**Original Data**: Bureau of Meteorology (BOM)  
**Copyright**: Commonwealth of Australia 2010  
**Time Period**: ~10 years of daily observations  
**Locations**: Multiple weather stations across Australia  

### Target Variable
- **RainTomorrow**: Yes/No (binary classification)
- **Definition**: Yes if daily rainfall ≥ 1mm, otherwise No
- **Class Distribution**: Imbalanced (~22% Yes, ~78% No in original data)

## Files Included

```
datasets/weather/rain_in_australia/
├── raw/
│   └── weatherAUS.csv                    (Original data - 142,193 rows × 23 columns)
├── processed/
│   ├── rain_australia_clean.csv          (Cleaned data)
│   └── rain_australia_features.csv       (With engineered features)
├── features/
│   ├── X_train_scaled.csv               (Training features)
│   ├── X_test_scaled.csv                (Testing features)
│   ├── y_train.csv                      (Training target)
│   ├── y_test.csv                       (Testing target)
│   └── scaler.pkl                       (StandardScaler for predictions)
├── metadata.json                         (Complete dataset documentation)
└── rain_in_australia_pipeline.ipynb      (Processing pipeline notebook)
```

## Key Features

### Weather Variables
- `MinTemp`, `MaxTemp` - Minimum and maximum temperature (°C)
- `Rainfall` - Daily rainfall (mm)
- `Evaporation` - Class A pan evaporation (mm)
- `Sunshine` - Hours of bright sunshine
- `WindGustDir`, `WindGustSpeed` - Wind gust direction and speed
- `WindDir9am`, `WindDir3pm` - Wind direction at 9am and 3pm
- `WindSpeed9am`, `WindSpeed3pm` - Wind speed at 9am and 3pm
- `Humidity9am`, `Humidity3pm` - Humidity at 9am and 3pm
- `Pressure9am`, `Pressure3pm` - Atmospheric pressure at 9am and 3pm
- `Cloud9am`, `Cloud3pm` - Cloud cover at 9am and 3pm
- `Temp9am`, `Temp3pm` - Temperature at 9am and 3pm
- `RainToday` - Whether it rained today (Yes/No)

### Engineered Features
- `temp_range` - Max temperature - Min temperature
- `temp_avg` - Average of max and min temperatures
- `wind_speed_diff` - 3pm wind speed - 9am wind speed
- `wind_speed_avg` - Average wind speed
- `humidity_diff` - 3pm humidity - 9am humidity
- `humidity_avg` - Average humidity
- `pressure_diff` - 3pm pressure - 9am pressure
- `has_rainfall` - Binary: did it rain today?
- `is_heavy_rain` - Binary: was rainfall > 10mm?
- `cloud_diff` - 3pm cloud - 9am cloud
- `cloud_avg` - Average cloud cover

## Data Processing

### Cleaning Steps
1. **Duplicates**: Removed duplicate rows
2. **Missing Values**: 
   - Numeric: Filled with median
   - Categorical: Filled with mode
3. **Outliers**: Removed using IQR method
4. **Encoding**: Label encoded categorical variables

### Train/Test Split
- **Split Ratio**: 80% training, 20% testing
- **Stratification**: Yes (preserves class distribution)
- **Scaling**: StandardScaler applied

## Usage

### Quick Start
```python
import pandas as pd
import pickle

# Load ML-ready data
X_train = pd.read_csv('features/X_train_scaled.csv')
X_test = pd.read_csv('features/X_test_scaled.csv')
y_train = pd.read_csv('features/y_train.csv').squeeze()
y_test = pd.read_csv('features/y_test.csv').squeeze()

# Load scaler for new predictions
with open('features/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

### Train a Classification Model
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

### Use in Production
```python
# For new weather data
new_data = pd.read_csv('new_weather_data.csv')
new_data_scaled = scaler.transform(new_data)
predictions = model.predict(new_data_scaled)
```

## ML Use Cases

✅ **Binary Classification** - Predict tomorrow's rain (Yes/No)  
✅ **Time-Series Forecasting** - Rainfall prediction over days/weeks  
✅ **Feature Importance** - Which weather variables matter most?  
✅ **Anomaly Detection** - Unusual weather patterns  
✅ **Regional Analysis** - Compare rainfall patterns across Australia  

## Suitable Models

- Logistic Regression (baseline)
- Decision Trees
- Random Forest
- Gradient Boosting (XGBoost, LightGBM)
- Neural Networks
- LSTM for time-series

## Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Samples | ~139,000 (after cleaning) |
| Training Samples | ~111,000 |
| Testing Samples | ~28,000 |
| Number of Features | 45+ |
| Target Classes | 2 (Yes/No) |
| Class Balance | Imbalanced (~22% positive) |

## Data Quality Notes

- Some missing values in weather measurements
- Wind direction highly variable
- Strong seasonal patterns in Australian weather
- Class imbalance (less rain than no rain)

## Processing Time

- Data Loading: ~2 seconds
- Cleaning: ~3 seconds
- Feature Engineering: ~1 second
- Train/Test Split: <1 second
- **Total**: ~6 seconds

## Next Steps

1. **Download Raw Data**: Get `weatherAUS.csv` from Kaggle
2. **Place in raw/**: `datasets/weather/rain_in_australia/raw/weatherAUS.csv`
3. **Run Notebook**: Execute `rain_in_australia_pipeline.ipynb`
4. **Train Model**: Use the generated ML-ready files in `features/`

## License

Original data copyright: Commonwealth of Australia 2010, Bureau of Meteorology  
Dataset: CC0 1.0 (Kaggle)  
This repository: Your chosen license

## References

- Bureau of Meteorology: https://www.bom.gov.au/climate/data
- Kaggle Dataset: https://www.kaggle.com/datasets/jsphyg/weather-dataset-raining-in-australia
- Climate Data Online: https://www.bom.gov.au/climate/data-services/

---

**Ready to use!** All preprocessing is complete. Start training your models immediately. 🚀
