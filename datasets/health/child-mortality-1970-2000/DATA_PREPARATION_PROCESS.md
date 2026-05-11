# Data Preparation Process — Child Mortality Dataset

## Objective
To clean and prepare the UN Child Mortality dataset (sex ratios and mortality rates by country, 1970s-2000s) for machine learning applications.

## Methodology
CRISP-DM framework: Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment

## Step-by-Step Process

### 1. Data Understanding
- **Source**: UN World Population Prospects 2010 Revision / UNICEF State of the World's Children 2012
- **Format**: Excel (.xls) with multiple sheets
- **Original Records**: 579 rows (countries × decades)
- **Original Features**: 17 columns
- **Countries**: 151
- **Decades**: 1970s, 1980s, 1990s, 2000s
- **Coverage**: Some countries missing 1970s data (127 vs 151 for later decades)

### 2. Initial Data Assessment
- **Missing Values**: 12 rows missing infant/child sex ratios and sex-specific mortality rates (Angola, etc.)
- **Data Types**: Mixed — integer ISO codes, string country names, float mortality rates
- **Quality Issues**:
  - 12 rows with NaN in sex ratio columns
  - Outliers in child mortality (cmr_both: 12 outliers beyond IQR bounds)
  - 83 countries had non-trend estimates (sex_ratio_trend = 'N')

### 3. Data Preparation Steps Applied

#### Step 1: Data Extraction
- Parsed sheet "Table S2-Methods and results"
- Skipped 5 header rows (title, explanatory text, blanks, dual-header row)
- Assigned meaningful column names matching original table structure

#### Step 2: Column Standardization
- Named columns: iso_code, country, sex_ratio_trend, decade, sex_ratio_infant, sex_ratio_child, sex_ratio_under5, imr_male/female/both, cmr_male/female/both, u5mr_male/female/both, method

#### Step 3: Missing Value Treatment
- **Numeric Columns** (sex_ratio_infant, sex_ratio_child, imr_male, imr_female, cmr_male, cmr_female): Filled with column median

#### Step 4: Outlier Treatment
- Used IQR method (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
- **Capped** outliers rather than removing them (preserves data for small-country analysis)
- Columns capped: imr_both (1), cmr_both (12), u5mr_both (1), sex_ratio_infant (3)

#### Step 5: Feature Engineering

| Feature | Type | Description |
|---------|------|-------------|
| `decade_num` | Numeric | Decade as integer (1970→1970) |
| `has_trend` | Binary | 1 if sex_ratio_trend = 'Y' |
| `infant_child_ratio` | Ratio | imr_both / cmr_both |
| `under5_child_ratio` | Ratio | u5mr_both / cmr_both |
| `imr_sex_gap` | Numeric | imr_male - imr_female |
| `u5mr_sex_gap` | Numeric | u5mr_male - u5mr_female |
| `country_freq` | Numeric | Frequency encoding of country |
| `region` | Categorical | Geographic region (7 groups) |
| `method_*` | One-hot | Loess, Linear, Average |

#### Step 6: Region Assignment
Countries grouped by ISO code ranges into 7 geographic regions:
- Northern Africa (ISO 4-20): 11 rows
- Sub-Saharan Africa (ISO 24-60): 30 rows
- Europe & Central Asia (ISO 68-150): 54 rows
- Middle East & South Asia (ISO 158-200): 31 rows
- East Asia & Pacific (ISO 268-530): 235 rows
- Americas (ISO 530-600): 36 rows
- Oceania (ISO 600-894): 182 rows

#### Step 7: ML Preparation
- **Features**: 28 numeric features (all original mortality data + engineered features + encoded categoricals)
- **Default Target**: u5mr_both (under-five mortality rate, both sexes)
- **Split**: 80/20 train/test with random_state=42
- **Scaling**: StandardScaler (z-score normalization)
- **Train set**: 463 rows × 28 features
- **Test set**: 116 rows × 28 features

### 4. Resulting Dataset Characteristics
- **Final Rows**: 579
- **Final Columns**: 34 (cleaned + features)
- **ML Features**: 28
- **Missing Values**: 0
- **Countries**: 151
- **Decades**: 4

### 5. Quality Assurance
- ✅ No duplicate rows
- ✅ Zero missing values in cleaned dataset
- ✅ Consistent encoding across all rows
- ✅ Outliers capped (not removed) to preserve data
- ✅ Reproducible via prepare_dataset.py script
- ✅ Train/test split reproducible (fixed random_state)
- ✅ Scaler saved for transforming new data

### 6. Files Created
| File | Description |
|------|-------------|
| `raw/Table_S2.xls` | Original UN data |
| `processed/child_mortality_clean.csv` | Cleaned dataset (34 columns) |
| `features/X_train_scaled.csv` | Scaled training features |
| `features/X_test_scaled.csv` | Scaled test features |
| `features/y_train.csv` | Training target |
| `features/y_test.csv` | Test target |
| `features/scaler.pkl` | Fitted StandardScaler |
| `metadata.json` | Dataset metadata and transformations |
| `README.md` | Dataset documentation |
| `DATA_PREPARATION_PROCESS.md` | This document |
| `prepare_dataset.py` | Reproducible pipeline script |

## Recommendations for ML Use
1. **Default target**: u5mr_both (under-five mortality) — well-distributed for regression
2. **Alternate targets**: 
   - imr_both for infant mortality prediction
   - sex_ratio_under5 for gender disparity analysis
3. **Feature selection**: Use feature importance to identify key predictors
4. **Temporal modeling**: Use decade_num as a time feature for trend analysis
5. **Regional analysis**: One-hot region encodings enable regional sub-models
6. **Stratified split**: Consider stratifying by region for imbalanced regional analysis

## Reproducibility
```bash
cd datasets/health/child-mortality-1970-2000
python3 prepare_dataset.py
```
