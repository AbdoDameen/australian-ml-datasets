# 🔥 Australian Bushfire Analytics — Data Science Portfolio

A collection of 4 data science projects built for Australian fire service applications. These projects demonstrate ML modelling, resource optimisation, satellite remote sensing, and interactive dashboard skills — all using real Australian government data.

**Target roles:** Fire service data science, operational analytics, procurement planning, and geospatial analysis positions.

---

## Projects

### 🔮 Forest Fire Risk Prediction
**ML Classification** — Predicts unplanned forest fires using tenure type, forest category, and prior fire history.

- **Data:** ABARES Forest Fire 2016–2021 (38455 pixel regions across all states)
- **Model:** Random Forest (200 estimators, balanced class weights)
- **Performance:** 0.93 ROC-AUC, 98% recall on fire detection
- **Outputs:** Trained model, SHAP-compatible features, ML-ready train/test splits
- `cd risk-prediction && python3 prepare_pipeline.py`

### 📊 Resource Allocation Optimisation
**Demand Forecasting + Budget Planning** — Forecasts seasonal fire incident counts and allocates resources (appliances, crews, helicopters) with cost estimates.

- **Approach:** Gradient Boosting regression on aggregated state-tenure groups
- **Outputs:** Per-state resource allocation plan with sensitivity analysis (20% uplift scenario)
- **Use case:** Fire service procurement and operational budgeting
- `cd resource-allocation && python3 resource_optimisation.py`

### 🛰️ Satellite Burn Scar Mapping
**Computer Vision / Remote Sensing** — Detects bushfire burn scars via Sentinel-2 satellite NDVI change detection.

- **Method:** Pre-fire vs post-fire NDVI comparison (NIR - Red / NIR + Red)
- **Demo:** Synthetic scene generator for offline experimentation
- **Real data:** Includes `download_sentinel2.py` script for Copernicus Data Space API
- `cd burn-scar-mapping && python3 burn_scar_mapping.py`

### 📈 Interactive Bushfire Dashboard
**Streamlit Dashboard** — Ties all projects together with interactive visualisations.

- Pages: Overview, Risk Explorer, Resource Planner, Burn Scar Viewer
- Uses Plotly for interactive charts (heatmaps, bar charts, maps)
- `cd dashboard && streamlit run dashboard.py`

---

## Data Sources

| Source | Description | Link |
|--------|-------------|------|
| ABARES Forest Fire Data 2016–2021 | Forest fire occurrence by tenure, forest type, and state — ESRI Grid + CSV attribute table | [agriculture.gov.au](https://www.agriculture.gov.au/abares/forestsaustralia/forest-data-maps-and-tools/spatial-data/forest-fire) |
| Sentinel-2 (Copernicus) | 10m resolution satellite imagery for NDVI burn scar detection | [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) |
| NASA FIRMS | Real-time MODIS/VIIRS active fire hotspots | [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/) |

## Prerequisites

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
# For dashboard:
pip install streamlit plotly
# For real satellite data:
pip install sentinelhub oauthlib
```

## Usage

Each project is self-contained. You can run either the standalone scripts or the Jupyter notebooks:

```bash
# Option A — Standalone runners (generates PNG charts to outputs/charts/)
cd risk-prediction && python3 p1_run.py
cd ../resource-allocation && python3 p2_run.py
cd ../burn-scar-mapping && python3 p3_run.py
cd ../dashboard && python3 p4_run.py
```

```bash
# Option B — Jupyter notebooks (interactive exploration)
cd risk-prediction && jupyter notebook forest_fire_risk_prediction.ipynb
cd ../resource-allocation && jupyter notebook fire_resource_allocation.ipynb
cd ../burn-scar-mapping && jupyter notebook satellite_burn_scar_mapping.ipynb
cd ../dashboard && jupyter notebook bushfire_analytics_dashboard.ipynb
```

---

*Built by Abdelrhman Dameen — for Australian fire service applications.*
