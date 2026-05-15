# Western Australian Mining Tenements Dataset

## Overview
This dataset contains information about mining tenements in Western Australia, sourced from the Department of Mines, Industry Regulation and Safety (DMIRS) through the SLIP (Shared Land Information Platform) WFS service.

## Source
- **Dataset Name**: Mining Tenements (DMIRS-003)
- **Source**: data.wa.gov.au
- **Access Method**: WFS (Web Feature Service) endpoint
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Last Updated**: 2026-05-06

## Dataset Description
The dataset contains information about live, pending, dead, and other types of mining tenements across Western Australia. Each record represents a mining tenement with details about:
- Tenement type and identifier
- Status (surveyed status, tenure status)
- Holder information
- Important dates (grant, start, end dates)
- Legal area measurements
- Geometric boundaries

## Data Cleaning Process
See `DATA_PREPARATION_PROCESS.md` for detailed documentation of the cleaning steps applied.

## Cleaned Dataset Statistics
- **Rows**: 5000
- **Columns**: 62
- **File Size**: Approximately 1642.8 KB

## Column Description
### Key Features:
- `tenstatus`: Tenure status (LIVE, DEAD, PENDING, etc.)
- `survstatus`: Survey status (SURVEYED, UNSURVEYED)
- `type`: Type of tenement (e.g., COAL MINING LEASE)
- `holdercnt`: Number of holders
- `legal_area`: Legal area size
- `unit_of_me`: Unit of measurement (typically HA for hectares)
- `fmt_tenid`: Formatted tenement identifier
- `st_area_the_geom`: Calculated area from geometry
- `st_perimeter_the_geom`: Calculated perimeter from geometry
- `is_live`: Binary target variable (1 if LIVE, 0 otherwise)
- `*_year`, `*_month`, `*_day`, `*_dayofweek`: Extracted date features
- `*_freq`: Frequency encoded categorical features
- Various dummy variables for categorical features

### Original Columns Removed:
- Detailed holder and address information (too specific for general ML)
- Raw geometry data (complex spatial data requiring specialized processing)
- Internal IDs (GmlId, oid, gid, tenid)
- Time components (separate date features extracted instead)
- Redundant identifier columns

## Usage
This cleaned dataset is ready for machine learning tasks such as:
- Classification: Predicting tenement status (LIVE vs DEAD)
- Regression: Predicting tenure duration or area
- Clustering: Grouping similar tenements
- Time series analysis: Understanding temporal patterns

## Requirements
- pandas
- numpy

## License
This dataset is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
See `License_CCBY4.pdf` in the original dataset for full license terms.
