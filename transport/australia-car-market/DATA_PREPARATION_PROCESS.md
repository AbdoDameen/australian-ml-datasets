# Data Preparation Process — Australian Car Market

## 1. Source Data

**File**: `raw/australian_car_market_clean.csv`

The raw dataset was collected from Australian automotive classifieds. It contains 17,048 listings with 16 attributes covering vehicle specifications, pricing, and condition.

## 2. Cleaning Steps

### 2.1 Numeric Field Parsing

- **Price**: Strips `$`, commas, handles `"POA"` (Price On Application) and empty values. Entries < $500 are treated as invalid and the row is dropped.
- **Kilometers (Odometer)**: Strips "km" suffix, commas, whitespace. Range validation: 1–3,000,000 km.
- **Year**: Parsed as integer, validated to range 1950–2025.
- **Engine Capacity (cc)**: Range validation: 500–10,000 cc.
- **Seating Capacity**: Range validation: 1–20 seats.

### 2.2 Categorical Cleaning

- **Brand**: Title-cased, with normalisation of common variants (e.g., "Merc-Benz" → "Mercedes-Benz").
- **Colour**: Title-cased and mapped to standard colour names (White, Black, Silver, Grey, Blue, Red, Green, etc.).
- **Gearbox/Fuel/Status/Type**: Whitespace stripped, title-cased.

### 2.3 Row Filtering

Rows are **dropped** if:
- `price` is missing, empty, or "$0" (96 rows dropped)
- `year` is missing or outside valid range (13 rows dropped)

**Total dropped**: ~109 rows (~0.6% of data).

## 3. Feature Engineering

### 3.1 Derived Features

| Feature             | Derivation                                           |
|---------------------|------------------------------------------------------|
| `decade`            | Year → decade bin (e.g., 2016 → "2010s")            |
| `price_bracket`     | Price → category: budget (<$15K), economy ($15–30K), mid-range ($30–50K), premium ($50–80K), luxury ($80K+) |
| `odometer_category` | Odometer → category: low (<20K), moderate (20–60K), average (60–120K), high (120–200K), very_high (200K+) |

### 3.2 ML Feature Encoding

Numeric features (`year`, `kilometers`, `cc`, `seating_capacity`) are **z-score normalised** (StandardScaler):
- `x_scaled = (x - mean) / std`

Categorical features are **one-hot encoded**:
- **decade**: 5 binary columns (1980s, 1990s, 2000s, 2010s, 2020s)
- **gearbox**: 2 binary columns (Automatic, Manual)
- **fuel**: 5 binary columns (Diesel, Premium Unleaded Petrol, Unleaded Petrol, Premium Unleaded/Electric, Unleaded Petrol/Electric)
- **status**: 3 binary columns (Demo, New In Stock, Used)

**Total**: 17 ML features + 1 target (`price`).

## 4. Output Files

| Directory    | File                              | Description                                |
|-------------|-----------------------------------|--------------------------------------------|
| `processed/` | `*_processed.csv`                | Cleaned data with derived features         |
| `processed/` | `*_processed.parquet`            | Parquet format (if pandas/pyarrow available)|
| `processed/` | `summary.json`                   | Dataset statistics                         |
| `features/`  | `ml_features.csv`                | ML-ready feature matrix (CSV)              |
| `features/`  | `ml_features.parquet`            | ML-ready feature matrix (Parquet)          |
| `features/`  | `scaler_params.json`             | Mean & std for each scaled numeric feature |
| `features/`  | `feature_names.json`             | List of all feature columns + target name  |

## 5. Reproducibility

To re-run the pipeline:

```bash
cd datasets/transport/australia-car-market/
python3 prepare_dataset.py
```

The pipeline is deterministic (seeded random operations where applicable).

## 6. Data Quality Notes

- The dataset has a strong bias toward used cars (96% of listings).
- Top 5 brands (Toyota, Holden, Ford, Mazda, Hyundai) account for ~47% of all listings.
- Wagon body type dominates (46% of listings).
- Automatic transmission vehicles are ~86% of the market.
- Colour distribution is skewed: White (36%), Silver (14%), Grey (14%), Black (12%).
- Some extreme values exist: max odometer 2,700,000 km, max price $999,000 — these are kept as legitimate outliers.
