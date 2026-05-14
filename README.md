<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E3A5F,100:0A2540&height=180&section=header&text=Australian%20ML%20Datasets&fontSize=42&fontColor=fff&animation=fadeIn&desc=Curated%20%E2%80%A2%20Cleaned%20%E2%80%A2%20ML-Ready&descSize=16" />
</div>

<p align="center">
  <b>A curated collection of high-quality Australian datasets</b><br>
  Cleaned, structured, and feature-engineered for machine learning.
</p>

<div align="center">
  <img src="https://img.shields.io/badge/datasets-11-1E3A5F?style=for-the-badge" />
  <img src="https://img.shields.io/badge/domains-6-0A66C2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/language-Python-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/license-Varies-8B5CF6?style=for-the-badge" />
</div>

---

## 📋 About

This repository provides **real-world Australian datasets** — cleaned, documented, and ready for machine learning. Each dataset includes:

- 📁 **Raw data** — original source files
- 🧹 **Cleaned data** — processed with documented transformations
- ⚙️ **ML-ready features** — scaled train/test splits with fitted scalers
- 📖 **Documentation** — README, metadata, and full process description
- 🔄 **Reproducible pipeline** — one script to regenerate everything

## 🗂️ Datasets

### 🌤️ Weather & Climate
| Dataset | Description | Source |
|---------|-------------|--------|
| [Rain in Australia](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/weather/rain-in-australia) | Climate variables from Australian weather stations | Bureau of Meteorology |

### 🏭 Energy
| Dataset | Description | Source |
|---------|-------------|--------|
| [CARMA Power Plant Emissions](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/energy/carma-power-plant-emissions) | CO2 emissions for 481 Australian power plants (2000, 2007, Future) | CARMA.org |

### ⛏️ Resources
| Dataset | Description | Source |
|---------|-------------|--------|
| [WA Mining Tenements](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/resources/mining-tenements) | Western Australian mining tenement records | DMIRS / data.wa.gov.au |

### 🏠 Housing
| Dataset | Description | Source |
|---------|-------------|--------|
| [NSW Dwelling Units](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/housing/nsw-dwelling-units) | NSW building approvals by sector | ABS |

### 🚗 Transport
| Dataset | Description | Source |
|---------|-------------|--------|
| [Australian Aircraft Register](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/transport/aircraft-register) | Civil aircraft registered in Australia | CASA |
| [Australia Car Market](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/transport/australia-car-market) | Used car listings with specs and prices | Public dataset |

### ❤️ Health
| Dataset | Description | Source |
|---------|-------------|--------|
| [Child Mortality (1970-2000s)](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/health/child-mortality-1970-2000) | Sex ratios and mortality rates by country | UN / UNICEF |

### 📊 Socioeconomic
| Dataset | Description | Source |
|---------|-------------|--------|
| [SEIFA 1996-2021](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/socioeconomic/seifa-1996-2021) | Socio-Economic Indexes for Areas (1.5M rows) | ABS |

### 🎮 Gaming
| Dataset | Description | Source |
|---------|-------------|--------|
| [Video Game Sales](https://github.com/AbdoDameen/australian-ml-datasets/tree/main/datasets/gaming/video-game-sales) | Global sales data for 16,593 games | Figshare |

---

## 📁 Standard Structure

Every dataset follows the same layout:

```
datasets/[domain]/[dataset-name]/
├── raw/                        # Original source files
├── processed/                  # Cleaned data + engineered features
│   └── [dataset]_clean.csv
├── features/                   # ML-ready data
│   ├── X_train_scaled.csv      # Scaled training features
│   ├── X_test_scaled.csv       # Scaled test features
│   ├── y_train.csv             # Training target
│   ├── y_test.csv              # Test target
│   └── scaler.pkl              # Fitted StandardScaler
├── prepare_dataset.py          # Reproducible pipeline script
├── README.md                   # Dataset overview
├── DATA_PREPARATION_PROCESS.md # Step-by-step process
└── metadata.json               # Structured metadata
```

---

## 🚀 ML Use Cases

| Task | Example Datasets |
|------|-----------------|
| **Regression** | Predict CO2 emissions, car prices, mortality rates |
| **Classification** | Mining tenement status, renewable vs fossil fuel |
| **Time-series** | Dwelling approvals, climate variables, emissions trends |
| **Geospatial** | Power plant locations, mining tenements, SEIFA regions |
| **Recommendation** | Video game sales analysis |

---

## 🛠️ Usage

Clone the repo and explore:

```bash
git clone https://github.com/AbdoDameen/australian-ml-datasets.git
cd australian-ml-datasets

# Process any dataset from scratch
cd datasets/[domain]/[dataset-name]
python3 prepare_dataset.py

# Load a cleaned dataset
import pandas as pd
df = pd.read_csv("processed/[dataset]_clean.csv")
```

---

## 📜 License

Each dataset is subject to its original source license. See individual dataset folders for details.

---

<div align="center">
  <sub>Built with ❤️ and data · 🇦🇺</sub>
</div>
