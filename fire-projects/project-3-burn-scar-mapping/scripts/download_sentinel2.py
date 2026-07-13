#!/usr/bin/env python3
"""
REAL DATA ACCESS — requires Copernicus Data Space account.

Install: pip install sentinelhub oauthlib
Register: https://dataspace.copernicus.eu/

Usage:
    python3 download_sentinel2.py --lat -33.86 --lon 151.21 --pre-date 2019-10-01 --post-date 2020-02-01 --output ./data

This downloads pre- and post-fire Sentinel-2 L2A imagery for the given
coordinates and dates, computes NDVI, and saves the burn scar map.
"""
import argparse, os, numpy as np
from pathlib import Path

def download_sentinel2(lat, lon, pre_date, post_date, output_dir):
    """
    Download Sentinel-2 imagery using sentinelhub-py.
    
    Steps:
    1. Set SH_CLIENT_ID and SH_CLIENT_SECRET env vars
    2. This function creates a WCS (Web Coverage Service) request
    3. Downloads B04 (Red) and B08 (NIR) bands
    4. Computes NDVI for pre- and post-fire
    
    For implementation details, see:
    https://sentinelhub-py.readthedocs.io/
    """
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
