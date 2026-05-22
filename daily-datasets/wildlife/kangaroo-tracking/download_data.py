#!/usr/bin/env python3
"""Download kangaroo dataset images + annotations from GitHub."""
import json
import urllib.request
import sys
from pathlib import Path

RAW = Path("/home/abdodameen/australian-ml-datasets/daily-datasets/wildlife/kangaroo-tracking/raw")
IMG_DIR = RAW / "images"
ANN_DIR = RAW / "annots"

BASE_URL = "https://raw.githubusercontent.com/experiencor/kangaroo/master"


def fetch_list(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Python"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def download_file(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Python"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        dest.write_bytes(data)
        return len(data)
    except Exception as e:
        print(f"  FAIL: {url.split('/')[-1]} — {e}")
        return 0


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    ANN_DIR.mkdir(parents=True, exist_ok=True)

    # Get file lists from API
    print("Fetching file lists...")
    images = fetch_list("https://api.github.com/repos/experiencor/kangaroo/contents/images")
    annots = fetch_list("https://api.github.com/repos/experiencor/kangaroo/contents/annots")

    img_names = [f["name"] for f in images if f["type"] == "file"]
    ann_names = [f["name"] for f in annots if f["type"] == "file"]

    print(f"Images: {len(img_names)}  Annotations: {len(ann_names)}")

    # Download images
    print("\nDownloading images...")
    img_count = 0
    img_bytes = 0
    for name in img_names:
        url = f"{BASE_URL}/images/{name}"
        dest = IMG_DIR / name
        if dest.exists():
            img_bytes += dest.stat().st_size
            img_count += 1
            continue
        size = download_file(url, dest)
        if size:
            img_count += 1
            img_bytes += size
        if img_count % 50 == 0:
            print(f"  {img_count}/{len(img_names)} images...")

    # Download annotations
    print("\nDownloading annotations...")
    ann_count = 0
    for name in ann_names:
        url = f"{BASE_URL}/annots/{name}"
        dest = ANN_DIR / name
        if not dest.exists():
            download_file(url, dest)
        ann_count += 1
        if ann_count % 50 == 0:
            print(f"  {ann_count}/{len(ann_names)} annots...")

    total_mb = img_bytes / (1024 * 1024)
    print(f"\n=== Done ===")
    print(f"Images: {img_count} ({total_mb:.1f} MB)")
    print(f"Annotations: {ann_count}")
    print(f"Image dir: {IMG_DIR}")
    print(f"Annot dir: {ANN_DIR}")

    # Quick sample of annotation structure
    if ann_names:
        sample = ANN_DIR / ann_names[0]
        print(f"\nSample annotation ({ann_names[0]}):")
        print(sample.read_text()[:500])


if __name__ == "__main__":
    main()
