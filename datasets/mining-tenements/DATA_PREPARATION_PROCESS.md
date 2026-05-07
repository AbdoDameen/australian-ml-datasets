# Data Preparation Process for Mining Tenements Dataset

## Objective
To clean and prepare the Western Australian Mining Tenements dataset for machine learning applications while preserving meaningful information and following data science best practices.

## Methodology Followed
This process follows the Cross-Industry Standard Process for Data Mining (CRISP-DM) methodology:
1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

## Step-by-Step Process

### 1. Data Understanding
- **Source**: WFS service from data.wa.gov.au
- **Initial Records**: 5,000 sampled records (full dataset has 30,308 records)
- **Initial Features**: 34 columns including IDs, dates, text fields, and geometry
- **License**: CC BY 4.0 (commercial use allowed with attribution)

### 2. Initial Data Assessment
- **Missing Values**: Analyzed and documented
- **Data Types**: Identified categorical, numerical, and datetime columns
- **Unique Values**: Examined cardinality of categorical features
- **Data Quality**: Checked for inconsistencies, duplicates, and outliers

### 3. Data Cleaning Steps Applied

#### Step 1: Column Name Standardization
- Removed special characters and spaces
- Standardized to lowercase with underscore separation
- Example: `st_area(the_geom)` → `st_area_the_geom`

#### Step 2: Missing Value Treatment
- **Text/Categorical Columns**: Filled with 'Unknown'
- **Numeric Columns**: 
  - Area/perimeter: Filled with 0
  - Other numeric: Filled with column median
- **Empty Strings**: Converted to 'Unknown' for text columns

#### Step 3: Text Cleaning
- Stripped leading/trailing whitespace
- Normalized internal whitespace (multiple spaces → single space)
- Standardized case where appropriate

#### Step 4: DateTime Feature Engineering
- Converted string dates to datetime objects
- Extracted components: year, month, day, day of week
- Calculated derived features: tenure duration (where applicable)
- Preserved original datetime columns for reference

#### Step 5: Feature Engineering for ML
- **Target Variable**: Created `is_live` (binary: 1 if tenstatus == 'LIVE')
- **Categorical Encoding**:
  - Low cardinality (<50 unique values): One-hot encoding
  - High cardinality (≥50 unique values): Frequency encoding
- **Frequency Encoding**: Created `_freq` columns for all categorical features

#### Step 6: Dimensionality Reduction
- Removed columns with limited predictive value for general ML:
  - Internal identifiers (GmlId, oid, gid, tenid)
  - Overly specific holder/address details (use holder count instead)
  - Complex geometry (requires spatial ML techniques)
  - Redundant time components (extracted features instead)
  - Detailed timestamp components (hours/minutes/seconds)

### 4. Resulting Dataset Characteristics
- **Final Rows**: 5000
- **Final Columns**: 62
- **Missing Values**: 0
- **Feature Types**:
  - Numerical: 35
  - Categorical (encoded): 9
  - DateTime Features: 21

### 5. Quality Assurance
- **No Data Leakage**: Target variable created properly
- **Consistent Encoding**: Same transformations applied to all data
- **Traceability**: All transformations documented
- **Reproducibility**: Scripted process ensures repeatability

### 6. Files Created
- `mining_tenements_cleaned.csv`: Cleaned dataset ready for ML
- `README.md`: Dataset overview and usage instructions
- `DATA_PREPARATION_PROCESS.md`: This document
- `clean_dataset.py`: Reusable cleaning script

## Recommendations for Future Use
1. **Full Dataset**: Consider downloading the complete dataset (30,308 records) for production models
2. **Spatial Features**: For advanced modeling, process the geometry column using spatial libraries (GeoPandas, Shapely)
3. **Temporal Analysis**: Use extracted date features for time-series analysis
4. **Feature Selection**: Apply feature importance techniques to identify most predictive variables
5. **Validation**: Always split data temporally when predicting future tenement status

## Reproducibility
To reproduce this cleaning process:
```bash
python3 clean_dataset.py
```

## Contact
For questions about this dataset preparation, refer to the original data source at data.wa.gov.au or consult the cleaning script comments.
