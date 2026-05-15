#!/usr/bin/env python3
"""
Australian Car Market Dataset — Standardised Pipeline
======================================================
Loads raw CSV, cleans, engineer features, and saves processed data + ML features.
"""

import csv
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
RAW_PATH = Path("raw/australian_car_market_clean.csv")
PROCESSED_DIR = Path("processed")
FEATURES_DIR = Path("features")
TARGET_DIR = Path(".")

# Output filenames
CLEAN_CSV = "australian_car_market_clean_processed.csv"
CLEAN_PARQUET = "australian_car_market_clean_processed.parquet"
FEATURES_CSV = "ml_features.csv"
FEATURES_PARQUET = "ml_features.parquet"
SCALER_META = "scaler_params.json"
FEATURE_NAMES = "feature_names.json"

RNG_SEED = 42

# Price brackets (AUD) — based on median ~30K
PRICE_BINS = [0, 15000, 30000, 50000, 80000, float("inf")]
PRICE_LABELS = ["budget", "economy", "mid_range", "premium", "luxury"]

# Odometer categories (km)
ODO_BINS = [0, 20000, 60000, 120000, 200000, float("inf")]
ODO_LABELS = ["low", "moderate", "average", "high", "very_high"]

# Decade mapping
DECADES = {
    1980: "1980s", 1990: "1990s", 2000: "2000s",
    2010: "2010s", 2020: "2020s",
}

# Columns to keep in processed output
PROCESSED_COLUMNS = [
    "id", "brand", "model", "variant", "series",
    "year", "decade", "price", "price_bracket",
    "kilometers", "odometer_category", "type", "gearbox",
    "fuel", "status", "cc", "color", "seating_capacity",
]

