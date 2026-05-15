# Data Preparation Process — Mushroom Classification

## Source

UCI ML Repository: [Mushroom dataset](https://archive.ics.uci.edu/dataset/73/mushroom). Original data from *The Audubon Society Field Guide to North American Mushrooms* (1981).

## Ingestion

- Parsed `agaricus-lepiota.data` — a comma-separated file with 23 columns (class + 22 attributes), no header
- 8,124 rows, all categorical

## Cleaning

1. **Missing values**: Attribute #11 (stalk_root) had 2,480 entries marked `?`. Replaced with a new category "missing" instead of imputing — the missingness itself may carry signal
2. **Letter-to-name mapping**: All single-letter codes converted to human-readable names using the UCI .names file mappings
3. **Duplicates**: None found
4. **Constant columns**: veil_type had only one value (partial) — kept for completeness

## Feature Engineering

- **One-hot encoding** on all 22 categorical features (drop_first=False)
- 117 binary features total
- veil_type's single value produced 1 column (partial=1 for all rows) — constant, but kept

## ML Preparation

- **Target**: class_label (0 = edible, 1 = poisonous)
- **Split**: 80/20 stratified (maintains class balance)
- **Scaling**: StandardScaler on all 117 features
- **Output**: 6,499 train / 1,625 test samples

## Files Created

| Path | Size |
|------|------|
| `processed/mushroom_clean.csv` | 1.2 MB — human-readable categorical data |
| `processed/mushroom_encoded.csv` | 6.9 MB — one-hot encoded |
| `features/X_train_scaled.csv` | 3.9 MB |
| `features/X_test_scaled.csv` | 976 KB |
| `features/y_train.csv` | 28 KB |
| `features/y_test.csv` | 7 KB |
| `features/scaler.pkl` | 17 KB |
