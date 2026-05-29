# Dataset #19: MIMIC-III ICU (Emergency)

**Domain:** Emergency-Medicine
**ML Task:** Classification (In-hospital Mortality)
**Source:** Kaggle (ihssanened/mimic-iii-clinical-databaseopen-access) / PhysioNet MIMIC-III
**Samples:** 119 emergency admissions | 39 in-hospital deaths (32.8% mortality rate)

## What's inside

This dataset tracks 119 emergency department admissions from the MIMIC-III database. The goal is to predict **in-hospital mortality** (`hospital_expire_flag`) based on patient data available at or near admission time.

### Tables used

| Table | Description | Rows |
|-------|-------------|------|
| `ADMISSIONS` | Admission records, ED times, diagnosis | 129 |
| `PATIENTS` | Demographics, DOB, gender | 100 |
| `D_LABITEMS` | Lab test code lookup | 753 |
| `LABEVENTS` | Lab measurements | 76,074 |

### Features (71 total)

- **Demographics:** age at admission, gender
- **Admission info:** admission_location, insurance, ethnicity, religion, marital_status, diagnosis
- **ED metrics:** emergency department length of stay (hours)
- **Lab values:** first-measured value of top 20 lab tests per admission (potassium, hematocrit, creatinine, anion gap, WBC, platelets, etc.)

### Target

`hospital_expire_flag` — 1 if patient died during hospital stay, 0 otherwise.

## Files

| Folder | Contents |
|--------|----------|
| `raw/` | Original CSVs (ADMISSIONS, PATIENTS, LABEVENTS, D_LABITEMS) |
| `processed/` | Cleaned features CSV + feature-engineered dataset |
| `features/` | ML-ready: X_train_scaled, X_test_scaled, y_train, y_test, scaler.pkl |

## Usage

```bash
cd daily-datasets/emergency-medicine/mimic-iii-icu
python3 prepare_dataset.py
```
