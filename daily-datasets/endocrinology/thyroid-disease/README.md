# Thyroid Disease (Dataset #20)

**Domain:** Endocrinology  
**ML Task:** Classification (3-class — normal, hyperfunction, subnormal)  
**Source:** UCI ML Repository / Garavan Institute, Sydney  

Thyroid disease classification records from the Garavan Institute, originally contributed by Ross Quinlan and preprocessed by Randolf Werner (Daimler-Benz) for backpropagation benchmarking. The goal is to determine whether a patient referred to the clinic has normal thyroid function, hyperfunction, or subnormal functioning (hypothyroid).

## Quick Stats

| Metric | Value |
|--------|-------|
| Rows | 7,200 |
| Columns | 24 (21 original + 2 engineered + class) |
| Missing values | 0 |
| Class balance | 92.6% normal, 5.1% hyperfunction, 2.3% subnormal |

## Columns

**Continuous (6):** `age`, `tsh`, `t3`, `tt4`, `t4u`, `fti` — all normalised to [0, 1].

**Binary (15):** `sex`, `on_thyroxine`, `query_on_thyroxine`, `on_antithyroid_medication`, `thyroid_surgery`, `query_hypothyroid`, `query_hyperthyroid`, `pregnant`, `sick`, `tumor`, `lithium`, `goitre`, `tsh_measured`, `t3_measured`, `tt4_measured` — all 0/1.

**Engineered (2):** `tsh_t3_ratio`, `calculated_fti`.

**Target:** `thyroid_class` — 1 (normal), 2 (hyperfunction), 3 (subnormal).

## Usage

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("processed/thyroid_disease_clean.csv")
X = df.drop("thyroid_class", axis=1)
y = df["thyroid_class"]

# Or use pre-scaled ML-ready files:
X_train = np.loadtxt("features/X_train_scaled.csv", delimiter=",")
y_train = np.loadtxt("features/y_train.csv")
```

## Baseline

Random Forest (100 trees) achieves **99.7% accuracy** on the 20% test set.

## Notes

- The raw data (`ann-train.data`, `ann-test.data`) is pre-normalised by the donor — all continuous values are in [0, 1], making this dataset ready for neural network training without additional scaling (though StandardScaler is included for compatibility).
- 92.6% majority class — a naive classifier guessing "subnormal" scores 92.6%.
- This is the ANN (artificial neural network) benchmark subset of the larger UCI Thyroid Disease collection.
