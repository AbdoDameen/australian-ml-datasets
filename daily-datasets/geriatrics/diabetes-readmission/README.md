# Diabetes Readmission

**Domain:** Geriatrics
**ML Task:** Binary classification (predict 30-day hospital readmission)
**Source:** UCI Machine Learning Repository
**License:** CC BY 4.0

Clinical records from 130 US hospitals (1999–2008) spanning ~102K inpatient encounters for patients with diabetes. Target is whether the patient was readmitted within 30 days of discharge (~11% positive rate).

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original CSV from UCI (`diabetic_data.csv`) |
| `processed/` | Cleaned + feature-engineered data (14MB, gitignored) |
| `features/` | ML-ready scaled train/test splits (151MB, gitignored) |
| `prepare_dataset.py` | Reproducible pipeline — run to regenerate |

## Columns

| Column | Description |
|--------|-------------|
| `readmit_30d` | **Target** — 1 if readmitted <30 days, else 0 |
| `time_in_hospital` | Length of stay (days) |
| `num_lab_procedures` | Number of lab tests performed |
| `num_procedures` | Number of non-lab procedures |
| `num_medications` | Number of medications prescribed |
| `number_outpatient` | Prior outpatient visits |
| `number_emergency` | Prior emergency visits |
| `number_inpatient` | Prior inpatient visits |
| `number_diagnoses` | Number of diagnoses entered |
| `age_mid` | Age group as numeric midpoint |
| `is_female` | Gender indicator |
| `a1c_level` | A1C result (0=None, 1=Norm, 2=>7, 3=>8) |
| `glucose_level` | Max glucose serum (0=None, 1=Norm, 2=>200, 3=>300) |
| `med_change` | Medication change flag (0/1) |
| `diabetes_med` | Diabetes medication prescribed (0/1) |
| `race_*` | One-hot encoded race (5 cols) |
| `adm_type_*` | One-hot encoded admission type (8 cols) |
| `spec_*` | One-hot encoded medical specialty (10 cols) |
| `metformin`… | 21 medication columns as ordinal (0=No, 1=Down, 2=Steady, 3=Up) |

## Usage

```bash
cd daily-datasets/geriatrics/diabetes-readmission
python3 prepare_dataset.py
```

This regenerates the cleaned data and ML-ready splits.
