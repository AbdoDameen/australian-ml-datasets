# Data Preparation Process — Australian Aircraft Register

## Step-by-step breakdown of the pipeline (`prepare_dataset.py`)

---

### Step 1: Load Raw Data

**Input:** `raw/aircraft_register_clean.csv`  
**Method:** `pandas.read_csv()` with `dtype=str` and `keep_default_na=False`

All 44 columns are read as strings to avoid premature type coercion. Empty cells are kept as empty strings, not `NaN`, giving full control over cleaning.

**Stats:** ~16,600 rows, 44 columns

---

### Step 2: Strip Strings & Standardise Column Names

**Operations:**
- Every cell in the DataFrame is trimmed of leading/trailing whitespace via `.map(lambda x: x.strip() if isinstance(x, str) else x)`.
- Column names are lowercased, whitespace/special characters replaced with underscores, and trailing underscores stripped.

**Rationale:**
- String fields like `manu`, `engtype`, and `regholdname` often carry incidental whitespace.
- Standardised snake_case names are portable across databases, ML frameworks, and analysis tools.

---

### Step 3: Handle Missing / Placeholder Values

**Placeholder replacement:**
Common empty-token values (`""`, `"NA"`, `"N/A"`, `"None"`, `"Nil"`, `"-"`, `"--"`, `"?"`) are replaced with `numpy.nan`.

**Numeric columns (`mtow`, `engnum`, `yearmanu`):**
- Coerced to numeric via `pd.to_numeric(..., errors="coerce")`.
- Remaining `NaN` values filled with the column median.

**Categorical / string columns:**
- `NaN` values filled with the string `"Unknown"`.

**Rationale:**
- The raw data uses inconsistent conventions for missing data (blank, `NA`, `-`).
- Median imputation for numeric features is robust to skew; "Unknown" preserves the categorical structure for string columns.

---

### Step 4: Feature Engineering

| Feature | Source Column | Method | Rationale |
|---------|---------------|--------|-----------|
| `decade` | `yearmanu` | `(year // 10) * 10` + `"s"` suffix | Groups years into interpretable cohorts; reduces sparsity |
| `manu_freq` | `manu` | Frequency encoding (count of each manufacturer) | Captures manufacturer prevalence; avoids high-cardinality one-hot |
| `is_aeroplane` | `airframe` | Case-insensitive string contains `"aeroplane"` | Binary flag for aeroplane airframes |
| `is_rotorcraft` | `airframe` | Case-insensitive string contains `"rotorcraft"` | Binary flag for rotorcraft airframes |
| `engine_category` | `engtype` | Keyword-matching into Piston / Turbine / Electric / Diesel / Not Applicable / Other | Groups 15+ raw engine types into 6 interpretable classes |
| `aircraft_age` | `yearmanu` | `2025 - yearmanu` (reference year) | More intuitive than raw year; zero-centred for modelling |
| `is_full_registration` | `regtype` | `regtype == "Full Registration"` | Binary flag for the most common registration status |

---

### Step 5: Save Processed Dataset

**Outputs (to `processed/`):**
- `aircraft_register_processed.csv` — full cleaned dataset with all engineered features (CSV format)
- `aircraft_register_processed.parquet` — same data in columnar Parquet format (if `pyarrow` is installed)

**Rationale:**
- CSV for maximum portability.
- Parquet for efficient storage (~70% smaller) and faster readback in ML pipelines.

**Row count after cleaning:** Same as input (~16,600) — no rows are dropped.

---

### Step 6: Create ML Features with StandardScaler

**Selection:**
8 numeric feature columns are selected: `mtow`, `engnum`, `yearmanu`, `manu_freq`, `aircraft_age`, `is_aeroplane`, `is_rotorcraft`, `is_full_registration`.

**Scaling:**
- `StandardScaler` from scikit-learn is fitted on the numeric features.
- Each feature is transformed to have mean ~0 and standard deviation ~1.

**Outputs (to `features/`):**
- `aircraft_register_features.csv` — standardised feature matrix with `mark` as an index column
- `scaler_params.json` — scaler means and scales for reproducible inference

**Rationale:**
- Standard scaling is required for distance-based and gradient-based ML models (SVM, k-NN, neural networks, PCA).
- Including `mark` allows joining features back to the full dataset or original source.

---

## Reproducibility

To reproduce the full pipeline:

```bash
pip install pandas numpy scikit-learn
cd datasets/transport/aircraft-register
python3 prepare_dataset.py
```

No random seeds are used — results are deterministic for the same input.
