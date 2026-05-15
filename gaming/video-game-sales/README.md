# Video Game Sales Dataset (1980-2020)

## Overview
Global sales data for **16,593 video games** spanning 1980-2020 across 31 platforms, 12 genres, and 578 publishers. Includes regional sales breakdowns (NA, EU, JP, Other) and engineered features for ML.

## Source
- **Source**: vgsales public dataset (Figshare)
- **DOI**: https://doi.org/10.6084/m9.figshare.31939302
- **License**: Public domain data

## Dataset Contents

### Raw Data
- `raw/vgsales.json` — Original JSON data (16,598 records)
- `raw/vgsales.md` — Original markdown table

### Processed Data
- `processed/video_game_sales_clean.csv` — Cleaned dataset (16,593 × 38)

### ML-Ready Data
- `features/X_train_scaled.csv` — Scaled training features (13,274 × 31)
- `features/X_test_scaled.csv` — Scaled test features (3,319 × 31)
- `features/y_train.csv` — Training target (global_sales)
- `features/y_test.csv` — Test target
- `features/scaler.pkl` — Fitted StandardScaler

## Key Columns

| Column | Description |
|--------|-------------|
| `name` | Game title |
| `platform` | Platform (PS2, Wii, DS, PC, etc.) |
| `year` | Release year (1980-2020) |
| `genre` | Genre (Action, Sports, RPG, Shooter, etc.) |
| `publisher` | Publisher company |
| `na_sales` | North America sales (millions) |
| `eu_sales` | Europe sales (millions) |
| `jp_sales` | Japan sales (millions) |
| `other_sales` | Other regions sales (millions) |
| `global_sales` | Global total sales (millions) |
| `na_sales_share` | NA share of global sales |
| `*_sales_share` | Regional shares of global |
| `platform_era` | Console generation (Retro, 6th Gen, etc.) |
| `is_top_publisher` | Flag for top 10 publishers |
| `name_length` | Length of game title |

## ML Use Cases
- **Regression**: Predict global sales from platform, genre, publisher features
- **Classification**: Predict best-selling region based on game attributes
- **Recommendation**: Genre/platform affinity analysis
- **Market analysis**: Regional sales pattern analysis

## Data Cleaning Applied
1. Filled 271 missing years and 58 missing publishers
2. Removed 5 duplicate entries
3. Capped outliers using IQR method
4. Created regional sales share features
5. Platform era classification (console generations)
6. One-hot encoded genre and platform era

## Requirements
- pandas, numpy, scikit-learn

## Reproducibility
```bash
cd datasets/gaming/video-game-sales
python3 prepare_dataset.py
```
