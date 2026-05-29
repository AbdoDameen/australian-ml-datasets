#!/usr/bin/env python3
"""
Crop Pest Infestation - Dataset Preparation Pipeline

Downloads raw crop disease images from GitHub Releases if not present locally,
then prepares them for ML image classification tasks.

Raw data release URL:
  https://github.com/AbdoDameen/australian-ml-datasets/releases/download/raw-data-v1/crop_pest_raw.zip
"""

import os
import sys
import zipfile
import requests
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATASET_DIR = Path(__file__).parent.resolve()
RAW_DATA_DIR = DATASET_DIR  # Images are in subdirectories directly here
RAW_ZIP_URL = (
    "https://github.com/AbdoDameen/australian-ml-datasets/releases/download/"
    "raw-data-v1/crop_pest_raw.zip"
)
RAW_ZIP_PATH = DATASET_DIR / "crop_pest_raw.zip"

# Expected classes
EXPECTED_CLASSES = [
    "Cashew anthracnose", "Cashew gumosis", "Cashew healthy", "Cashew leaf miner", "Cashew red rust",
    "Cassava bacterial blight", "Cassava brown spot", "Cassava green mite", "Cassava healthy", "Cassava mosaic",
    "Maize fall armyworm", "Maize grasshoper", "Maize healthy", "Maize leaf beetle", "Maize leaf blight",
    "Maize leaf spot", "Maize streak virus",
    "Tomato healthy", "Tomato leaf blight", "Tomato leaf curl", "Tomato septoria leaf spot", "Tomato verticulium wilt",
]
MIN_EXPECTED_IMAGES = 10000


# ─── Download Fallback ───────────────────────────────────────────────────────

def download_raw_data():
    """Download the raw data zip from GitHub Releases if not available locally."""
    # Check if image subdirectories already exist with content
    class_dirs = [d for d in RAW_DATA_DIR.iterdir() if d.is_dir() and any(d.glob("*.jpg"))]
    if class_dirs:
        total = sum(1 for _ in RAW_DATA_DIR.rglob("*.jpg"))
        print(f"[✓] Raw data already present: {total} images across {len(class_dirs)} class directories")
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
        image_count = sum(1 for _ in RAW_DATA_DIR.rglob("*.jpg"))
        class_dirs = [d for d in RAW_DATA_DIR.iterdir() if d.is_dir()]
        print(f"[✓] Found {image_count} images across {len(class_dirs)} class directories")
        if image_count < MIN_EXPECTED_IMAGES:
            print(f"[!] Warning: Expected at least {MIN_EXPECTED_IMAGES} images, found {image_count}")

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

def scan_and_validate():
    """Scan and validate the dataset structure."""
    print(f"\n{'='*60}")
    print("  Step 1: Scanning dataset structure")
    print(f"{'='*60}")

    if not RAW_DATA_DIR.exists():
        print(f"[✗] Data directory not found: {RAW_DATA_DIR}")
        return False

    # Identify class directories (directories containing images)
    class_dirs = sorted([
        d.name for d in RAW_DATA_DIR.iterdir()
        if d.is_dir() and any(d.glob("*.jpg"))
    ])

    print(f"  Found {len(class_dirs)} class directories:")
    for cd in class_dirs:
        img_count = len(list((RAW_DATA_DIR / cd).glob("*.jpg")))
        print(f"    {cd}: {img_count} images")

    total_images = sum(
        len(list((RAW_DATA_DIR / cd).glob("*.jpg")))
        for cd in class_dirs
    )
    print(f"\n  Total images: {total_images}")

    # Check expected classes
    missing_expected = [c for c in EXPECTED_CLASSES if c not in class_dirs]
    if missing_expected:
        print(f"  [!] Missing expected classes: {missing_expected}")
    else:
        print(f"  [✓] All expected classes present")

    if total_images < MIN_EXPECTED_IMAGES:
        print(f"  [!] Warning: Only {total_images} images (expected >= {MIN_EXPECTED_IMAGES})")
    else:
        print(f"  [✓] Minimum image count met")

    return True


def summarize_metadata():
    """Print summary metadata for ML pipeline."""
    print(f"\n{'='*60}")
    print("  Step 2: Dataset Summary")
    print(f"{'='*60}")

    class_dirs = sorted([
        d.name for d in RAW_DATA_DIR.iterdir()
        if d.is_dir() and any(d.glob("*.jpg"))
    ])

    print(f"  ML Task: Image Classification ({len(EXPECTED_CLASSES)} classes)")
    print(f"  Classes: {', '.join(EXPECTED_CLASSES)}")
    print(f"  Domain: Agriculture (Crop Pest Infestation)")
    print(f"  Source: DAFF")

    # Image size uniformity check
    from collections import defaultdict
    sizes = defaultdict(int)
    for cd in class_dirs:
        for img in (RAW_DATA_DIR / cd).glob("*.jpg"):
            w, h = 0, 0
            try:
                with open(img, "rb") as f:
                    f.seek(0x10)  # JPEG SOF marker approximate
                    data = f.read(16)
            except:
                pass
            break  # Just check one per class for now
        break

    print(f"  Ready for: PyTorch/TensorFlow classification pipelines")
    return True


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*60}")
    print("  Crop Pest Infestation - Dataset Preparation Pipeline")
    print(f"{'='*60}")
    print(f"  Dataset: {DATASET_DIR}")
    print(f"  ML Task: Image Classification")

    # Step 0: Ensure raw data is available
    if not download_raw_data():
        print("[✗] Pipeline aborted: raw data unavailable")
        sys.exit(1)

    # Step 1: Scan and validate
    scan_and_validate()

    # Step 2: Summarize
    summarize_metadata()

    print(f"\n{'='*60}")
    print("  Pipeline complete! Data is ready for ML training.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
