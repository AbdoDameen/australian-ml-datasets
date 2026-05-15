# Australian Aircraft Register Dataset

**Standard pipeline for cleaning, preparation, and feature engineering of the Australian civil aircraft register.**

## Overview

This dataset contains the register of civil aircraft in Australia as maintained by the Civil Aviation Safety Authority (CASA). It includes information on aircraft registration marks, manufacturers, models, engine types, weight, operational status, and registration holder details.

## Source

- **Data source:** Civil Aviation Safety Authority (CASA) — Australian Aircraft Register
- **Raw file:** `raw/aircraft_register_clean.csv`
- **Format:** CSV (comma-separated), 44 columns, ~16,600 rows

## Columns

| Column | Description |
|--------|-------------|
| `mark` | Aircraft registration mark (tail number) |
| `manu` | Aircraft manufacturer |
| `type` | Aircraft type (blank in this extraction) |
| `model` | Model designation |
| `serial` | Manufacturer serial number |
| `mtow` | Maximum Take-Off Weight (kg) |
| `engnum` | Number of engines |
| `engmanu` | Engine manufacturer |
| `engtype` | Engine type (Piston, Turboshaft, Turboprop, Turbofan, etc.) |
| `engmodel` | Engine model |
| `fueltype` | Fuel type (Gasoline, Kerosene, Diesel, Electricity) |
| `regtype` | Registration type |
| `regholdname` | Registration holder name |
| `regholdadd1` | Registration holder address line 1 |
| `regholdadd2` | Registration holder address line 2 |
| `regholdsuburb` | Registration holder suburb |
| `regholdstate` | Registration holder state |
| `regholdpostcode` | Registration holder postcode |
| `regholdcountry` | Registration holder country |
| `regholdcommdate` | Registration holder commencement date |
| `regopname` | Registered operator name |
| `regopadd1` | Registered operator address line 1 |
| `regopadd2` | Registered operator address line 2 |
| `regopsuburb` | Registered operator suburb |
| `regopstate` | Registered operator state |
| `regoppostcode` | Registered operator postcode |
| `regopcountry` | Registered operator country |
| `regopcommdate` | Registered operator commencement date |
| `datefirstreg` | Date of first registration |
| `gear` | Landing gear type |
| `airframe` | Airframe category (Power Driven Aeroplane, Rotorcraft, Glider, etc.) |
| `coacata` | C of A category A |
| `coacatb` | C of A category B |
| `coacatc` | C of A category C |
| `propmanu` | Propeller manufacturer |
| `propmodel` | Propeller model |
| `typecert` | Type certificate reference |
| `countrymanu` | Country of manufacture |
| `yearmanu` | Year of manufacture |
| `regexpirydate` | Registration expiry date |
| `suspendstatus` | Suspension status |
| `suspenddate` | Suspension date |
| `icaotypedesig` | ICAO type designator |
| `idera_authorised_party` | IDERA authorised party |

## Usage

### Prerequisites

```bash
pip install pandas numpy scikit-learn
```

### Run the pipeline

```bash
cd datasets/transport/aircraft-register
python3 prepare_dataset.py
```

### Output files

| File | Description |
|------|-------------|
| `processed/aircraft_register_processed.csv` | Cleaned dataset with engineered features |
| `processed/aircraft_register_processed.parquet` | Same data in Parquet format (if pyarrow available) |
| `features/aircraft_register_features.csv` | StandardScaler-normalised numerical features |
| `features/scaler_params.json` | Scaler parameters (means, scales) for inference |

### Engineered features

- `decade`: Decade of manufacture (e.g., "2000s")
- `manu_freq`: Frequency encoding of manufacturer
- `is_aeroplane`: Binary indicator for aeroplane airframes
- `is_rotorcraft`: Binary indicator for rotorcraft airframes
- `engine_category`: Broad engine class (Piston, Turbine, Electric, Diesel)
- `aircraft_age`: Age in years (reference year: 2025)
- `is_full_registration`: Binary indicator for full registration

## License

Refer to CASA terms of use for the underlying data.
