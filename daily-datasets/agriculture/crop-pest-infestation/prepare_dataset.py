#!/usr/bin/env python3
"""
Crop Pest Infestation — Dataset Preparation Pipeline

Downloads raw crop disease images from GitHub Releases if not present locally,
then validates, splits, and prepares for ML image classification.

Raw data release URL:
  https://github.com/AbdoDameen/australian-ml-datasets/releases/download/raw-data-v1/crop_pest_raw.zip

Usage:
  python prepare_dataset.py            # Full pipeline: download → validate → split
  python prepare_dataset.py --skip-dl  # Skip download, just validate + split
"""

import json
import sys
import zipfile
from pathlib import Path
from collections import Counter

import pandas as pd
import requests
from sklearn.model_selection import train_test_split


# ─── Configuration ───────────────────────────────────────────────────────────

DATASET_DIR = Path(__file__).parent.resolve()
RAW_ZIP_URL = (
    "https://github.com/AbdoDameen/australian-ml-datasets/releases/download/"
    "raw-data-v1/crop_pest_raw.zip"
)
RAW_ZIP_PATH = DATASET_DIR / "crop_pest_raw.zip"

EXPECTED_CLASSES = [
    "Cashew anthracnose", "Cashew gumosis", "Cashew healthy", "Cashew leaf miner",
    "Cashew red rust", "Cassava bacterial blight", "Cassava brown spot",
    "Cassava green mite", "Cassava healthy", "Cassava mosaic",
    "Maize fall armyworm", "Maize grasshoper", "Maize healthy", "Maize leaf beetle",
    "Maize leaf blight", "Maize leaf spot", "Maize streak virus",
    "Tomato healthy", "Tomato leaf blight", "Tomato leaf curl",
    "Tomato septoria leaf spot", "Tomato verticulium wilt",
]
MIN_EXPECTED_IMAGES = 10000
RANDOM_STATE = 42


# ─── Step 0: Download ────────────────────────────────────────────────────────

def download_raw_data():
    """Download raw data zip from GitHub Releases and extract into dataset dir."""
    # Check if class dirs already exist with images
    class_dirs = [d for d in DATASET_DIR.iterdir()
                  if d.is_dir() and any(d.glob("*.jpg"))]
    if class_dirs:
        total = sum(1 for _ in DATASET_DIR.rglob("*.jpg"))
        print(f"[✓] Raw data already present: {total} images across "
              f"{len(class_dirs)} class directories")
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
        print(f"[✓] Downloaded to {RAW_ZIP_PATH}")

        # Extract
        print("[→] Extracting...")
        with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zf:
            zf.extractall(path=DATASET_DIR)
        print(f"[✓] Extracted to {DATASET_DIR}")

        # Verify
        image_count = sum(1 for _ in DATASET_DIR.rglob("*.jpg"))
        class_dirs = [d for d in DATASET_DIR.iterdir() if d.is_dir()]
        print(f"[✓] Found {image_count} images across {len(class_dirs)} class directories")
        if image_count < MIN_EXPECTED_IMAGES:
            print(f"[!] Warning: Expected at least {MIN_EXPECTED_IMAGES} images, "
                  f"found {image_count}")

        # Clean up zip
        RAW_ZIP_PATH.unlink(missing_ok=True)
        print("[✓] Cleaned up zip file")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[✗] Download failed: {e}")
        return False
    except zipfile.BadZipFile as e:
        print(f"[✗] Zip extraction failed: {e}")
        return False


# ─── Step 1: Scan & Validate ────────────────────────────────────────────────

def scan_and_validate():
    """Scan class directories and validate the dataset structure."""
    print(f"\n{'='*60}")
    print("  Step 1: Scanning & validating dataset structure")
    print(f"{'='*60}")

    class_dirs = sorted([
        d.name for d in DATASET_DIR.iterdir()
        if d.is_dir() and any(d.glob("*.jpg"))
    ])
    missing_expected = [c for c in EXPECTED_CLASSES if c not in class_dirs]
    total_images = sum(len(list((DATASET_DIR / cd).glob("*.jpg"))) for cd in class_dirs)

    for cd in class_dirs:
        n = len(list((DATASET_DIR / cd).glob("*.jpg")))
        flag = " [!]" if cd in missing_expected else ""
        print(f"    {cd:35s} {n:5d} images{flag}")

    print(f"\n    Total: {total_images} images across {len(class_dirs)} class directories")

    if missing_expected:
        print(f"  [!] Missing expected classes: {missing_expected}")
    else:
        print(f"  [✓] All {len(EXPECTED_CLASSES)} expected classes present")

    if total_images < MIN_EXPECTED_IMAGES:
        print(f"  [!] Only {total_images} images (expected >= {MIN_EXPECTED_IMAGES})")
    else:
        print(f"  [✓] Minimum image count met")
    return True


