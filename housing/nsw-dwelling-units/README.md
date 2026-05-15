# NSW Dwelling Units Dataset

**Number of dwelling units approved by sector, building type, and series type — New South Wales, Australia**

This dataset is a metadata index of ABS time series tracking dwelling unit approvals in NSW. Each row represents one data series identified by a unique Series ID, with information about building type, sector, series type, and temporal coverage.

## Source

- **Australian Bureau of Statistics (ABS)** — Building Approvals Australia
- https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release#data-downloads

## Dataset Structure

| Field | Description |
|-------|-------------|
| `series_id` | Unique ABS series identifier (e.g., A418458A) |
| `series_type` | Original, Seasonally Adjusted, or Trend |
| `building_type` | Houses, Dwellings excluding houses, or Total (Type of Building) |
| `sector` | Private Sector or Total Sectors |
| `start_year` / `end_year` | Temporal coverage of the series |
| `start_decade` | Decade of series start (1980s–2020s) |
| `series_span_years` | Duration of series in years |
| `no_obs` | Number of observations in the series |

## Files

| File | Description |
|------|-------------|
| `raw/nsw_dwelling_units_clean.csv` | Original cleaned CSV from ABS |
| `processed/nsw_dwelling_units_clean.csv` | Cleaned dataset with engineered features |
| `features/X_train_scaled.csv` | Scaled training features (80%) |
| `features/X_test_scaled.csv` | Scaled test features (20%) |
| `features/y_train.csv` | Training target (no_obs) |
| `features/y_test.csv` | Test target (no_obs) |
| `features/scaler.pkl` | Fitted StandardScaler pickle |
| `features/sector_mapping.csv` | Sector → encoded value mapping |
| `metadata.json` | Full metadata |
| `prepare_dataset.py` | Reproducible preparation script |

## ML Features

16 features including:
- `no_obs`, `collection_month` — raw numeric fields
- `start_decade_num`, `series_span_years`, `start_month` — time-based features
- `sector_encoded` — binary (Private=0, Total=1)
- `is_original`, `is_seasonally_adjusted`, `is_trend` — series type flags
- `prefix_freq` — frequency of series ID prefix
- One-hot encoded building type (3 columns)
- One-hot encoded era (3 columns: 2000s, 2010s, 2020s)

Target variable: `no_obs` (number of observations per series)

## License

ABS Data — Commonwealth of Australia. Free use with attribution.
