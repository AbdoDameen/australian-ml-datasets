# Wine Quality — Vinho Verde (Dataset #52)

**Domain:** Oenology
**ML Task:** Regression — predict quality score (0-10)
**Source:** [UCI ML Repository](https://archive.ics.uci.edu/dataset/186/wine+quality) — Cortez et al., 2009

Physicochemical properties of Portuguese Vinho Verde wines, red and white variants combined. Quality is the median of at least 3 expert sensory ratings.

## Quick Stats

| Metric | Value |
|--------|-------|
| Rows | 6,497 raw → 5,320 cleaned (1,177 dupes removed) |
| Red / White | 1,599 / 4,898 |
| Features | 11 original + 9 engineered (27 after encoding) |
| Missing values | 0 |
| Quality range | 3-9 (median 6) |
| Split | 80/20 — 4,256 train / 1,064 test |

## Columns

**Physicochemical (11):** fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol

**Engineered (9):** total_acidity, fixed_to_volatile, so2_ratio, sweetness (dry/off_dry/medium/sweet), alcohol_band, is_high_alcohol, sugar_per_density, chlorides_per_alcohol, quality_label (≥7 = good, for classification use)

**Target:** quality (0-10)

## Usage

```python
import pandas as pd

df = pd.read_csv("processed/wine-quality-v2_clean.csv")
X = df.drop(columns=["quality", "quality_label"])
y = df["quality"]  # regression
```

## Notes

- Raw CSVs stay local (gitignored) — grab them from [UCI](https://archive.ics.uci.edu/dataset/186/wine+quality) and drop into `raw/` to re-run the pipeline
- Whites run sweeter: residual sugar 1.2 vs 6.4 g/L median, red vs white
- ~18% of rows were exact duplicates, mostly white wines
- Quality is coarse (integer, 3-9) — treat as ordinal regression or classify ≥7 as "good"
- Cite Cortez et al. (2009) if you publish results