# Columns for ML features (numeric after encoding)
TARGET_COLUMN = "price"
ML_FEATURE_COLUMNS = [
    "year", "kilometers", "cc", "seating_capacity",
    "decade_1980s", "decade_1990s", "decade_2000s",
    "decade_2010s", "decade_2020s",
    "gearbox_Automatic", "gearbox_Manual",
    "fuel_Diesel", "fuel_Premium Unleaded Petrol", "fuel_Unleaded Petrol",
    "fuel_Premium Unleaded/Electric", "fuel_Unleaded Petrol/Electric",
    "status_Demo", "status_New In Stock", "status_Used",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _clean_price(val: str) -> float | None:
    """Parse price — strip $, commas, 'POA', etc."""
    v = val.strip().upper()
    v = re.sub(r"[$,]", "", v)
    if v in ("", "POA", "N/A", "0"):
        return None
    try:
        p = float(v)
        return p if p >= 500 else None  # sensible lower bound
    except ValueError:
        return None


def _clean_kilometers(val: str) -> float | None:
    """Parse odometer — handle 'km', commas, etc."""
    v = val.strip().lower()
    v = re.sub(r"[km,\s]", "", v)
    if v in ("", "0", "n/a"):
        return None
    try:
        k = float(v)
        return k if 1 <= k <= 3_000_000 else None
    except ValueError:
        return None


def _clean_year(val: str) -> int | None:
    """Parse year — must be 1950–2025."""
    try:
        y = int(float(val.strip()))
        return y if 1950 <= y <= 2025 else None
    except (ValueError, TypeError):
        return None


def _clean_cc(val: str) -> float | None:
    """Parse engine capacity."""
    v = val.strip()
    if v in ("", "0", "N/A", "n/a"):
        return None
    try:
        cc = float(v)
        return cc if 500 <= cc <= 10000 else None
    except ValueError:
        return None


def _clean_seating(val: str) -> int | None:
    """Parse seating capacity."""
    v = val.strip()
    if v in ("", "0", "N/A", "n/a"):
        return None
    try:
        s = int(float(v))
        return s if 1 <= s <= 20 else None
    except (ValueError, TypeError):
        return None


def _clean_brand(val: str) -> str:
    """Normalise brand name."""
    v = val.strip().title()
    # Common normalisations
    mappings = {
        "Merc-Benz": "Mercedes-Benz",
        "Mercedes Benz": "Mercedes-Benz",
        "Range Rover": "Land Rover",
        "Alfa Romeo": "Alfa Romeo",
        "Aston Martin": "Aston Martin",
    }
    return mappings.get(v, v)


def _clean_color(val: str) -> str:
    """Normalise colour."""
    v = val.strip().title()
    standard = {"White", "Black", "Silver", "Grey", "Gray", "Blue",
                 "Red", "Green", "Gold", "Bronze", "Orange", "Purple",
                 "Yellow", "Brown", "Beige", "Navy", "Charcoal"}
    for s in standard:
        if s.lower() == v.lower() or s.lower() in v.lower():
            return s
    return v


def _decade(year: int) -> str:
    """Map year to decade."""
    base = (year // 10) * 10
    # clamp to defined decades
    for k in sorted(DECADES):
        if base <= k:
            return DECADES[k]
    return DECADES[sorted(DECADES)[-1]]


def _price_bracket(price: float) -> str:
    for i, upper in enumerate(PRICE_BINS[1:]):
        if price <= upper:
            return PRICE_LABELS[i]
    return PRICE_LABELS[-1]


def _odometer_category(km: float) -> str:
    for i, upper in enumerate(ODO_BINS[1:]):
        if km <= upper:
            return ODO_LABELS[i]
    return ODO_LABELS[-1]


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline():
    print("=" * 60)
    print("Australian Car Market — Data Preparation Pipeline")
    print("=" * 60)

    # ---- 1. Load raw ----
    print(f"\n[1/6] Loading raw data from {RAW_PATH}")
    with open(RAW_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
    print(f"       Loaded {len(raw_rows)} rows, {len(reader.fieldnames)} columns")

    # ---- 2. Clean ----
    print("\n[2/6] Cleaning data")
    clean_rows = []
    stats = Counter()
    for row in raw_rows:
        rec = dict(row)

        # Parse numeric fields
        price = _clean_price(rec.get("price", ""))
        kms = _clean_kilometers(rec.get("kilometers", ""))
        year = _clean_year(rec.get("year", ""))
        cc = _clean_cc(rec.get("cc", ""))
        seats = _clean_seating(rec.get("seating_capacity", ""))

        # Skip if essential fields missing
        if price is None:
            stats["dropped_no_price"] += 1
            continue
        if year is None:
            stats["dropped_no_year"] += 1
            continue

        # Clean categoricals
        brand = _clean_brand(rec.get("brand", ""))

        rec["price"] = price
        rec["kilometers"] = kms if kms is not None else 0
        rec["year"] = year
        rec["cc"] = cc if cc is not None else 0
        rec["seating_capacity"] = seats if seats is not None else 0
        rec["brand"] = brand
        rec["gearbox"] = rec.get("gearbox", "").strip().title()
        rec["fuel"] = rec.get("fuel", "").strip().title()
        rec["status"] = rec.get("status", "").strip().title()
        rec["type"] = rec.get("type", "").strip().title()
        rec["color"] = _clean_color(rec.get("color", ""))
        rec["model"] = rec.get("model", "").strip()
        rec["variant"] = rec.get("variant", "").strip()
        rec["series"] = rec.get("series", "").strip()

        # Feature engineering
        rec["decade"] = _decade(year)
        rec["price_bracket"] = _price_bracket(price)
        rec["odometer_category"] = _odometer_category(kms) if kms is not None else "unknown"

        clean_rows.append(rec)
        stats["kept"] += 1

    print(f"       Kept: {stats['kept']}")
    print(f"       Dropped (no price): {stats.get('dropped_no_price', 0)}")
    print(f"       Dropped (no year):  {stats.get('dropped_no_year', 0)}")

    # ---- 3. Save processed CSV ----
    print(f"\n[3/6] Saving processed data")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    csv_out = PROCESSED_DIR / CLEAN_CSV
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PROCESSED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(clean_rows)
    print(f"       CSV:  {csv_out} ({len(clean_rows)} rows)")

    # Try parquet
    try:
        import pandas as pd
        df_clean = pd.DataFrame(clean_rows)
        parquet_out = PROCESSED_DIR / CLEAN_PARQUET
        df_clean[PROCESSED_COLUMNS].to_parquet(parquet_out, index=False)
        print(f"       Parquet: {parquet_out}")
        has_pandas = True
    except ImportError:
        print("       Parquet: skipped (pandas/pyarrow not installed)")
        has_pandas = False
        df_clean = None

    # ---- 4. Feature engineering for ML ----
    print("\n[4/6] Creating ML features with standard scaling")
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)

    # One-hot / binary features
    feature_rows = []
    for rec in clean_rows:
        feat = {}
        feat["id"] = rec["id"]
        feat[TARGET_COLUMN] = rec[TARGET_COLUMN]

        # Numeric pass-through
        feat["year"] = rec["year"]
        feat["kilometers"] = rec["kilometers"]
        feat["cc"] = rec["cc"]
        feat["seating_capacity"] = rec["seating_capacity"]

        # Decade dummies
        for d in DECADES.values():
            feat[d.replace("s", "") + "s"] = 1 if rec["decade"] == d else 0

        # Gearbox dummies
        for g in ["Automatic", "Manual"]:
            feat["gearbox_" + g] = 1 if rec["gearbox"] == g else 0

        # Fuel dummies
        for f in ["Diesel", "Premium Unleaded Petrol", "Unleaded Petrol",
                   "Premium Unleaded/Electric", "Unleaded Petrol/Electric"]:
            feat["fuel_" + f] = 1 if rec["fuel"] == f else 0

        # Status dummies
        for s in ["Demo", "New In Stock", "Used"]:
            feat["status_" + s.replace(" ", "_")] = 1 if rec["status"] == s else 0

        feature_rows.append(feat)

    # Standard scaling (fit on training only; here we do whole dataset)
    numeric_cols = ["year", "kilometers", "cc", "seating_capacity"]
    scaler_params = {}
    X_raw = {col: [] for col in numeric_cols}
    for rec in feature_rows:
        for col in numeric_cols:
            X_raw[col].append(rec[col])

    for col in numeric_cols:
        vals = X_raw[col]
        mu = statistics.mean(vals)
        sigma = statistics.stdev(vals) if statistics.stdev(vals) > 1e-10 else 1.0
        scaler_params[col] = {"mean": mu, "std": sigma}
        for i, rec in enumerate(feature_rows):
            rec[col + "_scaled"] = (rec[col] - mu) / sigma

    # Build final feature vectors
    final_feature_cols = [col + "_scaled" for col in numeric_cols]
    final_feature_cols += [c for c in ML_FEATURE_COLUMNS
                           if c not in numeric_cols]

    ml_rows = []
    for rec in feature_rows:
        row = {"id": rec["id"]}
        for col in final_feature_cols:
            row[col] = rec.get(col, 0.0)
        row[TARGET_COLUMN] = rec[TARGET_COLUMN]
        ml_rows.append(row)

    # Save features CSV
    feat_csv_out = FEATURES_DIR / FEATURES_CSV
    feat_fieldnames = ["id"] + final_feature_cols + [TARGET_COLUMN]
    with open(feat_csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=feat_fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ml_rows)
    print(f"       CSV:  {feat_csv_out} ({len(ml_rows)} rows, {len(final_feature_cols)} features)")

    # Save features Parquet
    if has_pandas:
        df_feat = pd.DataFrame(ml_rows)
        feat_parquet_out = FEATURES_DIR / FEATURES_PARQUET
        df_feat.to_parquet(feat_parquet_out, index=False)
        print(f"       Parquet: {feat_parquet_out}")

    # Save scaler params
    scaler_path = FEATURES_DIR / SCALER_META
    with open(scaler_path, "w") as f:
        json.dump(scaler_params, f, indent=2)
    print(f"       Scaler params: {scaler_path}")

    # Save feature names
    fnames_path = FEATURES_DIR / FEATURE_NAMES
    with open(fnames_path, "w") as f:
        json.dump({"feature_columns": final_feature_cols,
                    "target_column": TARGET_COLUMN,
                    "num_features": len(final_feature_cols),
                    "num_samples": len(ml_rows)}, f, indent=2)
    print(f"       Feature names: {fnames_path}")

    # ---- 5. Summary statistics ----
    print("\n[5/6] Computing summary statistics")

    brands_all = [r["brand"] for r in clean_rows]
    brand_counts = Counter(brands_all)

    decade_counts = Counter(r["decade"] for r in clean_rows)
    bracket_counts = Counter(r["price_bracket"] for r in clean_rows)
    odo_counts = Counter(r["odometer_category"] for r in clean_rows)

    prices = [r["price"] for r in clean_rows]
    kms = [r["kilometers"] for r in clean_rows]

    summary = {
        "dataset": "australian-car-market",
        "total_rows_raw": len(raw_rows),
        "total_rows_clean": len(clean_rows),
        "columns": PROCESSED_COLUMNS,
        "ml_features": {
            "feature_count": len(final_feature_cols),
            "feature_columns": final_feature_cols,
            "target": TARGET_COLUMN,
            "scaler": scaler_params,
        },
        "statistics": {
            "price": {
                "min": min(prices),
                "max": max(prices),
                "mean": round(statistics.mean(prices), 2),
                "median": statistics.median(prices),
                "std": round(statistics.stdev(prices), 2),
            },
            "year": {
                "min": int(min(r["year"] for r in clean_rows)),
                "max": int(max(r["year"] for r in clean_rows)),
            },
            "kilometers": {
                "min": min(kms),
                "max": max(kms),
                "mean": round(statistics.mean(kms), 2),
                "median": statistics.median(kms),
            },
            "top_brands": dict(brand_counts.most_common(10)),
            "unique_brands": len(brand_counts),
            "decade_distribution": dict(decade_counts.most_common()),
            "price_bracket_distribution": dict(bracket_counts.most_common()),
            "odometer_distribution": dict(odo_counts.most_common()),
        },
        "dropped_rows": {
            "no_price": stats.get("dropped_no_price", 0),
            "no_year": stats.get("dropped_no_year", 0),
        },
    }

    summary_path = TARGET_DIR / "processed" / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"       Summary: {summary_path}")

    # ---- 6. Done ----
    print("\n[6/6] Pipeline complete!")
    print(f"       Cleaned:   {stats['kept']} rows -> {csv_out}")
    print(f"       Features:  {len(ml_rows)} rows x {len(final_feature_cols)} cols -> {feat_csv_out}")
    print("=" * 60)

    return summary


if __name__ == "__main__":
    summary = run_pipeline()
