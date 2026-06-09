#!/usr/bin/env python3
"""
Crop Yields (Global) — Dataset Preparation Pipeline

Downloads raw GeoTIFF rasters from GitHub Releases, extracts Australian
agricultural pixel values, creates a tabular ML dataset with temporal and
spatial features, and prepares train/test splits.

Raw data release URL:
  https://github.com/AbdoDameen/australian-ml-datasets/releases/download/raw-data-v1/crop_yields_raw.zip

Usage:
  python prepare_dataset.py              # Full pipeline
  python prepare_dataset.py --skip-dl    # Skip download, process only
"""

import json
import pickle
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    import rasterio
except ImportError:
    print("[✗] rasterio not found. Install: pip install rasterio")
    sys.exit(1)


# ─── Configuration ───────────────────────────────────────────────────────────

DATASET_DIR = Path(__file__).parent.resolve()
PROCESSED = DATASET_DIR / "processed"
FEATURES = DATASET_DIR / "features"
RAW_DIR = DATASET_DIR / "GlobalCropYield5min_V3"

RAW_ZIP_URL = (
    "https://github.com/AbdoDameen/australian-ml-datasets/releases/download/"
    "raw-data-v1/crop_yields_raw.zip"
)
RAW_ZIP_PATH = DATASET_DIR / "crop_yields_raw.zip"

EXPECTED_TIF_COUNT = 136  # 4 crops × 34 years
RANDOM_STATE = 42

# Australia bounding box
AUS_LON_MIN, AUS_LON_MAX = 112, 155
AUS_LAT_MIN, AUS_LAT_MAX = -45, -10


# ─── Step 0: Download ────────────────────────────────────────────────────────

