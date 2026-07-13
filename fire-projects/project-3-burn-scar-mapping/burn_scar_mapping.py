#!/usr/bin/env python3
"""
Project 3: Satellite Burn Scar Mapping — Sentinel-2 NDVI Analysis

Detects and maps bushfire burn scars by comparing pre-fire and post-fire
satellite imagery using the Normalized Difference Vegetation Index (NDVI).

This script provides:
1. A function to download Sentinel-2 imagery via the Copernicus Data Space
   (requires free registration)
2. NDVI computation and change detection
3. Burn scar classification and area estimation
4. A self-contained demo with synthetic data for users without API access

For full API access: register at https://dataspace.copernicus.eu/
"""
import numpy as np
import json
import warnings
from pathlib import Path
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
SCRIPTS_DIR = BASE / "scripts"
OUTPUTS_DIR = BASE / "outputs"

RANDOM_STATE = 42


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: NDVI-based Burn Scar Detection
# ═══════════════════════════════════════════════════════════════════════════

def compute_ndvi(nir_band, red_band):
    """
    Compute Normalized Difference Vegetation Index.
    
    NDVI = (NIR - Red) / (NIR + Red)
    
    Range: -1 to 1
    - Dense vegetation: 0.6 to 0.9
    - Sparse vegetation: 0.2 to 0.5
    - Bare soil / urban: 0.0 to 0.2
    - Burn scar / water: -0.2 to 0.1
    """
    nir = np.array(nir_band, dtype=np.float64)
    red = np.array(red_band, dtype=np.float64)
    
    denominator = nir + red
    denominator[denominator == 0] = 0.01  # avoid division by zero
    
    ndvi = (nir - red) / denominator
    return np.clip(ndvi, -1, 1)


def detect_burn_scars(ndvi_pre, ndvi_post, threshold=-0.15):
    """
    Detect burn scars by comparing pre-fire and post-fire NDVI.
    
    A significant decrease in NDVI indicates vegetation loss from fire.
    
    Args:
        ndvi_pre: NDVI before the fire (2D numpy array)
        ndvi_post: NDVI after the fire (2D numpy array)
        threshold: NDVI change threshold for burn classification
        
    Returns:
        burn_mask: binary array (1 = burned, 0 = unburned)
        ndvi_diff: NDVI difference map
        burn_area_pct: percentage of area classified as burned
    """
    ndvi_diff = ndvi_pre - ndvi_post
    burn_mask = ndvi_diff > abs(threshold)
    
    total_pixels = burn_mask.size
    burn_pixels = burn_mask.sum()
    burn_area_pct = (burn_pixels / total_pixels) * 100
    
    return burn_mask, ndvi_diff, burn_area_pct


def classify_burn_severity(ndvi_diff):
    """
    Classify burn severity based on NDVI change magnitude.
    
    Severity levels:
        - Low: NDVI change 0.15-0.30
        - Moderate: NDVI change 0.30-0.50
        - Severe: NDVI change > 0.50
    """
    severity = np.zeros_like(ndvi_diff, dtype=np.uint8)
    severity[(ndvi_diff > 0.15) & (ndvi_diff <= 0.30)] = 1  # Low
    severity[(ndvi_diff > 0.30) & (ndvi_diff <= 0.50)] = 2  # Moderate
    severity[ndvi_diff > 0.50] = 3  # Severe
    
    return severity


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: Demo with Synthetic Sentinel-2 Data
# ═══════════════════════════════════════════════════════════════════════════

