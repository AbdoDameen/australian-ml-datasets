#!/usr/bin/env python3
"""
Expand Video Game Sales dataset with advanced features:
- Market context features (genre dominance, publisher share)
- Competition metrics (games per year/platform/genre)
- Platform lifecycle analysis
- Sales ranking features
"""

import pandas as pd
import numpy as np
import json, pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

BASE = Path("/home/abdodameen/australian-ml-datasets/datasets/gaming/video-game-sales")
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

# Load cleaned data
df = pd.read_csv(PROCESSED / "video_game_sales_clean.csv")
print(f"Loaded {len(df):,} games")

orig_cols = set(df.columns)

# =============================================================================
# 1. MARKET CONTEXT FEATURES
# =============================================================================
print("\n1. Market Context Features")

# Genre dominance: what % of that year's total sales does this genre account for
year_genre_sales = df.groupby(['year', 'genre'])['global_sales'].sum().reset_index()
year_total_sales = df.groupby('year')['global_sales'].sum().reset_index()
year_genre_sales = year_genre_sales.merge(year_total_sales, on='year', suffixes=('', '_total'))
year_genre_sales['genre_market_share'] = year_genre_sales['global_sales'] / year_genre_sales['global_sales_total']
genre_share_map = year_genre_sales.set_index(['year', 'genre'])['genre_market_share'].to_dict()
df['genre_market_share'] = df.apply(lambda r: genre_share_map.get((r['year'], r['genre']), 0), axis=1)
print(f"  ✓ genre_market_share — genre's % of total annual sales")

# Publisher market share by year
year_pub_sales = df.groupby(['year', 'publisher'])['global_sales'].sum().reset_index()
year_pub_sales = year_pub_sales.merge(year_total_sales, on='year', suffixes=('', '_total'))
year_pub_sales['publisher_market_share'] = year_pub_sales['global_sales'] / year_pub_sales['global_sales_total']
pub_share_map = year_pub_sales.set_index(['year', 'publisher'])['publisher_market_share'].to_dict()
df['publisher_market_share'] = df.apply(lambda r: pub_share_map.get((r['year'], r['publisher']), 0), axis=1)
print(f"  ✓ publisher_market_share — publisher's % of total annual sales")

# =============================================================================
# 2. COMPETITION METRICS
# =============================================================================
print("\n2. Competition Metrics")

# Games released in same year
year_counts = df.groupby('year').size().to_dict()
df['games_in_year'] = df['year'].map(year_counts)
print(f"  ✓ games_in_year — total games released that year")

# Games released in same year + genre
year_genre_counts = df.groupby(['year', 'genre']).size().to_dict()
df['games_in_year_genre'] = df.apply(lambda r: year_genre_counts.get((r['year'], r['genre']), 0), axis=1)
print(f"  ✓ games_in_year_genre — games in same year + genre")

# Games released in same year + platform
year_plat_counts = df.groupby(['year', 'platform']).size().to_dict()
df['games_in_year_platform'] = df.apply(lambda r: year_plat_counts.get((r['year'], r['platform']), 0), axis=1)
print(f"  ✓ games_in_year_platform — games in same year + platform")

# =============================================================================
# 3. SALES RANKING FEATURES
# =============================================================================
print("\n3. Sales Ranking Features")

# Sales percentile within year
df['sales_percentile_year'] = df.groupby('year')['global_sales'].rank(pct=True)
print(f"  ✓ sales_percentile_year — percentile rank within release year")

# Sales percentile within year + genre
df['sales_percentile_year_genre'] = df.groupby(['year', 'genre'])['global_sales'].rank(pct=True)
print(f"  ✓ sales_percentile_year_genre — percentile within year + genre")

# Whether game is in top 10% of its year
df['is_top10_pct_year'] = (df['sales_percentile_year'] >= 0.9).astype(int)
print(f"  ✓ is_top10_pct_year — top 10% of games that year")

# =============================================================================
# 4. PLATFORM ERA LIFECYCLE
# =============================================================================
print("\n4. Platform Lifecycle")

# Platform launch years (approximate for major platforms)
platform_launch = {
    'PS2': 2000, 'PS3': 2006, 'PS4': 2013, 'PS': 1994, 'PSP': 2004, 'PSV': 2011,
    'Xbox': 2001, 'X360': 2005, 'XOne': 2013,
    'Wii': 2006, 'WiiU': 2012, 'GC': 2001, 'N64': 1996, 'SNES': 1990, 'NES': 1983,
    'DS': 2004, '3DS': 2011, 'GBA': 2001, 'GB': 1989,
    'SAT': 1994, 'DC': 1998, 'GEN': 1988,
    'PC': 1980, '2600': 1977
}
df['platform_age'] = df.apply(lambda r: r['year'] - platform_launch.get(r['platform'], r['year']), axis=1)
df['platform_age'] = df['platform_age'].clip(lower=0)
print(f"  ✓ platform_age — years since platform launch")

