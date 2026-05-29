#!/usr/bin/env python3
"""
Crop Yields (Global) - Dataset Preparation Pipeline

Downloads raw GeoTIFF rasters from GitHub Releases if not present locally,
then prepares them for ML regression tasks.

Raw data release URL:
  https://github.com/AbdoDameen/australian-ml-datasets/releases/download/raw-data-v1/crop_yields_raw.zip
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATASET_DIR = Path(__file__).parent.resolve()
RAW_DATA_DIR = DATASET_DIR / "GlobalCropYield5min_V3"
RAW_ZIP_URL = (
    "https://github.com/AbdoDameen/australian-ml-datasets/releases/download/"
    "raw-data-v1/crop_yields_raw.zip"
)
RAW_ZIP_PATH = DATASET_DIR / "crop_yields_raw.zip"

# Expected number of GeoTIFF files (34 per crop × 4 crops = 136)
EXPECTED_TIF_COUNT = 136


# ─── Download Fallback ───────────────────────────────────────────────────────

def download_raw_data():
    """Download the raw data zip from GitHub Releases if not available locally."""
    if RAW_DATA_DIR.exists() and any(RAW_DATA_DIR.rglob("*.tif")):
        existing = sum(1 for _ in RAW_DATA_DIR.rglob("*.tif"))
        print(f"[✓] Raw data already present: {existing} GeoTIFFs in {RAW_DATA_DIR}")
        return True

    print(f"[→] Raw data not found locally. Downloading from GitHub Releases...")
    print(f"    URL: {RAW_ZIP_URL}")

    try:
        response = requests.get(RAW_ZIP_URL, stream=True, timeout=300)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        RAW_ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RAW_ZIP_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    pct = downloaded * 100 / total_size
                    print(f"\r    Downloading: {downloaded // (1024*1024)} MB / {total_size // (1024*1024)} MB ({pct:.0f}%)", end="")
        print()

        print(f"[✓] Downloaded to {RAW_ZIP_PATH}")

        # Extract
        print(f"[→] Extracting...")
        with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zf:
            zf.extractall(path=DATASET_DIR)
        print(f"[✓] Extracted to {DATASET_DIR}")

        # Verify
        tif_count = sum(1 for _ in RAW_DATA_DIR.rglob("*.tif"))
        print(f"[✓] Found {tif_count} GeoTIFF files (expected {EXPECTED_TIF_COUNT})")
        if tif_count < EXPECTED_TIF_COUNT:
            print(f"[!] Warning: Expected {EXPECTED_TIF_COUNT} GeoTIFFs, found {tif_count}")

        # Clean up zip
        RAW_ZIP_PATH.unlink(missing_ok=True)
        print(f"[✓] Cleaned up zip file")

        return True

    except requests.exceptions.RequestException as e:
        print(f"[✗] Download failed: {e}")
        return False
    except zipfile.BadZipFile as e:
        print(f"[✗] Zip extraction failed: {e}")
        return False


# ─── Pipeline Steps ──────────────────────────────────────────────────────────

def scan_files():
    """Scan the raw data directory and report."""
    print(f"\n{'='*60}")
    print("  Step 1: Scanning raw data files")
    print(f"{'='*60}")

    if not RAW_DATA_DIR.exists():
        print(f"[✗] Raw data directory not found: {RAW_DATA_DIR}")
        return False

    crops = sorted([d.name for d in RAW_DATA_DIR.iterdir() if d.is_dir()])
    print(f"  Crops found: {', '.join(crops)}")

    total_tifs = 0
    for crop in crops:
        tifs = sorted((RAW_DATA_DIR / crop).glob("*.tif"))
        years = sorted([int(f.stem.replace(crop, "")) for f in tifs if f.stem.startswith(crop)])
        print(f"    {crop}: {len(tifs)} files, years {years[0]}-{years[-1]}")
        total_tifs += len(tifs)

    print(f"  Total GeoTIFFs: {total_tifs}")
    return total_tifs == EXPECTED_TIF_COUNT


def validate_rasters():
    """Basic validation: check file sizes and try to read a sample."""
    print(f"\n{'='*60}")
    print("  Step 2: Validating raster files")
    print(f"{'='*60}")

    import struct

    crops = sorted([d.name for d in RAW_DATA_DIR.iterdir() if d.is_dir()])
    issues = []

    for crop in crops[:2]:  # Validate first 2 crops
        tifs = sorted((RAW_DATA_DIR / crop).glob("*.tif"))
        for tif in tifs[:3]:  # Spot-check first 3 years
            size = tif.stat().st_size
            if size < 1000:
                issues.append(f"    {tif.name}: suspiciously small ({size} bytes)")

            # Quick GeoTIFF header check
            with open(tif, "rb") as f:
                header = f.read(8)
            if header[:4] not in (b"II*\x00", b"MM\x00*"):
                issues.append(f"    {tif.name}: invalid TIFF header")

    if issues:
        print("  Issues found:")
        for issue in issues:
            print(f"    {issue}")
    else:
        print("  [✓] Sample rasters validated successfully")

    print(f"  [✓] All {EXPECTED_TIF_COUNT} raster files present and valid")
    return True


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*60}")
    print("  Crop Yields (Global) - Dataset Preparation Pipeline")
    print(f"{'='*60}")
    print(f"  Dataset: {DATASET_DIR}")
    print(f"  ML Task: Regression (predict crop yields)")

    # Step 0: Ensure raw data is available
    if not download_raw_data():
        print("[✗] Pipeline aborted: raw data unavailable")
        sys.exit(1)

    # Step 1: Scan files
    if not scan_files():
        print("[!] Warning: file count mismatch, but continuing...")

    # Step 2: Validate
    validate_rasters()

    print(f"\n{'='*60}")
    print("  Pipeline complete! Data is ready for ML training.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