def download_raw_data():
    """Download raw data zip from GitHub Releases and extract."""
    if RAW_DIR.exists() and any(RAW_DIR.rglob("*.tif")):
        existing = sum(1 for _ in RAW_DIR.rglob("*.tif"))
        print(f"[✓] Raw data already present: {existing} GeoTIFFs")
        return True

    print("[→] Raw data not found locally. Downloading from GitHub Releases...")
    print(f"    URL: {RAW_ZIP_URL}")

    try:
        response = requests.get(RAW_ZIP_URL, stream=True, timeout=300)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(RAW_ZIP_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    pct = downloaded * 100 / total_size
                    print(f"\r    Downloading: {downloaded // (1024*1024)} MB / "
                          f"{total_size // (1024*1024)} MB ({pct:.0f}%)", end="")
        print()

        print("[→] Extracting...")
        with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zf:
            zf.extractall(path=DATASET_DIR)
        print(f"[✓] Extracted to {DATASET_DIR}")

        tif_count = sum(1 for _ in RAW_DIR.rglob("*.tif"))
        print(f"[✓] Found {tif_count} GeoTIFF files (expected {EXPECTED_TIF_COUNT})")
        RAW_ZIP_PATH.unlink(missing_ok=True)
        return True

    except requests.exceptions.RequestException as e:
        print(f"[✗] Download failed: {e}")
        return False
    except zipfile.BadZipFile as e:
        print(f"[✗] Zip extraction failed: {e}")
        return False


# ─── Step 1: Extract Australian Pixels ───────────────────────────────────────

def extract_australia_pixels():
    """
    Extract Australian agricultural pixel values from all crop/year GeoTIFFs.

    Returns a DataFrame with columns: crop, year, latitude, longitude, yield_kg_ha
    """
    print(f"\n{'='*60}")
    print("  Step 1: Extracting Australian agricultural pixels")
    print(f"{'='*60}")

    records = []

    for crop_dir in sorted(RAW_DIR.iterdir()):
        if not crop_dir.is_dir():
            continue
        crop = crop_dir.name
        tifs = sorted(crop_dir.glob("*.tif"))
        if not tifs:
            continue

        with rasterio.open(tifs[0]) as src:
            if src.bounds.right < AUS_LON_MIN:
                print(f"  {crop}: does not reach Australia (right={src.bounds.right:.1f}°E)")
                continue

            cap_lon = min(AUS_LON_MAX, src.bounds.right)
            col_start = int((AUS_LON_MIN - src.bounds.left) / abs(src.transform[0]))
            col_end = int((cap_lon - src.bounds.left) / abs(src.transform[0]))
            row_start = int((src.bounds.top - AUS_LAT_MAX) / abs(src.transform[4]))
            row_end = int((src.bounds.top - AUS_LAT_MIN) / abs(src.transform[4]))

            # Build (lat, lon) lookup for each pixel in the Australia slice
            lons = np.arange(col_start, col_end) * abs(src.transform[0]) + src.bounds.left
            lats = np.arange(row_start, row_end) * abs(src.transform[4])
            lats = src.bounds.top - lats  # Convert from pixel offset to actual latitude

        print(f"  {crop}: scanning {col_end - col_start}×{row_end - row_start} "
              f"Australia slice across {len(tifs)} years...")

        for tif in tifs:
            year = tif.stem.replace(crop, "")
            with rasterio.open(tif) as src:
                data = src.read(1)
                slice_data = data[row_start:row_end, col_start:col_end]

            for i in range(slice_data.shape[0]):
                for j in range(slice_data.shape[1]):
                    val = slice_data[i, j]
                    if not np.isnan(val):
                        records.append({
                            "crop": crop.lower(),
                            "year": int(year),
                            "latitude": round(float(lats[i]), 4),
                            "longitude": round(float(lons[j]), 4),
                            "yield_kg_ha": round(float(val), 2),
                        })

            if records and len(records) % 50000 == 0:
                print(f"    ... {len(records):,} records extracted so far")

    df = pd.DataFrame(records)
    print(f"\n  [✓] Extracted {len(df):,} records across {df['crop'].nunique() if len(df) else 0} crops")

    if len(df):
        for crop_name in df['crop'].unique():
            sub = df[df['crop'] == crop_name]
            print(f"      {crop_name}: {len(sub):,} rows, "
                  f"yield {sub['yield_kg_ha'].min():.0f}–{sub['yield_kg_ha'].max():.0f} kg/ha")

    return df


# ─── Step 2: Clean Data ──────────────────────────────────────────────────────

def clean_data(df):
    """
    Clean the extracted dataset: deduplicate, handle outliers, standardise names.
    """
    print(f"\n{'='*60}")
    print("  Step 2: Cleaning data")
    print(f"{'='*60}")

    before = len(df)

    # Drop duplicates (same crop, year, lat, lon)
    df = df.drop_duplicates(subset=["crop", "year", "latitude", "longitude"])
    print(f"  Duplicates removed: {before - len(df)}")

    # Remove impossible yield values (negative or zero)
    before2 = len(df)
    df = df[df["yield_kg_ha"] > 0]
    print(f"  Zero/negative yields removed: {before2 - len(df)}")

    # Outlier treatment via IQR (per crop)
    before3 = len(df)
    cleaned = []
    for crop_name in df["crop"].unique():
        sub = df[df["crop"] == crop_name].copy()
        q1 = sub["yield_kg_ha"].quantile(0.25)
        q3 = sub["yield_kg_ha"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 3 * iqr
        upper = q3 + 3 * iqr
        before_sub = len(sub)
        sub = sub[(sub["yield_kg_ha"] >= lower) & (sub["yield_kg_ha"] <= upper)]
        cleaned.append(sub)
        print(f"  {crop_name}: IQR outliers removed: {before_sub - len(sub)} "
              f"({lower:.0f}–{upper:.0f} kg/ha)")

    df = pd.concat(cleaned, ignore_index=True)
    print(f"  Total rows after cleaning: {len(df):,}")
    return df


# ─── Step 3: Feature Engineering ─────────────────────────────────────────────

def engineer_features(df):
    """
    Add temporal and spatial features for ML.
    """
    print(f"\n{'='*60}")
    print("  Step 3: Feature engineering")
    print(f"{'='*60}")

    # Temporal features
    df["year_since_1982"] = df["year"] - 1982
    df["decade"] = (df["year"] // 10) * 10

    # Seasonal features (southern hemisphere)
    df["is_drought_year"] = df["year"].isin([1982, 2002, 2003, 2006, 2007, 2015]).astype(int)

    # Spatial features
    df["abs_latitude"] = df["latitude"].abs()

    # Agricultural zone (simplified Australian climate bands)
    df["climate_zone"] = pd.cut(
        df["abs_latitude"],
        bins=[0, 15, 25, 35, 45, 90],
        labels=["tropical", "subtropical", "temperate", "cool_temperate", "alpine"],
    )

    # Encode climate zone
    df = pd.get_dummies(df, columns=["climate_zone"], prefix="zone")

    # One-hot encode crop
    df = pd.get_dummies(df, columns=["crop"], prefix="crop")

    # Convert bool to int
    for c in df.select_dtypes(include=["bool"]).columns:
        df[c] = df[c].astype(int)

    print(f"  Temporal: year_since_1982, decade, is_drought_year")
    print(f"  Spatial:  abs_latitude, climate_zone (one-hot)")
    print(f"  Categorical: crop (one-hot)")
    print(f"  Feature count: {len([c for c in df.columns if c not in ['yield_kg_ha', 'latitude', 'longitude', 'year', 'decade']])}")

    return df


# ─── Step 4: ML Preparation ──────────────────────────────────────────────────

def prepare_ml(df):
    """
    Split, scale, and save ML-ready files.
    """
    print(f"\n{'='*60}")
    print("  Step 4: Preparing ML-ready files")
    print(f"{'='*60}")

    FEATURES.mkdir(parents=True, exist_ok=True)

    # Feature columns (exclude target + id + raw spatial/temporal)
    exclude = {"yield_kg_ha", "latitude", "longitude", "year", "decade"}
    feature_cols = [c for c in df.columns if c not in exclude]
    target_col = "yield_kg_ha"

    X = df[feature_cols].select_dtypes(include=[np.number])
    y = df[target_col]

    print(f"  Features: {X.shape[1]}")
    print(f"  Target:   {target_col}")
    print(f"  Total samples: {len(df):,}")

    # Train/test split (80/20, shuffle=False for spatial consistency)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE,
    )

    print(f"  Train: {len(X_train):,} samples")
    print(f"  Test:  {len(X_test):,} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save
    np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
    np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
    np.savetxt(FEATURES / "y_train.csv", y_train.values, delimiter=",")
    np.savetxt(FEATURES / "y_test.csv", y_test.values, delimiter=",")

    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Save feature names
    with open(FEATURES / "feature_names.json", "w") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"  [✓] ML files saved to {FEATURES.resolve()}")
    return True


# ─── Step 5: Save Cleaned CSV & Metadata ─────────────────────────────────────

def save_outputs(df):
    """
    Save the cleaned tabular dataset and generate metadata.
    """
    print(f"\n{'='*60}")
    print("  Step 5: Saving outputs")
    print(f"{'='*60}")

    PROCESSED.mkdir(parents=True, exist_ok=True)

    # Save cleaned CSV
    csv_path = PROCESSED / "crop_yields_australia_clean.csv"
    df.to_csv(csv_path, index=False)
    print(f"  [✓] Cleaned CSV: {csv_path} ({csv_path.stat().st_size / 1024 / 1024:.1f} MB)")

    # Build metadata
    crop_cols = [c for c in df.columns if c.startswith("crop_")]
    crops_present = [c.replace("crop_", "") for c in crop_cols if df[c].sum() > 0]

    metadata = {
        "name": "Crop Yields (Global) — Australian Extract",
        "domain": "Agriculture",
        "ml_task": "Regression (predict crop yield in kg/ha)",
        "source": "SAGE / UW-Madison Global Crop Yield Dataset (5-minute resolution)",
        "source_url": "https://sage.nelson.wisc.edu/data-and-models/datasets/global-crop-yield-dataset-5-minute-resolution/",
        "australia_bounds": {
            "longitude": [AUS_LON_MIN, AUS_LON_MAX],
            "latitude": [AUS_LAT_MIN, AUS_LAT_MAX],
        },
        "crops_in_australia": crops_present,
        "temporal_range": {"start": int(df["year"].min()), "end": int(df["year"].max())},
        "total_rows": int(len(df)),
        "columns": [
            {"name": "crop_*", "type": "int (one-hot)", "description": "Binary indicator for each crop (maize, rice, wheat)"},
            {"name": "year", "type": "int", "description": "Harvest year (1982–2015)"},
            {"name": "year_since_1982", "type": "int", "description": "Years since 1982 (temporal feature)"},
            {"name": "decade", "type": "int", "description": "Decade grouping"},
            {"name": "is_drought_year", "type": "int (binary)", "description": "Flag for known Australian drought years"},
            {"name": "latitude", "type": "float", "description": "Pixel centroid latitude (EPSG:4326)"},
            {"name": "longitude", "type": "float", "description": "Pixel centroid longitude (EPSG:4326)"},
            {"name": "abs_latitude", "type": "float", "description": "Absolute latitude (spatial feature)"},
            {"name": "zone_*", "type": "int (one-hot)", "description": "Australian climate zone (tropical / subtropical / temperate / cool_temperate)"},
            {"name": "yield_kg_ha", "type": "float", "description": "Target — crop yield in kg per hectare"},
        ],
        "features_ml": {
            "feature_count": len([c for c in df.columns if c not in ["yield_kg_ha", "latitude", "longitude", "year", "decade"]]),
            "scaler": "StandardScaler",
            "test_split": 0.2,
        },
        "transformations": [
            "Extracted Australian pixels from 136 global GeoTIFF rasters",
            "Removed duplicate pixel-year-crop combinations",
            "Removed zero/negative yield values",
            "IQR outlier treatment (3× IQR per crop)",
            "Added temporal features: year_since_1982, decade, is_drought_year",
            "Added spatial features: abs_latitude, climate_zone (one-hot)",
            "Crop type one-hot encoded",
        ],
    }

    with open(PROCESSED / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    print(f"  [✓] Metadata saved")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*60}")
    print("  Crop Yields (Global) — Dataset Preparation Pipeline")
    print(f"{'='*60}")
    print(f"  Dataset: {DATASET_DIR}")
    print(f"  ML Task: Regression (predict crop yields in kg/ha)")

    # Download
    if "--skip-dl" not in sys.argv:
        if not download_raw_data():
            print("[✗] Pipeline aborted: raw data unavailable")
            sys.exit(1)
    else:
        print("[→] Skipping download (--skip-dl)")

    if not RAW_DIR.exists():
        print(f"[✗] Raw data directory not found: {RAW_DIR}")
        sys.exit(1)

    # Extract
    df = extract_australia_pixels()
    if len(df) == 0:
        print("[✗] No Australian pixel data extracted")
        sys.exit(1)

    # Clean
    df = clean_data(df)

    # Feature engineering
    df = engineer_features(df)

    # Save outputs (raw cleaned CSV)
    save_outputs(df)

    # ML prep
    prepare_ml(df)

    print(f"\n{'='*60}")
    print("  Pipeline complete! Data is ready for ML training.")
    print(f"{'='*60}")
    print(f"  Cleaned CSV:    {PROCESSED / 'crop_yields_australia_clean.csv'}")
    print(f"  ML features:    {FEATURES / 'X_train_scaled.csv'} etc.")
    print(f"  Metadata:       {PROCESSED / 'metadata.json'}")


if __name__ == "__main__":
    main()
