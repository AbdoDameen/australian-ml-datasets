# Forest Cover Type — Data Preparation Process

## Source

UCI ML Repository: https://archive.ics.uci.edu/dataset/31/covertype  
Citation: Blackard, J.A. & Dean, D.J. (1999). Comparative accuracies of artificial neural networks and discriminant analysis in predicting forest cover types from cartographic variables.

## Raw Data

The raw file `covtype.data` is in UCI `.data` format — comma-separated, no header, 54 features + 1 target. Single-letter codes with `?` for missing values (none found in this dataset).

**Column structure:**
- Columns 1–10: Quantitative (elevation, aspect, slope, hydrology distances, hillshade, fire points)
- Columns 11–14: Binary wilderness area indicators (4 types)
- Columns 15–54: Binary soil type indicators (40 types)
- Column 55: Cover type target (1–7)

## Cleaning

- Removed duplicate rows (none found — the raw covtype.data has 581,012 unique rows)
- No missing values present in the dataset
- No outlier removal needed — cartographic data is discrete and already validated

## Feature Engineering

Added 12 derived features:

1. **elevation_slope** — interaction between elevation and slope
2. **horiz_vert_hydrology_ratio** — horizontal/vertical hydrology distance ratio (clipped 0–1000)
3. **avg_hillshade** — mean hillshade across 9am, noon, 3pm
4. **hillshade_range** — hillshade range (max − min)
5. **total_hydrology_distance** — horizontal + vertical hydrology distance
6. **near_water** — binary: within 100m horizontal or 20m vertical of water
7. **near_road** — binary: within 100m of roadway
8. **near_fire** — binary: within 500m of wildfire ignition point
9. **northness** — cos(aspect) in radians
10. **eastness** — sin(aspect) in radians
11. **wilderness_count** — number of wilderness areas present per cell
12. **soil_count** — number of soil types present per cell

Total features: 10 quantitative + 44 binary + 12 derived = **68 features**

## ML Preparation

- **Train/test split:** 80/20 stratified by cover type (preserves class proportions)
- **Target encoding:** LabelEncoder (7 classes)
- **Scaling:** StandardScaler fit on training, transform both
- **Output:** X_train_scaled (464,809 × 68), X_test_scaled (116,203 × 68), y_train, y_test, scaler.pkl, label_encoder.pkl

## Target Distribution

| Class | Name | Count | % |
|-------|------|------:|---:|
| 1 | Spruce/Fir | 211,840 | 36.5% |
| 2 | Lodgepole Pine | 283,301 | 48.8% |
| 3 | Ponderosa Pine | 35,754 | 6.2% |
| 4 | Cottonwood/Willow | 2,747 | 0.5% |
| 5 | Aspen | 9,493 | 1.6% |
| 6 | Douglas-fir | 17,367 | 3.0% |
| 7 | Krummholz | 20,510 | 3.5% |

Imbalanced — Spruce/Fir and Lodgepole Pine make up 85% of samples.