# Platform lifecycle stage
def lifecycle(age):
    if age <= 1: return 'launch'
    elif age <= 3: return 'early'
    elif age <= 6: return 'peak'
    elif age <= 10: return 'mature'
    else: return 'decline'

df['platform_lifecycle'] = df['platform_age'].apply(lifecycle)
print(f"  ✓ platform_lifecycle stage: {df['platform_lifecycle'].value_counts().to_dict()}")

# =============================================================================
# 5. SAVE EXPANDED DATASET
# =============================================================================
new_features = sorted(set(df.columns) - orig_cols)
print(f"\n{'='*60}")
print(f"Added {len(new_features)} new features:")
for f in sorted(new_features):
    print(f"  • {f}")

# Save expanded cleaned CSV
expanded_csv = PROCESSED / "video_game_sales_expanded.csv"
df.to_csv(expanded_csv, index=False)
print(f"\n✓ Saved expanded dataset: {expanded_csv}")
print(f"  Dimensions: {df.shape[0]:,} rows × {df.shape[1]} columns")

# =============================================================================
# 6. UPDATE ML FILES
# =============================================================================
print("\n6. Updating ML-ready data")

# Build ML feature list (numeric only)
ml_features_num = [
    'year', 'na_sales', 'eu_sales', 'jp_sales', 'other_sales',
    'na_sales_share', 'eu_sales_share', 'jp_sales_share', 'other_sales_share',
    'publisher_games_count', 'platform_freq', 'name_length',
    'is_top_publisher',
    # NEW features
    'genre_market_share', 'publisher_market_share',
    'games_in_year', 'games_in_year_genre', 'games_in_year_platform',
    'sales_percentile_year', 'sales_percentile_year_genre',
    'is_top10_pct_year', 'platform_age',
]

# Add one-hot columns
genre_cols = sorted([c for c in df.columns if c.startswith('genre_')])
era_cols = sorted([c for c in df.columns if c.startswith('platform_era_')])
lifecycle_cols = sorted([c for c in df.columns if c.startswith('platform_lifecycle_')]) if any(c.startswith('platform_lifecycle_') for c in df.columns) else []

all_features = ml_features_num + genre_cols + era_cols
all_features = [c for c in all_features if c in df.columns]

# Ensure numeric
ml_df = df[all_features].copy()
bool_cols = ml_df.select_dtypes(include=['bool']).columns
for c in bool_cols:
    ml_df[c] = ml_df[c].astype(int)
ml_df = ml_df.astype(float)
ml_df = ml_df.fillna(0)

# Train/test split
X = ml_df
y = df['global_sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pd.DataFrame(X_train_scaled, columns=all_features).to_csv(FEATURES / "X_train_scaled_v2.csv", index=False)
pd.DataFrame(X_test_scaled, columns=all_features).to_csv(FEATURES / "X_test_scaled_v2.csv", index=False)
pd.DataFrame(y_train).to_csv(FEATURES / "y_train_v2.csv", index=False, header=['global_sales'])
pd.DataFrame(y_test).to_csv(FEATURES / "y_test_v2.csv", index=False, header=['global_sales'])
with open(FEATURES / "scaler_v2.pkl", "wb") as f:
    pickle.dump(scaler, f)

print(f"  ✓ Features: {len(all_features)} (was 31)")
print(f"  ✓ Train: {len(X_train):,}  Test: {len(X_test):,}")
print(f"  ✓ Saved as v2 files in features/")

# Update metadata
with open(BASE / "metadata.json") as f:
    meta = json.load(f)

meta["features_for_ml_v2"] = len(all_features)
meta["expanded_features"] = new_features
meta["updated_date"] = str(pd.Timestamp.now())

with open(BASE / "metadata.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"  ✓ Updated metadata.json")

print(f"\n{'='*60}")
print(f"🎮 EXPANSION COMPLETE")
print(f"{'='*60}")
print(f"  Original features: 31")
print(f"  Expanded features: {len(all_features)}")
print(f"  New features added: {len(new_features)}")
print(f"  Files: video_game_sales_expanded.csv + v2 ML files")
