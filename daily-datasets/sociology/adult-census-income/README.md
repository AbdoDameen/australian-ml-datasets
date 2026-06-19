# Adult Census Income (Dataset #63)

**Domain:** Sociology  
**ML Task:** Binary Classification — predict if income >$50K/yr  
**Source:** UCI ML Repository ([adult](https://archive.ics.uci.edu/dataset/2/adult))

Census income data from the 1994 US Census. 48K records, 14 demographic and employment features.

## Quick Stats

| Metric | Value |
|--------|-------|
| Rows | 48,790 (cleaned) |
| Features (original) | 14 |
| Features (engineered) | 15 |
| Features (after encoding) | 131 |
| Class balance | 76% ≤50K / 24% >50K |
| Missing handled | workclass (5.7%), occupation (5.7%), native_country (1.8%) |
| Duplicates removed | 52 |

## Columns

**Demographics (5):** age, workclass, education, marital_status, race, sex, native_country  
**Employment (4):** occupation, hours_per_week, fnlwgt (population weight)  
**Financial (4):** capital_gain, capital_loss, education_num  
**Target:** income (>50K or <=50K)

**Engineered (15):** age_group, is_senior, has_advanced_degree, capital_net, has_capital_gain, has_capital_loss, hours_category, is_overtime, is_government, is_self_employed, is_married, is_us_born, is_husband, is_male, income_label

## Usage

```python
import pandas as pd

df = pd.read_csv("processed/adult-census-income_clean.csv")
X = df.drop(columns=["income_label", "income"])
y = df["income_label"]
```

## Notes

- Classic benchmark dataset for binary classification
- Imbalanced (76/24) — evaluate with precision/recall or AUC, not accuracy
- 13K+ hours_per_week outliers capped — most people work exactly 40 hrs
- Capital gain is extremely right-skewed (most people have $0, max $99,999)
