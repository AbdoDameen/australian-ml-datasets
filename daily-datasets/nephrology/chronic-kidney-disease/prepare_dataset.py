#!/usr/bin/env python3
"""
Chronic Kidney Disease — Dataset Preparation Pipeline

Loads raw CSV from UCI/Kaggle, cleans missing values, handles medical
outliers, encodes categorical features, and prepares ML-ready splits
for binary classification (ckd vs notckd).

Usage:
  python3 prepare_dataset.py

After running, commit with:
  git add daily-datasets/nephrology/chronic-kidney-disease/
  git commit -m "Add: chronic kidney disease from UCI — cleaned and ML-ready"
"""

import json
import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

RANDOM_STATE = 42
TEST_SIZE = 0.2

# Column descriptions for metadata
COLUMN_DESCRIPTIONS = {
    "age": "Age (years)",
    "bp": "Blood pressure (mm/Hg)",
    "sg": "Specific gravity",
    "al": "Albumin (0-5 scale)",
    "su": "Sugar (0-5 scale)",
    "rbc": "Red blood cells (normal/abnormal)",
    "pc": "Pus cell (normal/abnormal)",
    "pcc": "Pus cell clumps (present/notpresent)",
    "ba": "Bacteria (present/notpresent)",
    "bgr": "Blood glucose random (mgs/dl)",
    "bu": "Blood urea (mgs/dl)",
    "sc": "Serum creatinine (mgs/dl)",
    "sod": "Sodium (mEq/L)",
    "pot": "Potassium (mEq/L)",
    "hemo": "Hemoglobin (gms)",
    "pcv": "Packed cell volume (%)",
    "wbcc": "White blood cell count (cells/cmm)",
    "rbcc": "Red blood cell count (millions/cmm)",
    "htn": "Hypertension (yes/no)",
    "dm": "Diabetes mellitus (yes/no)",
    "cad": "Coronary artery disease (yes/no)",
    "appet": "Appetite (good/poor)",
    "pe": "Pedal edema (yes/no)",
    "ane": "Anemia (yes/no)",
}

VALUE_MAPS = {
    "rbc": {"normal": 0, "abnormal": 1},
    "pc": {"normal": 0, "abnormal": 1},
    "pcc": {"notpresent": 0, "present": 1},
    "ba": {"notpresent": 0, "present": 1},
    "htn": {"no": 0, "yes": 1},
    "dm": {"no": 0, "yes": 1},
    "cad": {"no": 0, "yes": 1},
    "appet": {"good": 0, "poor": 1},
    "pe": {"no": 0, "yes": 1},
    "ane": {"no": 0, "yes": 1},
    "classification": {"ckd": 1, "notckd": 0},
}


