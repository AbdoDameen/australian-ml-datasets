# Water Potability (Dataset #27)

**Domain:** Freshwater Ecology
**ML Task:** Binary Classification (Potable vs Not Potable)
**Source:** Kaggle

Water quality metrics for predicting drinking water safety. Based on 9 chemical properties measured across water samples.

## Quick Stats

| Metric | Value |
|--------|-------|
| Rows | 3,276 |
| Columns | 19 (9 original + 8 engineered + target) |
| Missing (original) | 1,434 across 3 columns |
| Class balance | 61% not potable, 39% potable |
| Baseline RF | 64.9% |

## Columns

**Water chemistry (9):** `ph`, `hardness`, `solids`, `chloramines`, `sulfate`, `conductivity`, `organic_carbon`, `trihalomethanes`, `turbidity`

**Engineered (8):** `salinity_index`, `organic_load`, `hardness_conductivity_ratio`, `ph_acidic`, `ph_slightly_acidic`, `ph_neutral`, `ph_slightly_alkaline`, `ph_alkaline`

**Target:** `potability` — 0 (not potable), 1 (potable)

## Usage

```python
import pandas as pd

df = pd.read_csv("processed/water_potability_clean.csv")
X = df.drop("potability", axis=1)
y = df["potability"]
```

## Notes

- 15% of pH values and 24% of sulfate values were missing — imputed with median
- Water potability is a hard problem with basic chemical assays; this dataset is useful for feature engineering demos and showing the limits of shallow models
- 92.5% of the missing sulfate values occur in non-potable samples — not random
