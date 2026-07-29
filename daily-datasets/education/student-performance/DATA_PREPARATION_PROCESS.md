# Data Preparation: Student Performance

## Source

UCI Machine Learning Repository — "Student Performance" dataset (P. Cortez and A. Silva, 2008).  
Collected from two Portuguese public schools (Gabriel Pereira and Mousinho da Silveira) during 2005–2006.

## Pipeline

### 1. Loading
- Two CSV files (`student-mat.csv`, `student-por.csv`) loaded with `sep=';'`
- A `subject` column added to each before concatenation
- Combined into a single DataFrame: 1,044 rows × 35 columns

### 2. Cleaning
- Column names standardized to lowercase with underscores
- **No missing values** found in either dataset (100% complete)
- **No duplicate rows** detected
- **Outlier capping** applied to `absences` (IQR 1.5× method) — 54 values capped
- Students with absences > 9 clipped to the upper bound

### 3. Feature Engineering
- **Grade changes:** G1→G2, G1→G3 deltas
- **Average grade:** mean of G1, G2, G3
- **Binary flags:** has_failed (failures > 0), high_absences (absences > 10), low_famrel (famrel ≤ 2)
- **Effort metric:** studytime_effort = studytime / (G3 + 1)
- **Alcohol composite:** alcohol_score = DALC + WALC

### 4. ML Preparation
- **Categorical encoding:** One-hot encoding for all 17 categorical variables (school, sex, address, famsize, Pstatus, Mjob, Fjob, reason, guardian, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic)
- **Train/test split:** 80/20 with random_state=42
- **Scaling:** StandardScaler fit on training data, transform both sets
- **Output:** 68 features, 835 train / 209 test samples

## Output Files

| File | Description |
|------|-------------|
| `processed/student-performance_clean.csv` | Combined, cleaned, feature-engineered dataset |
| `features/X_train_scaled.csv` | Training features (scaled, 835×68) |
| `features/X_test_scaled.csv` | Test features (scaled, 209×68) |
| `features/y_train.csv` | Training target (G3) |
| `features/y_test.csv` | Test target (G3) |
| `features/scaler.pkl` | StandardScaler for new predictions |
| `features/feature_names.json` | Feature list and target name |
| `metadata.json` | Full dataset documentation |
