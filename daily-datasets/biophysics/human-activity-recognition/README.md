# Dataset #06: Human Activity Recognition

**Domain:** Biophysics
**ML Task:** Classification (6 classes)
**Source:** UCI Machine Learning Repository

30 subjects wearing a Samsung Galaxy S II on their waist, doing six activities while accelerometer and gyroscope data was recorded at 50 Hz. 561 features extracted from 2.56-second sliding windows with 50% overlap.

## Stats

| | |
|---|---|
| Samples | 10,299 |
| Features | 561 |
| Subjects | 30 |
| Activities | 6 |
| Train/Test | 7,352 / 2,947 (native splits) |
| Missing values | 0 |

## Activities

LAYING (1,944), STANDING (1,906), SITTING (1,777), WALKING (1,722), WALKING_UPSTAIRS (1,544), WALKING_DOWNSTAIRS (1,406)

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | UCI HAR Dataset.zip + .names file |
| `processed/` | Cleaned CSV with all 561 feature columns |
| `features/` | Scaled train/test splits + scaler + label encoder |
| `prepare_dataset.py` | End-to-end reproducible pipeline |
| `metadata.json` | Column descriptions, sources, parameters |

## Usage

```python
import pandas as pd
import pickle

X_train = pd.read_csv('features/X_train_scaled.csv')
X_test = pd.read_csv('features/X_test_scaled.csv')
y_train = pd.read_csv('features/y_train.csv')
y_test = pd.read_csv('features/y_test.csv')

with open('features/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('features/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)
```

6 activity classes: LAYING (0), SITTING (1), STANDING (2), WALKING (3), WALKING_DOWNSTAIRS (4), WALKING_UPSTAIRS (5)

## Pipeline

```bash
cd daily-datasets/biophysics/human-activity-recognition
python3 prepare_dataset.py
```

## Source

https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones
