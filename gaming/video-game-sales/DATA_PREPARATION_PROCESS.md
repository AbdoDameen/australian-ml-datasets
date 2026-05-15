# Data Preparation Process — Video Game Sales

## Objective
Clean and prepare the global video game sales dataset for machine learning applications — predicting sales from platform, genre, publisher, and release year features.

## Step-by-Step Process

### 1. Data Understanding
- **Source**: vgsales public dataset
- **Format**: JSON (16,598 records)
- **Features**: 11 columns — Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales
- **Coverage**: 1980-2020, 31 platforms, 12 genres, 578 publishers
- **Missing Values**: 271 missing Year, 58 missing Publisher

### 2. Data Cleaning
1. **Column names**: Standardized to lowercase with underscores
2. **Missing Years**: Filled 271 with median (2007)
3. **Missing Publishers**: Filled 58 with 'Unknown'
4. **Duplicates**: Removed 5 (same name + platform)
5. **Year type**: Converted float to int
6. **Outliers**: Capped via IQR method (affects ~10-15% of sales columns)

### 3. Feature Engineering
| Feature | Type | Description |
|---------|------|-------------|
| `na_sales_share` | Ratio | NA sales ÷ global sales |
| `eu_sales_share` | Ratio | EU sales ÷ global sales |
| `jp_sales_share` | Ratio | JP sales ÷ global sales |
| `other_sales_share` | Ratio | Other sales ÷ global sales |
| `platform_era` | Categorical | Retro, 6th Gen, 7th Gen, 8th Gen, PC, Other |
| `decade` | Ordinal | 1980, 1990, 2000, 2010, 2020 |
| `is_top_publisher` | Binary | Top 10 publisher flag |
| `publisher_games_count` | Numeric | Frequency encoding |
| `platform_freq` | Numeric | Frequency encoding |
| `name_length` | Numeric | Game title length |

### 4. ML Preparation
- **Features**: 31 numeric features
- **Default Target**: global_sales (millions)
- **Split**: 80/20 train/test (13,274 / 3,319)
- **Scaling**: StandardScaler
- **Encoding**: One-hot for genre (12) and platform era (6)

### 5. Files Created
| File | Description |
|------|-------------|
| `raw/vgsales.json` | Original JSON data |
| `processed/video_game_sales_clean.csv` | Cleaned dataset (38 columns) |
| `features/X_train_scaled.csv` | Scaled training features |
| `features/X_test_scaled.csv` | Scaled test features |
| `features/y_train.csv` | Training target |
| `features/y_test.csv` | Test target |
| `features/scaler.pkl` | Fitted StandardScaler |
| `metadata.json` | Dataset metadata |
| `README.md` | Dataset documentation |
| `DATA_PREPARATION_PROCESS.md` | This document |
| `prepare_dataset.py` | Reproducible pipeline |

## Reproducibility
```bash
cd datasets/gaming/video-game-sales
python3 prepare_dataset.py
```
