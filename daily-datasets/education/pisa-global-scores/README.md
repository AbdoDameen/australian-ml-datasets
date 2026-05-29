# Dataset #17: PISA Global Scores

**Domain:** Education
**ML Task:** Classification (math proficiency above/below OECD average)
**Source:** OECD PISA 2022
**Samples:** ~80,000 students
**Features:** Demographics, socioeconomic index, school belonging, emotional support

## What's inside

PISA 2022 student background questionnaire merged with cognitive test scores. Target is binary math proficiency — scored above or below the OECD average (~450).

### Features

- Country, gender, age
- HISEI (socioeconomic index)
- PARED (parents' education)
- Home resources (computer, internet, possessions)
- BELONG (sense of belonging at school)
- EMOSUPS (emotional support)
- Math interest items

### Target

`math_high` — 1 if PV1MATH score above OECD average, 0 otherwise.

## Files

| Folder | Contents |
|--------|----------|
| `processed/` | pisa_cleaned.parquet |
| `features/` | X_train.parquet, X_test.parquet, y_train.parquet, y_test.parquet, scaler.pkl |
| `prepare_dataset.py` | Pipeline script |

## Usage

```bash
/tmp/pisa_venv/bin/python3 prepare_dataset.py
```
