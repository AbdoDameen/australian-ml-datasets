# Cervical Cancer Risk — Data Preparation Process

## Source

UCI ML Repository: https://archive.ics.uci.edu/dataset/385/cervical+cancer+risk+factors  
Citation: Fernandes, K., Cardoso, J. S., & Fernandes, J. (2017). Transfer learning with partial observability applied to cervical cancer screening.

## Raw Data

`risk_factors_cervical_cancer.csv` — 858 patients, 36 columns. Missing values encoded as `?` in string columns. After parsing: 3,622 `?` values across the dataset.

## Cleaning

1. **Parsed `?` to NaN** across all 27 numeric-object columns
2. **Removed 23 duplicate rows** → 835 unique patients
3. **Filled missing values:**
   - Continuous (median): number of sexual partners (2), first intercourse age (17), pregnancies (2), smoking years (0), pack-years (0), hormonal years (0.5), IUD years (0), STD count (0), time since first STD diagnosis (4 years), time since last (3 years)
   - Binary (filled with 0): smokes, hormonal contraceptives, IUD, STDs, all 14 individual STD indicators

## Feature Engineering

8 derived features:

1. **age_group** — binned: 0-25, 25-35, 35-45, 45+
2. **sexual_activity_score** — partners × pregnancies (capped at 100)
3. **smoking_years_per_age** — smoking duration relative to age
4. **heavy_smoker** — >= 20 pack-years
5. **hormonal_years_per_age** — hormonal contraceptive duration relative to age
6. **std_count** — sum of all individual STD indicators
7. **prior_diagnosis** — any prior cancer/CIN/HPV diagnosis
8. **positive_screening** — any positive Hinselmann/Schiller/Citology test

## ML Preparation

- **Removed from features:** Biopsy (target), Hinselmann/Schiller/Citology (leak w/ target), Dx:Cancer/Dx:CIN/Dx:HPV/Dx (prior diagnosis leaks)
- **Train/test split:** 80/20 stratified by Biopsy (preserves 6.4% positive rate)
- **Scaling:** StandardScaler
- **Imbalance:** 43 positive / 625 negative in train, 11 / 156 in test

## Target Distribution

| Biopsy | Class | Train | Test |
|:-----:|-------|------:|-----:|
| 0 | Negative | 625 (93.6%) | 156 (93.4%) |
| 1 | Positive | 43 (6.4%) | 11 (6.6%) |
