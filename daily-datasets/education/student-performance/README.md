# Student Performance

**Predict final grades from demographics, social factors, and study habits.**

Two Portuguese secondary schools — 1,044 students across Math (395) and Portuguese (649) classes.  

**Source:** [UCI ML Repository](https://archive.ics.uci.edu/dataset/320/student+performance)  
**License:** CC BY 4.0  
**Target:** `g3` — final grade (0–20, regression)

## Structure

```
education/student-performance/
├── raw/           # student-mat.csv, student-por.csv (semicolon-delimited)
├── processed/     # student-performance_clean.csv (combined, cleaned, features engineered)
├── features/      # ML-ready: scaled train/test splits + scaler
├── prepare_dataset.py   # Reproducible pipeline
└── metadata.json        # Column descriptions, shape, transforms
```

## Key Stats

| Metric | Value |
|--------|-------|
| Total students | 1,044 |
| Math / Portuguese | 395 / 649 |
| Features (after encoding) | 68 |
| Target range | 0–20 |
| Mean G3 | 11.34 |

## Quick Start

```python
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

X_train = pd.read_csv('features/X_train_scaled.csv')
y_train = pd.read_csv('features/y_train.csv').squeeze()
X_test = pd.read_csv('features/X_test_scaled.csv')
y_test = pd.read_csv('features/y_test.csv').squeeze()

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print(f'MAE: {mean_absolute_error(y_test, preds):.2f}')
```

## Features

**Demographic:** school, sex, age, address, family size, parents' cohabitation, parents' education & jobs  
**Social:** reason for school choice, guardian, travel time, study time, past failures, extracurriculars  
**Health & Habits:** alcohol consumption (workday/weekend), going out, free time, health status, absences  
**Academic:** G1 & G2 (period grades), engineered grade changes & performance tiers  
**Target:** G3 — final grade