# ─── Step 2: Summarize ──────────────────────────────────────────────────────

def summarize_metadata():
    """Print dataset summary."""
    print(f"\n{'='*60}")
    print("  Step 2: Dataset Summary")
    print(f"{'='*60}")
    print(f"  ML Task:       Image Classification ({len(EXPECTED_CLASSES)} classes)")
    print(f"  Domain:        Agriculture (Crop Pest Infestation)")
    print(f"  Crops:         Cashew, Cassava, Maize, Tomato")
    print(f"  Source:        DAFF")
    print(f"  Ready for:     PyTorch / TensorFlow classification pipelines")
    return True


# ─── Step 3: Stratified Split ───────────────────────────────────────────────

def generate_splits():
    """Create stratified train (70%) / val (15%) / test (15%) splits as CSVs."""
    print(f"\n{'='*60}")
    print("  Step 3: Generating stratified train/val/test splits")
    print(f"{'='*60}")

    out_dir = DATASET_DIR / "data"
    out_dir.mkdir(exist_ok=True)

    # Scan all images
    records = []
    for cd in sorted(DATASET_DIR.iterdir()):
        if not cd.is_dir():
            continue
        class_name = cd.name
        for img in sorted(cd.glob("*.jpg")):
            records.append({
                "image_path": str(img.relative_to(DATASET_DIR)),
                "label": class_name,
                "crop": class_name.split()[0],
            })

    if not records:
        print("  [✗] No images found. Run download step first.")
        return False

    df = pd.DataFrame(records)
    print(f"  Total images: {len(df)}")

    # Stratified split
    y = df["label"]
    X_train, X_temp, y_train, y_temp = train_test_split(
        df, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y,
    )
    val_ratio = 0.15 / 0.3  # 15% of total → half of the 30% temp
    X_val, X_test, _, _ = train_test_split(
        X_temp, y_temp, test_size=0.15 / 0.3,
        random_state=RANDOM_STATE, stratify=y_temp,
    )

    X_train["split"] = "train"
    X_val["split"] = "val"
    X_test["split"] = "test"

    print(f"  Train: {len(X_train):>6} ({100*len(X_train)/len(df):.1f}%)")
    print(f"  Val:   {len(X_val):>6} ({100*len(X_val)/len(df):.1f}%)")
    print(f"  Test:  {len(X_test):>6} ({100*len(X_test)/len(df):.1f}%)")

    # Save CSVs
    X_train.to_csv(out_dir / "train.csv", index=False)
    X_val.to_csv(out_dir / "val.csv", index=False)
    X_test.to_csv(out_dir / "test.csv", index=False)
    pd.concat([X_train, X_val, X_test]).to_csv(out_dir / "all_splits.csv", index=False)

    # Class labels
    all_classes = sorted(df["label"].unique())
    class_labels = {i: name for i, name in enumerate(all_classes)}
    with open(out_dir / "class_labels.json", "w") as f:
        json.dump(class_labels, f, indent=2)

    # Dataset stats
    stats = {
        "total_images": len(df),
        "num_classes": len(all_classes),
        "classes": all_classes,
        "crops": sorted(df["crop"].unique()),
        "splits": {
            "train": {"count": len(X_train), "pct": round(100*len(X_train)/len(df), 1)},
            "val":   {"count": len(X_val),   "pct": round(100*len(X_val)/len(df), 1)},
            "test":  {"count": len(X_test),  "pct": round(100*len(X_test)/len(df), 1)},
        },
        "class_distribution": {
            cls: {
                "total": int((df["label"] == cls).sum()),
                "train": int((X_train["label"] == cls).sum()),
                "val":   int((X_val["label"] == cls).sum()),
                "test":  int((X_test["label"] == cls).sum()),
            }
            for cls in all_classes
        },
    }
    with open(out_dir / "dataset_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\n  [✓] Splits saved to {out_dir.resolve()}")
    return True


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"{'='*60}")
    print("  Crop Pest Infestation — Dataset Preparation Pipeline")
    print(f"{'='*60}")
    print(f"  Dataset: {DATASET_DIR}")
    print(f"  ML Task: Image Classification ({len(EXPECTED_CLASSES)} classes)")

    if "--skip-dl" not in sys.argv:
        if not download_raw_data():
            print("[✗] Pipeline aborted: raw data unavailable")
            sys.exit(1)
    else:
        print("[→] Skipping download (--skip-dl)")

    scan_and_validate()
    summarize_metadata()
    generate_splits()

    print(f"\n{'='*60}")
    print("  Pipeline complete! Data is ready for ML training.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
