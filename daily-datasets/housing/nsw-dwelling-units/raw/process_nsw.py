import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import json
from datetime import datetime
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Paths
dataset_path = Path('.')
raw_path = dataset_path / 'raw'
processed_path = dataset_path / 'processed'
features_path = dataset_path / 'features'
raw_path.mkdir(exist_ok=True)
processed_path.mkdir(exist_ok=True)
features_path.mkdir(exist_ok=True)

# Find excel in root or raw
excel_candidates = list(dataset_path.glob('*.xls*'))
if not excel_candidates:
    excel_candidates = list(raw_path.glob('*.xls*'))

if not excel_candidates:
    raise FileNotFoundError('No Excel file found in dataset folder or raw/. Place the original .xlsx/.xls file here and re-run.')

src_file = excel_candidates[0]
# copy to raw if not already there
dst_file = raw_path / src_file.name
if not dst_file.exists():
    shutil.copy2(src_file, dst_file)
    print(f'Copied {src_file.name} -> raw/{src_file.name}')
else:
    print(f'Raw file exists: raw/{src_file.name}')

# Load Excel
try:
    df = pd.read_excel(dst_file, header=0)
    # if columns contain Unnamed, try promoting first row
    if df.columns.astype(str).str.contains('Unnamed').sum() > 0 and len(df) > 1:
        df.columns = df.iloc[0].astype(str)
        df = df[1:].reset_index(drop=True)
    print(f'Loaded {dst_file.name} with shape {df.shape}')
except Exception as e:
    raise RuntimeError(f'Failed to read Excel: {e}')

# Cleaning
# Standardize column names
df.columns = [str(c).strip().lower().replace(' ', '_').replace('/', '_') for c in df.columns]
# Drop fully empty rows and reset
df = df.dropna(how='all').reset_index(drop=True)
# Remove duplicates
dups_before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
dups_removed = int(dups_before - len(df))
print(f'Removed duplicates: {dups_removed}')

# Try convert object columns to numeric where appropriate
for col in df.columns:
    if df[col].dtype == object:
        sample = df[col].dropna().astype(str).head(50).str.replace(',', '').str.replace('\u2013', '-')
        if sample.str.match(r'^[-+]?[0-9]*\.?[0-9]+$').any():
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

# Identify numeric and categorical
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()

# Impute numeric with median
for c in numeric_cols:
    if df[c].isnull().any():
        med = df[c].median()
        df[c] = df[c].fillna(med)
        print(f'Imputed numeric {c} with median={med}')

# Impute categorical with mode or Unknown
for c in cat_cols:
    if df[c].isnull().any():
        modes = df[c].mode()
        fill = modes[0] if not modes.empty else 'Unknown'
        df[c] = df[c].fillna(fill)
        print(f'Imputed categorical {c} with {fill}')

# Save cleaned CSV
cleaned_file = processed_path / 'nsw_dwelling_units_clean.csv'
df.to_csv(cleaned_file, index=False)
print(f'Saved cleaned CSV: {cleaned_file}')

# ML prep: label encode small-cardinality categoricals and scale numeric
encoders = {}
for c in cat_cols:
    nunique = int(df[c].nunique(dropna=True)) if c in df.columns else 0
    if nunique <= 20 and nunique > 1:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c].astype(str))
        encoders[c] = le
        print(f'Label encoded {c} (nunique={nunique})')

scaler = None
if numeric_cols:
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols].astype(float))
    joblib.dump(scaler, features_path / 'scaler.pkl')
    print('Scaled numeric columns and saved scaler')

# Save ML-ready features (full table)
features_file = features_path / 'nsw_dwelling_units_features_scaled.csv'
df.to_csv(features_file, index=False)
print(f'Saved ML-ready features: {features_file}')

# Save encoders if created
if encoders:
    joblib.dump(encoders, features_path / 'encoders.pkl')
    print('Saved encoders')

# Update metadata.json
meta = {
    'dataset_name': 'Number of dwelling units approved, by sector, all series - New South Wales',
    'source': 'ABS (provided link) / User provided',
    'original_source': str(dst_file),
    'description': 'Cleaned and ML-prepared dataset of dwelling units approved in NSW by sector and series.',
    'created_date': str(datetime.now()),
    'data_cleaning': {
        'duplicates_removed': dups_removed,
        'missing_values_handled': 'Median for numeric, Mode for categorical',
        'outliers_removed_method': 'Not applied'
    },
    'ml_preparation': {
        'numeric_scaled': numeric_cols,
        'categorical_label_encoded': list(encoders.keys()),
        'scaler_file': str((features_path / 'scaler.pkl')) if scaler is not None else None,
        'encoders_file': str((features_path / 'encoders.pkl')) if encoders else None
    },
    'total_samples': int(len(df)),
    'total_features': int(df.shape[1]),
    'files': {
        'raw': str(dst_file),
        'cleaned': str(cleaned_file),
        'features_scaled': str(features_file),
        'scaler': str((features_path / 'scaler.pkl')) if scaler is not None else None,
        'encoders': str((features_path / 'encoders.pkl')) if encoders else None,
        'metadata': 'metadata.json'
    }
}
with open(dataset_path / 'metadata.json', 'w') as f:
    json.dump(meta, f, indent=2)
print('Updated metadata.json')

# Update README to include ABS source link
readme = dataset_path / 'README.md'
abs_link = 'https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release#data-downloads'
if readme.exists():
    text = readme.read_text(encoding='utf-8')
    if abs_link not in text:
        text = text + '\n\n## Source\nABS data: ' + abs_link + '\n'
        readme.write_text(text, encoding='utf-8')
        print('Updated README with ABS link')
else:
    readme.write_text(f'# Dataset\n\nSource: {abs_link}\n', encoding='utf-8')
    print('Created README with ABS link')

print('\nProcessing complete')
