# 06 | Human Activity Recognition

10,299 samples of smartphone sensor data from 30 subjects doing 6 activities. 561 time/frequency features from a Samsung Galaxy S II accelerometer + gyroscope.

**Source:** UCI ML Repository — [Human Activity Recognition Using Smartphones](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones)

**Task:** Multi-class classification — predict which of 6 activities a subject is performing

## Data

30 subjects, waist-mounted Samsung Galaxy S II, 50 Hz sampling. Each window is 2.56 sec (128 readings) with 50% overlap.

**Activities:**

| Activity | Samples |
|----------|---------|
| LAYING | 1,944 |
| STANDING | 1,906 |
| SITTING | 1,777 |
| WALKING | 1,722 |
| WALKING_UPSTAIRS | 1,544 |
| WALKING_DOWNSTAIRS | 1,406 |

**Features:** 561 features across time domain (mean, std, mad, etc.) and frequency domain (FFT-derived). Pre-processed with noise filters and calibrated sensor signals.

## Files

| File | Description |
|------|-------------|
| `raw/` | Original UCI HAR Dataset.zip + .names |
| `processed/human_activity_recognition_clean.csv` | Merged train/test, cleaned, 10,299 x 565 |
| `features/` | 80/20 stratified split, StandardScaled, label encoded |
| `prepare_dataset.py` | Reproducible pipeline |
| `metadata.json` | Transformations, sensor specs, class mapping |

## Usage

```bash
cd daily-datasets/biophysics/human-activity-recognition
python3 prepare_dataset.py
```
