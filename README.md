<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E3A5F,100:0A2540&height=180&section=header&text=Australian%20ML%20Datasets&fontSize=42&fontColor=fff&animation=fadeIn&desc=Curated%20%E2%80%A2%20Cleaned%20%E2%80%A2%20ML-Ready&descSize=16" />
</div>

<p align="center">
  <b>Real Australian data, cleaned and ready to use.</b><br>
  No more scraping government portals at 2am.
</p>

<div align="center">
  <img src="https://img.shields.io/badge/datasets-11-1E3A5F?style=for-the-badge" />
  <img src="https://img.shields.io/badge/domains-6-0A66C2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/language-Python-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/license-Varies-8B5CF6?style=for-the-badge" />
</div>

---

## About

If you've ever tried building ML projects with Australian public data, you know the pain. Government portals serve up data in every format imaginable — Excel sheets with 12 tabs, PDFs masquerading as CSVs, shapefiles only readable by three people on earth. Half the time the column names are in ALL CAPS with random spaces.

This repo fixes that.

Every dataset here has been pulled from its source, cleaned up, feature-engineered, and saved in a format you can actually work with. No wrestling with `encoding='latin1'` or praying `pd.read_excel` finds the right sheet. Just clone it, pick a dataset, and get on with building models.

**Who this is for:**

- **Data scientists** who need real-world Australian data without the cleanup overhead
- **ML students** looking for meaningful datasets to practise on — regression, classification, time-series, geospatial — it's all here
- **Researchers** working on Australian-specific problems who don't want to spend a week just getting the data into shape
- **Anyone** who's ever opened a government CSV and immediately closed it again

Each dataset comes with a `prepare_dataset.py` script so you can see exactly what was done and modify it if needed. No black boxes, no secrets.

---

## Datasets

Browse the datasets/ folder — each one lives under a domain directory:

```
datasets/
├── weather/rain-in-australia/
├── energy/carma-power-plant-emissions/
├── resources/mining-tenements/
├── housing/nsw-dwelling-units/
├── transport/aircraft-register/
├── transport/australia-car-market/
├── health/child-mortality-1970-2000/
├── socioeconomic/seifa-1996-2021/
└── gaming/video-game-sales/
```

Eleven datasets across eight domains, from climate variables to mining tenements to video game sales. Population data, weather stations, power plant emissions, car prices, aircraft registrations — if it's Australian and useful for ML, it's probably in here.

---

## What each dataset gives you

Every dataset follows the same structure. Open any one and you'll find:

```
raw/                        # The original file, untouched
processed/                  # Cleaned data with engineered features
features/                   # ML-ready: scaled splits + scaler
prepare_dataset.py          # Run this to rebuild from scratch
README.md                   # What you're looking at
DATA_PREPARATION_PROCESS.md # Every step documented
metadata.json               # Machine-readable metadata
```

The `prepare_dataset.py` scripts are the real value. Run one and it'll load the raw data, clean it, create features, split into train/test, apply StandardScaler, and save everything to the right folders. Zero manual steps.

---

## Releases

This repo uses semantic versioning. Check the [Releases page](https://github.com/AbdoDameen/australian-ml-datasets/releases) for tagged versions of the full dataset collection.

**Latest release:** v1.0.0

To download a specific release as a zip or tarball:

```bash
curl -LO https://github.com/AbdoDameen/australian-ml-datasets/archive/refs/tags/v1.0.0.tar.gz
```

---

## Quick start

```bash
git clone https://github.com/AbdoDameen/australian-ml-datasets.git
cd australian-ml-datasets

# Pick a dataset and process it
cd datasets/energy/carma-power-plant-emissions
python3 prepare_dataset.py

# Load the cleaned data
import pandas as pd
df = pd.read_csv("processed/carma_australia_emissions_clean.csv")
```

## ML Use Cases

| Problem type | What you can build |
|---|---|
| Regression | Predict CO2 emissions, car prices, mortality rates, socioeconomic scores |
| Classification | Mining tenement status, renewable vs fossil fuel, socioeconomic tiers |
| Time-series | Dwelling approvals trends, climate variable forecasting, emission trajectories |
| Geospatial | Power plant distribution, mining tenement clustering, SEIFA regional analysis |

---

## License

Each dataset keeps its original source license. Check the individual dataset folders for specifics.

---

<div align="center">
  <sub>Built with Python, pandas, and stubbornness. 🇦🇺</sub>
</div>