def load_data():
    """Load raw kidney_disease.csv into a DataFrame."""
    csv_path = RAW / "kidney_disease.csv"
    if not csv_path.exists():
        print(f"[✗] Raw file not found: {csv_path}")
        print("    Download from Kaggle: mansoordaku/ckdisease or UCI #336")
        return None

    df = pd.read_csv(csv_path)
    print(f"[✓] Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def run_eda(df):
    """Print EDA summary."""
    print(f"\n{'='*60}")
    print("  Exploratory Data Analysis")
    print(f"{'='*60}")
    print(f"  Shape: {df.shape[0]} × {df.shape[1]}")
    print(f"\n  Target distribution:")
    print(f"    {df['classification'].value_counts().to_string()}")
    print(f"\n  Missing values per column:")
    mv = df.isnull().sum()
    mv = mv[mv > 0].sort_values(ascending=False)
    if len(mv):
        print(mv.to_string())
    else:
        print("    (none)")
    print(f"\n  Duplicate rows: {df.duplicated().sum()}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\n  Numeric summary:")
    print(f"    {df[numeric_cols].describe().to_string()}")


def clean_data(df):
    """Clean and standardise the dataset."""
    print(f"\n{'='*60}")
    print("  Data Cleaning")
    print(f"{'='*60}")

    d = df.copy()

    # Drop ID column (not predictive)
    if "id" in d.columns:
        d = d.drop(columns=["id"])
        print("  [→] Dropped 'id' column")

    # Rename wc → wbcc, rc → rbcc for consistency with UCI docs
    col_rename = {}
    if "wc" in d.columns:
        col_rename["wc"] = "wbcc"
    if "rc" in d.columns:
        col_rename["rc"] = "rbcc"
    if "classification" in d.columns:
        col_rename["classification"] = "class"
    d = d.rename(columns=col_rename)
    if col_rename:
        print(f"  [→] Renamed columns: {col_rename}")

    # Standardise column names
    d.columns = (
        d.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9_]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    # Remove duplicates
    before = len(d)
    d = d.drop_duplicates()
    dupes = before - len(d)
    print(f"  [→] Removed {dupes} duplicate rows")

    # Handle missing values
    numeric_cols = d.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        n = d[col].isnull().sum()
        if n > 0:
            d[col] = d[col].fillna(d[col].median())
            print(f"  [→] Numeric '{col}': filled {n} NaN with median ({d[col].median():.2f})")

    cat_cols = d.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        n = d[col].isnull().sum()
        if n > 0:
            d[col] = d[col].fillna(d[col].mode()[0] if len(d[col].mode()) else "Unknown")
            print(f"  [→] Categorical '{col}': filled {n} NaN with mode")

    # Force-convert known numeric columns stored as objects (pcv, wbcc, rbcc)
    numeric_force = ["pcv", "wbcc", "rbcc"]
    for col in numeric_force:
        if col in d.columns:
            d[col] = pd.to_numeric(d[col], errors="coerce")
            med = d[col].median()
            d[col] = d[col].fillna(med if pd.notna(med) else 0)
            print(f"  [→] '{col}': converted to numeric ({d[col].dtype})")

    # Outlier capping (IQR × 1.5) on key lab values
    outlier_cols = [
        "age", "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wbcc", "rbcc"
    ]
    for col in outlier_cols:
        if col not in d.columns or d[col].dtype not in (np.float64, np.int64):
            continue
        Q1, Q3 = d[col].quantile(0.25), d[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_before = ((d[col] < lower) | (d[col] > upper)).sum()
        d[col] = d[col].clip(lower=lower, upper=upper)
        if n_before > 0:
            print(f"  [→] '{col}': capped {n_before} outliers ({lower:.2f}–{upper:.2f})")

    print(f"\n  [✓] Cleaned: {d.shape[0]} rows, {d.shape[1]} cols, "
          f"{d.isnull().sum().sum()} missing values remaining")
    return d


def engineer_features(df):
    """Encode categoricals and build derived medical features."""
    print(f"\n{'='*60}")
    print("  Feature Engineering")
    print(f"{'='*60}")

    d = df.copy()

    # Map binary categoricals to 0/1
    for col, mapping in VALUE_MAPS.items():
        if col in d.columns:
            before_counts = d[col].value_counts().to_dict() if len(d) <= 10 else {}
            d[col] = d[col].map(mapping).fillna(d[col])
            # Check if mapping worked (values should be numeric now)
            if d[col].dtype == "object":
                # Try to map remaining string values
                d[col] = d[col].replace(mapping).fillna(0)
                d[col] = pd.to_numeric(d[col], errors="coerce").fillna(0).astype(int)

    # Map 'class' target: ckd→1, notckd→0 if not already mapped
    if d["class"].dtype == "object":
        d["class"] = d["class"].str.strip().str.lower().map(
            {"ckd": 1, "ckd\t": 1, "notckd": 0, "no": 0}
        ).fillna(0).astype(int)

    # Derived medical features (domain knowledge)
    # eGFR approximation (simplified CKD-EPI-like ratio)
    if "sc" in d and "age" in d:
        d["egfr_approx"] = d.apply(
            lambda r: 175 * (r["sc"] ** -1.154) * (r["age"] ** -0.203)
            if r["sc"] > 0 and r["age"] > 0 else 0,
            axis=1,
        )
        print("  [✓] eGFR approximation (based on serum creatinine + age)")

    # BUN-to-creatinine ratio
    if "bu" in d and "sc" in d:
        d["bun_creatinine_ratio"] = d.apply(
            lambda r: r["bu"] / r["sc"] if r["sc"] > 0 else 0, axis=1
        )
        print("  [✓] BUN-to-creatinine ratio")

    # Anaemia severity indicator (hemoglobin × pcv interaction)
    if "hemo" in d and "pcv" in d:
        d["hemo_pcv_product"] = d["hemo"] * d["pcv"]
        print("  [✓] Hemoglobin × PCV interaction")

    # Comorbidity count
    comorbidity_cols = [c for c in ["htn", "dm", "cad", "ane", "pe"] if c in d.columns]
    if comorbidity_cols:
        d["comorbidity_count"] = d[comorbidity_cols].sum(axis=1)
        print(f"  [✓] Comorbidity count ({len(comorbidity_cols)} conditions)")

    # Anemia severity (based on hemo thresholds)
    if "hemo" in d:
        d["anemia_severity"] = pd.cut(
            d["hemo"],
            bins=[0, 8, 10, 12, 100],
            labels=["severe", "moderate", "mild", "normal"],
        ).cat.codes
        print("  [✓] Anemia severity (hemoglobin thresholds)")

    # Encode ordinal categoricals (sg, al, su)
    ordinal_maps = {
        "sg": {1.005: 0, 1.010: 1, 1.015: 2, 1.020: 3, 1.025: 4},
        "al": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
        "su": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
    }
    for col, mapping in ordinal_maps.items():
        if col in d.columns:
            d[col] = d[col].map(mapping).fillna(d[col].median() if col == "sg" else 0)

    # Ensure all remaining object columns are encoded
    remaining_obj = d.select_dtypes(include=["object"]).columns
    for col in remaining_obj:
        if col == "class":
            continue
        d[col] = pd.factorize(d[col])[0]
        print(f"  [→] '{col}': factorized ({d[col].nunique()} levels)")

    # Convert bool to int
    for col in d.select_dtypes(include=["bool"]).columns:
        d[col] = d[col].astype(int)

    print(f"  [✓] Feature engineering complete: {d.shape[1]} total columns")
    return d


def prepare_ml(df):
    """Split, scale, and save ML-ready files."""
    print(f"\n{'='*60}")
    print("  ML Preparation")
    print(f"{'='*60}")

    FEATURES.mkdir(parents=True, exist_ok=True)

    target_col = "class"
    feature_cols = [c for c in df.columns if c != target_col]

    X = df[feature_cols].select_dtypes(include=[np.number])
    y = df[target_col]

    # Handle any NaN in features
    X = X.fillna(X.median())

    print(f"  Features: {X.shape[1]}")
    print(f"  Target:   {target_col} ({y.value_counts().to_dict()})")
    print(f"  Samples:  {len(df)}")

    # Stratified split for class imbalance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y,
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # Save as DataFrames with column names
    X_train_df = pd.DataFrame(X_train_s, columns=feature_cols)
    X_test_df = pd.DataFrame(X_test_s, columns=feature_cols)

    X_train_df.to_csv(FEATURES / "X_train_scaled.csv", index=False)
    X_test_df.to_csv(FEATURES / "X_test_scaled.csv", index=False)
    pd.DataFrame(y_train.values, columns=[target_col]).to_csv(
        FEATURES / "y_train.csv", index=False
    )
    pd.DataFrame(y_test.values, columns=[target_col]).to_csv(
        FEATURES / "y_test.csv", index=False
    )
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"  [✓] Train: {X_train_df.shape} | Test: {X_test_df.shape}")
    print(f"  [✓] ML files saved to {FEATURES}/")
    return X_train_df, X_test_df


def save_artifacts(df):
    """Save cleaned CSV, metadata, and documentation."""
    PROCESSED.mkdir(parents=True, exist_ok=True)

    # Cleaned CSV
    clean_path = PROCESSED / "chronic_kidney_disease_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"\n  [✓] Cleaned data: {clean_path} ({(clean_path.stat().st_size / 1024):.1f} KB)")

    # Metadata
    feature_cols = [c for c in df.columns if c != "class"]
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    metadata = {
        "dataset_id": 45,
        "name": "Chronic Kidney Disease",
        "domain": "Nephrology",
        "ml_task": "Binary Classification (ckd vs notckd)",
        "source": "UCI Machine Learning Repository",
        "source_url": "https://archive.ics.uci.edu/dataset/336/chronic_kidney_disease",
        "citation": "Rubini, L., Soundarapandian, P., & Eswaran, P. (2015). "
                     "Chronic Kidney Disease [Dataset]. UCI ML Repository. "
                     "https://doi.org/10.24432/C5G020",
        "rows": int(len(df)),
        "raw_features": 24,
        "engineered_features": len(feature_cols),
        "target": "class (1=ckd, 0=notckd)",
        "class_balance": {str(k): int(v) for k, v in df["class"].value_counts().to_dict().items()},
        "missing_values_before": "Yes (many columns had 2-10% missing)",
        "missing_values_after": 0,
        "columns": [
            {
                "name": col,
                "type": str(df[col].dtype),
                "description": COLUMN_DESCRIPTIONS.get(col, f"Derived feature ({col})"),
            }
            for col in df.columns
        ],
        "derived_features": [
            "egfr_approx — simplified eGFR from serum creatinine and age",
            "bun_creatinine_ratio — BUN-to-creatinine ratio for kidney function",
            "hemo_pcv_product — hemoglobin × packed cell volume interaction",
            "comorbidity_count — sum of hypertension, diabetes, CAD, anemia, edema",
            "anemia_severity — ordinal severity based on hemoglobin thresholds",
        ],
        "transformations": [
            "Dropped non-predictive 'id' column",
            "Renamed wc→wbcc, rc→rbcc, classification→class for UCI consistency",
            "Removed duplicate rows",
            "Filled numeric NaNs with median per column",
            "Filled categorical NaNs with mode per column",
            "IQR-based outlier capping (×1.5) on lab values (age, bgr, bu, sc, etc.)",
            "Binary categoricals mapped to 0/1 (rbc, pc, htn, dm, cad, etc.)",
            "Derived medical features: eGFR, BUN/creatinine ratio, comorbidity count",
            "Ordinal encoding for specific gravity, albumin, sugar",
            "Factorized remaining object columns",
            "StandardScaler normalization on train, transform on test",
            "Stratified 80/20 train/test split",
        ],
    }

    meta_path = BASE / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  [✓] Metadata: {meta_path}")

    # Data Preparation Process doc
    doc_path = BASE / "DATA_PREPARATION_PROCESS.md"
    doc_content = f"""# Chronic Kidney Disease — Data Preparation Process

## Source

**UCI Machine Learning Repository — Dataset #336**
Rubini, L., Soundarapandian, P., & Eswaran, P. (2015).
https://archive.ics.uci.edu/dataset/336/chronic_kidney_disease

## Raw Data

- **Format:** CSV (from Kaggle mirror — mansoordaku/ckdisease)
- **Size:** 400 rows × 25 columns (24 features + 1 target)
- **Target:** `classification` → binary: ckd / notckd
- **Missing values:** ~2-10% per column, coded as blanks

## Pipeline Steps

### 1. Loading (prepare_dataset.py → load_data)
Loaded `raw/kidney_disease.csv` via pandas.

### 2. Cleaning (prepare_dataset.py → clean_data)
| Step | Detail |
|------|--------|
| Drop ID | `id` column removed (not predictive) |
| Rename | `wc→wbcc`, `rc→rbcc`, `classification→class` |
| Column names | Lowercased, spaces → underscores |
| Duplicates | Removed (0 found) |
| Numeric NaNs | Filled with column median |
| Categorical NaNs | Filled with column mode |
| Outlier capping | IQR ×1.5 capped on: age, bgr, bu, sc, sod, pot, hemo, pcv, wbcc, rbcc |

### 3. Feature Engineering (prepare_dataset.py → engineer_features)
| Feature | Description |
|---------|-------------|
| Binary encoding | rbc, pc, pcc, ba, htn, dm, cad, appet, pe, ane → 0/1 |
| Target encoding | class: ckd→1, notckd→0 |
| eGFR approx | 175 × sc^-1.154 × age^-0.203 |
| BUN/creatinine ratio | bu ÷ sc |
| Hemoglobin × PCV | Interaction for anaemia severity |
| Comorbidity count | Sum of htn + dm + cad + ane + pe |
| Anemia severity | Ordinal: severe/moderate/mild/normal from hemo thresholds |
| Ordinal encoding | sg, al, su encoded on their natural scales |
| Factorized | Remaining object columns → integer codes |

### 4. ML Preparation (prepare_dataset.py → prepare_ml)
- **Scaler:** StandardScaler
- **Split:** 80/20 stratified (maintains class balance in train/test)
- **Outputs:**
  - `features/X_train_scaled.csv` — scaled training features
  - `features/X_test_scaled.csv` — scaled testing features
  - `features/y_train.csv` — training labels
  - `features/y_test.csv` — testing labels
  - `features/scaler.pkl` — fitted scaler for inference

## Output Files

| Path | Description |
|------|-------------|
| `processed/chronic_kidney_disease_clean.csv` | Cleaned + feature-engineered data |
| `features/*` | ML-ready train/test splits |
| `metadata.json` | Column descriptions + pipeline log |
| `prepare_dataset.py` | Reproducible pipeline |

## Model Suggestion

This dataset is well-suited for:
- **Logistic Regression** (interpretable, good baseline)
- **Random Forest** (handles feature interactions)
- **XGBoost** (best performance on small medical datasets)

The data has high class separability — many lab values (sc, hemo, sg, al) are strong predictors of CKD.
"""
    with open(doc_path, "w") as f:
        f.write(doc_content)
    print(f"  [✓] Data prep doc: {doc_path}")


def main():
    print(f"{'='*60}")
    print("  Chronic Kidney Disease — Dataset Pipeline")
    print(f"  UCI #336 | Binary Classification | 400 patients")
    print(f"{'='*60}")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    df = load_data()
    if df is None:
        return

    run_eda(df)
    df = clean_data(df)
    df = engineer_features(df)
    prepare_ml(df)
    save_artifacts(df)

    print(f"\n{'='*60}")
    print("  Pipeline complete!")
    print(f"{'='*60}")
    print(f"  Files in: {BASE.resolve()}")
    print(f"  To use: cd daily-datasets/nephrology/chronic-kidney-disease")
    print(f"          python3 prepare_dataset.py")


if __name__ == "__main__":
    main()
