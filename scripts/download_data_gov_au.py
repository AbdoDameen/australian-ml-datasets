#!/usr/bin/env python3
"""
Download datasets from data.gov.au via CKAN API.

Most Australian government datasets are published on data.gov.au with
a CKAN API. No API key needed for public datasets.

Usage:
  python download_data_gov_au.py --search beachwatch          # Search datasets
  python download_data_gov_au.py --dataset <id>               # Download by ID
  python download_data_gov_au.py --dataset all --domain water # Batch download
"""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

import requests

BASE = "https://data.gov.au/data/api/3/action"


def search_datasets(query: str, rows: int = 10) -> list[dict]:
    """Search data.gov.au for datasets matching a query."""
    resp = requests.get(f"{BASE}/package_search", params={"q": query, "rows": rows})
    resp.raise_for_status()
    return resp.json()["result"]["results"]


def get_dataset(dataset_id: str) -> dict:
    """Get dataset metadata and resource URLs by ID or slug."""
    resp = requests.get(f"{BASE}/package_show", params={"id": dataset_id})
    resp.raise_for_status()
    return resp.json()["result"]


def download_resource(url: str, output_dir: Path) -> Path:
    """Download a single resource to output_dir, return the local path."""
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    # Try to get a filename from URL or Content-Disposition
    fname = (
        resp.headers.get("Content-Disposition", "").split("filename=")[-1].strip('"')
        or url.split("/")[-1].split("?")[0]
        or "download"
    )
    path = output_dir / fname

    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    return path


def download_dataset(dataset_id: str, output_dir: Path) -> dict:
    """Download all CSVs/Excel resources from a dataset."""
    dataset = get_dataset(dataset_id)
    ds_dir = output_dir / dataset["name"]
    ds_dir.mkdir(parents=True, exist_ok=True)

    # Save metadata
    meta_path = ds_dir / "metadata.json"
    meta = {
        "title": dataset.get("title", ""),
        "id": dataset.get("id", ""),
        "name": dataset.get("name", ""),
        "notes": dataset.get("notes", ""),
        "url": f"https://data.gov.au/dataset/{dataset.get('id', '')}",
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    results = {"dataset": meta, "resources": []}
    for resource in dataset.get("resources", []):
        fmt = resource.get("format", "").upper()
        if fmt not in ("CSV", "XLS", "XLSX", "JSON"):
            continue
        url = resource.get("url", "")
        if not url:
            continue
        try:
            path = download_resource(url, ds_dir)
            results["resources"].append({
                "name": resource.get("name", ""),
                "format": fmt,
                "path": str(path),
                "size": path.stat().st_size,
            })
            print(f"  [✓] {resource.get('name', '')} ({fmt}) → {path.name}")
        except Exception as e:
            print(f"  [✗] {resource.get('name', '')}: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Download datasets from data.gov.au")
    parser.add_argument("--search", help="Search for datasets by keyword")
    parser.add_argument("--dataset", help="Dataset ID or name to download (or 'all')")
    parser.add_argument("--domain", help="Domain filter when --dataset all (optional)")
    parser.add_argument("--output", default="./data/data_gov_au", help="Output directory")
    parser.add_argument("--rows", type=int, default=10, help="Max search results")
    args = parser.parse_args()

    out_dir = Path(args.output)

    if args.search:
        results = search_datasets(args.search, args.rows)
        print(f"\nFound {len(results)} datasets:\n")
        for i, ds in enumerate(results, 1):
            print(f"  {i:3d}. {ds['title']}")
            print(f"       ID: {ds['id']}")
            print(f"       URL: https://data.gov.au/dataset/{ds['id']}")
            print(f"       Updated: {ds.get('metadata_modified', '')[:10]}")
            print()

    elif args.dataset:
        if args.dataset == "all":
            # Search for Australian datasets by domain
            query = f"Australia {args.domain or ''}".strip()
            results = search_datasets(query, args.rows)
            print(f"Downloading up to {len(results)} datasets matching '{query}'...")
            for ds in results:
                print(f"\n📦 {ds['title']}")
                try:
                    download_dataset(ds["id"], out_dir)
                except Exception as e:
                    print(f"  [✗] Failed: {e}")
        else:
            download_dataset(args.dataset, out_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
