# Data Preparation: Human Activity Recognition

**Dataset:** Human Activity Recognition Using Smartphones (UCI HAR)
**Source:** UCI Machine Learning Repository
**License:** CC BY 4.0

## Raw Data

30 subjects (19-48 years old) each wore a Samsung Galaxy S II on their waist while performing six activities. The embedded accelerometer and gyroscope captured 3-axis linear acceleration and 3-axis angular velocity at 50 Hz.

Each window is 2.56 seconds (128 readings) with 50% overlap. From each window, 561 time and frequency domain features were extracted.

**Raw files:**
- `UCI HAR Dataset.zip` — contains train/test splits, features.txt, activity_labels.txt
- `UCI HAR Dataset.names` — metadata and citation info

## Pipeline Steps

1. **Extract** — zip extracted to temp directory
2. **Load features** — 561 feature names from `features.txt` (477 unique after dedup)
3. **Load labels** — map activity IDs to names
4. **Merge splits** — combine train (7,352) and test (2,947) into one dataframe (10,299 x 565)
5. **Clean** — no missing values, no duplicates to remove. Standardized column names to lowercase with underscores
6. **ML prep** — dropped identifier columns (subject_id, activity_id, split), label-encoded activity_name, stratified 80/20 train-test split, StandardScaler on features

## Cleaning Applied

- Column names normalized to lowercase with underscores
- Duplicate rows checked: none found
- Missing values checked: none found (pre-processed sensor data)

## Feature Engineering

No additional features created. The 561 feature vector is already engineered from raw sensor signals:

- Time domain: mean, standard deviation, median absolute deviation, max, min, signal magnitude area, energy, entropy, autoregression coefficients, correlation, etc.
- Frequency domain (FFT): mean frequency, skewness, kurtosis, energy bands, angle between vectors
- Three-axis signals: body acceleration, gravity acceleration, body angular velocity

## ML Ready Files

| File | Shape | Purpose |
|------|-------|---------|
| `X_train_scaled.csv` | 8,239 x 561 | Training features (scaled) |
| `X_test_scaled.csv` | 2,060 x 561 | Test features (scaled) |
| `y_train.csv` | 8,239 x 1 | Training labels (encoded 0-5) |
| `y_test.csv` | 2,060 x 1 | Test labels (encoded 0-5) |
| `scaler.pkl` | — | Fitted StandardScaler |
| `label_encoder.pkl` | — | Fitted LabelEncoder |

## Targets

6 activity classes: LAYING (0), SITTING (1), STANDING (2), WALKING (3), WALKING_DOWNSTAIRS (4), WALKING_UPSTAIRS (5)
