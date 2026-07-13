# 🔥 Australian Bushfire Analytics — Data Science Portfolio

A collection of 4 data science projects built for Australian fire service applications. These projects demonstrate ML modelling, resource optimisation, satellite remote sensing, and interactive dashboard skills — all using real Australian government data.

**Target roles:** Fire service data science, operational analytics, procurement planning, and geospatial analysis positions.

---

## Projects

### 1. 🔮 Forest Fire Risk Prediction
**ML Classification** — Predicts unplanned forest fires using tenure type, forest category, and prior fire history.

- **Data:** ABARES Forest Fire 2016–2021 (38455 pixel regions across all states)
- **Model:** Random Forest (200 estimators, balanced class weights)
- **Performance:** 0.93 ROC-AUC, 98% recall on fire detection
- **Outputs:** Trained model, SHAP-compatible features, ML-ready train/test splits
- `cd project-1-risk-prediction && python3 prepare_pipeline.py`

### 2. 📊 Resource Allocation Optimisation
**Demand Forecasting + Budget Planning** — Forecasts seasonal fire incident counts and allocates resources (appliances, crews, helicopters) with cost estimates.

- **Approach:** Gradient Boosting regression on aggregated state-tenure groups
- **Outputs:** Per-state resource allocation plan with sensitivity analysis (20% uplift scenario)
- **Use case:** Fire service procurement and operational budgeting
- `cd project-2-resource-allocation && python3 resource_optimisation.py`

### 3. 🛰️ Satellite Burn Scar Mapping
**Computer Vision / Remote Sensing** — Detects bushfire burn scars via Sentinel-2 satellite NDVI change detection.

- **Method:** Pre-fire vs post-fire NDVI comparison (NIR - Red / NIR + Red)
- **Demo:** Synthetic scene generator for offline experimentation
- **Real data:** Includes `download_sentinel2.py` script for Copernicus Data Space API
- `cd project-3-burn-scar-mapping && python3 burn_scar_mapping.py`

### 4. 📈 Interactive Bushfire Dashboard
**Streamlit Dashboard** — Ties all projects together with interactive visualisations.

- Pages: Overview, Risk Explorer, Resource Planner, Burn Scar Viewer
- Uses Plotly for interactive charts (heatmaps, bar charts, maps)
- `cd project-4-dashboard && streamlit run dashboard.py`

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

Each project is self-contained. Pipeline scripts generate all outputs (cleaned data, models, visualisations) from raw ABARES data.

```bash
# Run all projects in order
cd project-1-risk-prediction && python3 prepare_pipeline.py
cd ../project-2-resource-allocation && python3 resource_optimisation.py
cd ../project-3-burn-scar-mapping && python3 burn_scar_mapping.py
cd ../project-4-dashboard && streamlit run dashboard.py
```

## Google Colab Quick Start

Each project folder has a markdown file with a "Run in Colab" badge — click to open and run in your browser without installing anything.

---

*Built by Abdelrhman Dameen — for Australian fire service applications.*
