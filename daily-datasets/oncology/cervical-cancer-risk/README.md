# Cervical Cancer Risk Factors

Risk factors for cervical cancer from UCI — 835 patients with sexual history, smoking, contraception, STD history, and screening results.

**Domain:** Oncology  
**ML Task:** Binary classification (Biopsy-positive cancer)  
**Source:** UCI ML Repository — https://archive.ics.uci.edu/dataset/385/cervical+cancer+risk+factors  
**Size:** 835 rows × 36 features (after engineering)

## Target

**Biopsy** — 0 (negative, 93.6%) | 1 (positive, 6.4%). Heavily imbalanced.

## Feature Groups

- **Demographics:** Age
- **Sexual history:** Number of partners, first intercourse age, pregnancies
- **Smoking:** Status, years, packs/year
- **Contraception:** Hormonal contraceptives (years), IUD (years)
- **STD history:** 14 individual STD indicators + diagnosis timeline
- **Engineered (8):** age_group, sexual_activity_score, smoking_years_per_age, heavy_smoker, hormonal_years_per_age, std_count, prior_diagnosis, positive_screening

## Files

| Folder | Contents |
|--------|----------|
| `raw/` | `risk_factors_cervical_cancer.csv` |
| `processed/` | `cervical_cancer_risk_clean.csv` |
| `features/` | X_train_scaled, X_test_scaled, y_train, y_test, scaler.pkl |

## Usage

```bash
cd daily-datasets/oncology/cervical-cancer-risk
python3 prepare_dataset.py
```
