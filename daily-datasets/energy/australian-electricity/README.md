# Australian Electricity Generation

**Domain:** Energy
**Source:** AEMO (Australian Energy Market Operator)
**URL:** https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem

## Description
Electricity generation data from the National Electricity Market (NEM) across all Australian states. Includes generation by fuel type (coal, gas, hydro, wind, solar, battery), scheduled generation, and semi-scheduled generation outputs at 5-minute and 30-minute intervals.

## ML Potential
- Time series forecasting of renewable vs fossil fuel generation
- Anomaly detection in grid operations
- Demand prediction and load balancing

## Files
- `raw/` — Raw CSV/excel downloads from AEMO
- `processed/` — Cleaned, consolidated time series
- `features/` — Engineered features for ML