def generate_demo_scene(size=(200, 200), fire_patch=True):
    """
    Generate a synthetic pre-fire and post-fire scene for demo purposes.
    
    Creates:
    - A vegetated landscape (high NDVI pre-fire)
    - A burn scar patch (low NDVI post-fire)
    """
    np.random.seed(RANDOM_STATE)
    
    # Pre-fire NDVI: healthy vegetation with some variation
    ndvi_pre = np.random.normal(0.6, 0.15, size)
    ndvi_pre = np.clip(ndvi_pre, 0.2, 0.9)
    
    # Add some forest structure (clusters of higher NDVI)
    for _ in range(20):
        cx, cy = np.random.randint(0, size[0]), np.random.randint(0, size[1])
        r = np.random.randint(10, 30)
        y, x = np.ogrid[:size[0], :size[1]]
        mask = (x - cx)**2 + (y - cy)**2 < r**2
        ndvi_pre[mask] = np.random.uniform(0.7, 0.9)
    
    # Post-fire: same scene with a burn scar
    ndvi_post = ndvi_pre.copy()
    
    if fire_patch:
        # Create an irregular burn scar
        cx, cy = size[0] // 2, size[1] // 2
        y, x = np.ogrid[:size[0], :size[1]]
        # Irregular shape: ellipse + random perturbation
        angle = np.random.uniform(0, np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = (x - cx) * cos_a + (y - cy) * sin_a
        y_rot = -(x - cx) * sin_a + (y - cy) * cos_a
        a, b = size[0] * 0.25, size[1] * 0.15  # semi-axes
        burn_mask = (x_rot / a)**2 + (y_rot / b)**2 < 1
        # Randomize edges
        noise = np.random.normal(0, 0.5, size)
        burn_mask = burn_mask & (noise > -0.3)
        
        # Severity varies within burn scar
        ndvi_post[burn_mask] = np.random.uniform(-0.1, 0.25, burn_mask.sum())
    
    return ndvi_pre, ndvi_post


def estimate_burn_area(burn_mask, pixel_resolution_m=10):
    """Estimate burn area in hectares."""
    pixel_area_ha = (pixel_resolution_m ** 2) / 10000  # 1 ha = 10,000 m²
    burn_pixels = burn_mask.sum()
    area_ha = burn_pixels * pixel_area_ha
    return area_ha


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: Sentinelsat Data Access Guide
# ═══════════════════════════════════════════════════════════════════════════

SENTINEL_SCRIPT = """#!/usr/bin/env python3
\"\"\"
REAL DATA ACCESS — requires Copernicus Data Space account.

Install: pip install sentinelhub oauthlib
Register: https://dataspace.copernicus.eu/

Usage:
    python3 download_sentinel2.py --lat -33.86 --lon 151.21 --pre-date 2019-10-01 --post-date 2020-02-01 --output ./data

This downloads pre- and post-fire Sentinel-2 L2A imagery for the given
coordinates and dates, computes NDVI, and saves the burn scar map.
\"\"\"
import argparse, os, numpy as np
from pathlib import Path

def download_sentinel2(lat, lon, pre_date, post_date, output_dir):
    \"\"\"
    Download Sentinel-2 imagery using sentinelhub-py.
    
    Steps:
    1. Set SH_CLIENT_ID and SH_CLIENT_SECRET env vars
    2. This function creates a WCS (Web Coverage Service) request
    3. Downloads B04 (Red) and B08 (NIR) bands
    4. Computes NDVI for pre- and post-fire
    
    For implementation details, see:
    https://sentinelhub-py.readthedocs.io/
    \"\"\"
    from sentinelhub import WcsRequest, MimeType, CRS, BBox, DataSource
    
    bbox = BBox([lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05], crs=CRS.WGS84)
    
    for label, date in [('pre', pre_date), ('post', post_date)]:
        for band, band_name in [('B04', 'red'), ('B08', 'nir')]:
            request = WcsRequest(
                data_source=DataSource.SENTINEL2_L2A,
                layer=f'BANDS-{band}',
                bbox=bbox,
                time=(date, date),
                image_format=MimeType.TIFF,
                size_x=512, size_y=512,
                maxcc=20.0  # max cloud cover percentage
            )
            request.save_data(data_folder=output_dir, 
                            redownload=True,
                            filename=f's2_{label}_{band_name}.tiff')
    
    # Load bands and compute NDVI
    import rasterio
    nir_pre = rasterio.open(f'{output_dir}/s2_pre_nir.tiff').read(1).astype(float)
    red_pre = rasterio.open(f'{output_dir}/s2_pre_red.tiff').read(1).astype(float)
    nir_post = rasterio.open(f'{output_dir}/s2_post_nir.tiff').read(1).astype(float)
    red_post = rasterio.open(f'{output_dir}/s2_post_red.tiff').read(1).astype(float)
    
    # Scale from DN to reflectance
    for arr in [nir_pre, red_pre, nir_post, red_post]:
        arr /= 10000.0
    
    # NDVI
    ndvi_pre = (nir_pre - red_pre) / (nir_pre + red_pre + 1e-10)
    ndvi_post = (nir_post - red_post) / (nir_post + red_post + 1e-10)
    
    np.save(f'{output_dir}/ndvi_pre.npy', ndvi_pre)
    np.save(f'{output_dir}/ndvi_post.npy', ndvi_post)
    print(f'Saved NDVI arrays to {output_dir}/')
    print(f'Pre-fire NDVI mean: {ndvi_pre.mean():.3f}')
    print(f'Post-fire NDVI mean: {ndvi_post.mean():.3f}')
    print(f'NDVI change: {ndvi_pre.mean() - ndvi_post.mean():.3f}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Sentinel-2 for burn scar mapping')
    parser.add_argument('--lat', type=float, required=True, help='Latitude')
    parser.add_argument('--lon', type=float, required=True, help='Longitude')
    parser.add_argument('--pre-date', required=True, help='Pre-fire date (YYYY-MM-DD)')
    parser.add_argument('--post-date', required=True, help='Post-fire date (YYYY-MM-DD)')
    parser.add_argument('--output', default='./data', help='Output directory')
    args = parser.parse_args()
    download_sentinel2(args.lat, args.lon, args.pre_date, args.post_date, args.output)
"""


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("PROJECT 3: Satellite Burn Scar Mapping — Sentinel-2 NDVI")
    print("=" * 60)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate demo scene
    print(f"\n--- Generating Synthetic Demo Scene ---")
    ndvi_pre, ndvi_post = generate_demo_scene(size=(200, 200), fire_patch=True)
    
    print(f"Demo scene: {ndvi_pre.shape[0]}×{ndvi_pre.shape[1]} pixels")
    print(f"Pre-fire NDVI: mean={ndvi_pre.mean():.3f}, std={ndvi_pre.std():.3f}")
    print(f"Post-fire NDVI: mean={ndvi_post.mean():.3f}, std={ndvi_post.std():.3f}")
    
    # Detect burn scars
    print(f"\n--- Burn Scar Detection ---")
    burn_mask, ndvi_diff, burn_area_pct = detect_burn_scars(ndvi_pre, ndvi_post)
    
    area_ha = estimate_burn_area(burn_mask, pixel_resolution_m=10)
    area_sqkm = area_ha / 100
    
    print(f"Burn scar area: {area_ha:.1f} hectares ({area_sqkm:.2f} km²)")
    print(f"Burn scar pixels: {burn_mask.sum():,} / {burn_mask.size:,} ({burn_area_pct:.1f}%)")
    
    # Severity classification
    print(f"\n--- Burn Severity Classification ---")
    severity = classify_burn_severity(ndvi_diff)
    
    for label, level in [("Low", 1), ("Moderate", 2), ("Severe", 3)]:
        pct = (severity == level).sum() / severity.size * 100
        print(f"  {label:10s}: {pct:.1f}% of total area")
    
    # Save outputs
    np.save(OUTPUTS_DIR / "ndvi_pre.npy", ndvi_pre)
    np.save(OUTPUTS_DIR / "ndvi_post.npy", ndvi_post)
    np.save(OUTPUTS_DIR / "ndvi_diff.npy", ndvi_diff)
    np.save(OUTPUTS_DIR / "burn_mask.npy", burn_mask)
    np.save(OUTPUTS_DIR / "burn_severity.npy", severity)
    print(f"\nSaved outputs to {OUTPUTS_DIR}/")
    
    # Write the data access script
    script_path = SCRIPTS_DIR / "download_sentinel2.py"
    with open(script_path, "w") as f:
        f.write(SENTINEL_SCRIPT)
    print(f"Wrote Sentinel-2 download script to {script_path}")
    
    # Generate metadata
    metadata = {
        "project": "Satellite Burn Scar Mapping",
        "source": "Sentinel-2 (Copernicus) / synthetic demo",
        "created_date": str(datetime.now()),
        "demo_scene_size": f"{ndvi_pre.shape[0]}×{ndvi_pre.shape[1]}",
        "burn_area_hectares": round(area_ha, 1),
        "burn_area_percent": round(burn_area_pct, 1),
        "severity_breakdown": {
            "low_pct": round((severity == 1).sum() / severity.size * 100, 1),
            "moderate_pct": round((severity == 2).sum() / severity.size * 100, 1),
            "severe_pct": round((severity == 3).sum() / severity.size * 100, 1)
        },
        "methods": [
            "NDVI = (NIR - Red) / (NIR + Red)",
            "Pre-fire NDVI - Post-fire NDVI > threshold = burn scar",
            "Sentinel-2 L2A (10m resolution, B04 Red + B08 NIR bands)",
            "For real data: register at Copernicus Data Space, use sentinelhub-py"
        ]
    }
    
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*60}")
    print("PROJECT 3 COMPLETE")
    print(f"{'='*60}")
    print("\nTo run with real Sentinel-2 data:")
    print("  1. Register at https://dataspace.copernicus.eu/")
    print("  2. pip install sentinelhub oauthlib")
    print(f"  3. python3 scripts/download_sentinel2.py --lat -33.86 --lon 151.21 \\")
    print(f"     --pre-date 2019-10-01 --post-date 2020-02-01 --output ./data")


if __name__ == "__main__":
    main()
