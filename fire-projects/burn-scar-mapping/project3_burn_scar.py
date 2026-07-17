# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn"]
# ///
# -*- coding: utf-8 -*-

import marimo

__generated_with = "0.23.14"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # 🛰️ Project 3: Satellite Burn Scar Mapping

        Detect bushfire burn scars by comparing pre-fire and post-fire Sentinel-2 satellite imagery using NDVI (Normalized Difference Vegetation Index).

        **Method:** NDVI = (NIR − Red) / (NIR + Red)  |  **ΔNDVI > threshold** = burn scar
        """
    )


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    import warnings
    warnings.filterwarnings('ignore')
    sns.set_theme(style="whitegrid", palette="muted")
    return Path, np, plt, sns, warnings


# ─── GENERATE SYNTHETIC SCENE ──────────────────────────────────────────────

@app.cell
def _(np):
    np.random.seed(42)

    size = 300
    ndvi_pre = np.random.normal(0.65, 0.12, (size, size)).clip(0.2, 0.92)

    # Forest patches
    for _ in range(30):
        cx, cy = np.random.randint(0, size, 2)
        r = np.random.randint(8, 35)
        y, x = np.ogrid[:size, :size]
        mask = (x - cx)**2 + (y - cy)**2 < r**2
        ndvi_pre[mask] = np.random.uniform(0.75, 0.95, mask.sum())

    # Water bodies
    for _ in range(5):
        cx, cy = np.random.randint(0, size, 2)
        r = np.random.randint(3, 10)
        mask = (np.ogrid[:size, :size][0] - cx)**2 + (np.ogrid[:size, :size][1] - cy)**2 < r**2
        ndvi_pre[mask] = np.random.uniform(-0.1, 0.05, mask.sum())

    print(f"Scene size: {size}×{size}")
    print(f"Pre-fire NDVI: mean={ndvi_pre.mean():.3f}, range=[{ndvi_pre.min():.3f}, {ndvi_pre.max():.3f}]")
    return cx, cy, mask, ndvi_pre, r, size, x, y


# ─── BURN SCAR ─────────────────────────────────────────────────────────────

@app.cell
def _(ndvi_pre, np, size):
    ndvi_post = ndvi_pre.copy()

    # Main burn scar — irregular ellipse
    _cx, _cy = size // 2, size // 2 - 15
    _y, _x = np.ogrid[:size, :size]
    angle = np.random.uniform(0, np.pi)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    x_rot = (_x - _cx) * cos_a + (_y - _cy) * sin_a
    y_rot = -(_x - _cx) * sin_a + (_y - _cy) * cos_a
    a, b = size * 0.2, size * 0.12
    burn = (x_rot / a)**2 + (y_rot / b)**2 < 1
    # Add edge noise
    noise = np.random.normal(0, 0.4, (size, size))
    burn = burn & (noise > -0.2)

    # Severity varies within burn scar
    ndvi_post[burn] = np.random.uniform(-0.15, 0.3, burn.sum())

    # Secondary small burn
    _cx2, _cy2 = size // 3, size // 3
    burn2 = ((_x - _cx2) / (a * 0.3))**2 + ((_y - _cy2) / (b * 0.3))**2 < 1
    ndvi_post[burn2] = np.random.uniform(-0.1, 0.2, burn2.sum())

    print(f"Post-fire NDVI: mean={ndvi_post.mean():.3f}")
    print(f"Burn scar pixels: {burn.sum():,} ({burn.mean()*100:.1f}% of scene)")
    print(f"Secondary burn: {burn2.sum():,} pixels")
    return (
        a, angle, b, burn, burn2, cos_a, cx, cx2, cy, cy2, ndvi_post,
        noise, sin_a, x, x_rot, y, y_rot
    )


# ─── COMPUTE NDVI DIFF & SEVERITY ──────────────────────────────────────────

@app.cell
def _(burn, burn2, ndvi_post, ndvi_pre, np):
    ndvi_diff = ndvi_pre - ndvi_post
    burn_mask = (burn | burn2) | (ndvi_diff > 0.15)

    severity = np.zeros_like(ndvi_diff, dtype=np.uint8)
    severity[(ndvi_diff > 0.15) & (ndvi_diff <= 0.30)] = 1
    severity[(ndvi_diff > 0.30) & (ndvi_diff <= 0.50)] = 2
    severity[ndvi_diff > 0.50] = 3

    area_ha = burn_mask.sum() * 100 / 10000  # 10m resolution → hectares
    area_km2 = area_ha / 100

    sev_labels = {0: "Unburned", 1: "Low", 2: "Moderate", 3: "Severe"}
    print(f"Burn area: {area_ha:.1f} ha ({area_km2:.2f} km²)")
    print(f"\nSeverity breakdown:")
    for lv in [1, 2, 3]:
        print(f"  {sev_labels[lv]:10s}: {(severity == lv).sum():>6,} px ({(severity == lv).mean()*100:.1f}%)")
    return area_ha, area_km2, burn_mask, ndvi_diff, sev_labels, severity


# ─── PANEL: PRE-FIRE, POST-FIRE, NDVI DIFF ────────────────────────────────

@app.cell
def _(ndvi_diff, ndvi_post, ndvi_pre, plt):
    _fig, _axes = plt.subplots(1, 3, figsize=(18, 5))
    _fig.suptitle("Satellite NDVI Analysis — Pre vs Post Fire", fontsize=14, fontweight="bold")

    im1 = axes[0].imshow(ndvi_pre, cmap="YlGn", vmin=-0.2, vmax=1.0)
    axes[0].set_title("Pre-Fire NDVI\n(Healthy Vegetation)")
    axes[0].axis("off")
    plt.colorbar(im1, ax=axes[0], shrink=0.8)

    im2 = axes[1].imshow(ndvi_post, cmap="YlGn", vmin=-0.2, vmax=1.0)
    axes[1].set_title("Post-Fire NDVI\n(Burn Scar Visible)")
    axes[1].axis("off")
    plt.colorbar(im2, ax=axes[1], shrink=0.8)

    im3 = axes[2].imshow(ndvi_diff, cmap="RdBu_r", vmin=-0.3, vmax=0.7)
    axes[2].set_title("NDVI Difference\n(ΔNDVI = Pre − Post)")
    axes[2].axis("off")
    plt.colorbar(im3, ax=axes[2], shrink=0.8)

    plt.tight_layout()
    fig


# ─── PANEL: BURN MASK + SEVERITY ──────────────────────────────────────────

@app.cell
def _(burn_mask, plt, severity):
    from matplotlib.colors import ListedColormap
    sev_cmap = ListedColormap(["#2d6a2f", "#f0ad4e", "#d9534f", "#8b0000"])

    _fig, _axes = plt.subplots(1, 2, figsize=(12, 5))
    _fig.suptitle("Burn Scar Detection Results", fontsize=14, fontweight="bold")

    axes[0].imshow(burn_mask, cmap=ListedColormap(["#228B22", "#DC143C"]))
    axes[0].set_title(f"Burn Scar Mask\n({burn_mask.sum():,} px detected)")
    axes[0].axis("off")

    im = axes[1].imshow(severity, cmap=sev_cmap, vmin=0, vmax=3)
    axes[1].set_title("Burn Severity Classification\n(Green=Unburned → Red=Severe)")
    axes[1].axis("off")
    cbar = plt.colorbar(im, ax=axes[1], shrink=0.8, ticks=[0.4, 1.15, 2.0, 2.85])
    cbar.set_ticklabels(["Unburned", "Low", "Moderate", "Severe"])

    plt.tight_layout()
    fig


# ─── SEVERITY PIE + NDVI PROFILE ──────────────────────────────────────────

@app.cell
def _(burn_mask, ndvi_diff, ndvi_post, ndvi_pre, plt, severity, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # Severity pie
    sev_counts = [severity[severity == i].size for i in range(4)]
    labels = ["Unburned", "Low", "Moderate", "Severe"]
    colors_pie = ["#2d6a2f", "#f0ad4e", "#d9534f", "#8b0000"]
    explode = (0, 0.05, 0.05, 0.1)
    axes[0].pie(sev_counts, labels=labels, autopct="%1.1f%%", colors=colors_pie,
                explode=explode, startangle=90)
    axes[0].set_title("Burn Severity Distribution", fontweight="bold")

    # NDVI histogram comparison
    sns.histplot(ndvi_pre.flatten(), bins=50, alpha=0.5, label="Pre-Fire", ax=axes[1], color="#2d6a2f")
    sns.histplot(ndvi_post.flatten(), bins=50, alpha=0.5, label="Post-Fire", ax=axes[1], color="#d9534f")
    axes[1].axvline(ndvi_pre.mean(), color="#2d6a2f", ls="--", lw=2)
    axes[1].axvline(ndvi_post.mean(), color="#d9534f", ls="--", lw=2)
    axes[1].set_xlabel("NDVI")
    axes[1].set_ylabel("Pixel Count")
    axes[1].set_title("NDVI Distribution: Pre vs Post Fire", fontweight="bold")
    axes[1].legend()

    plt.tight_layout()
    fig


# ─── FIRE RADAR PROFILE ───────────────────────────────────────────────────

@app.cell
def _(burn_mask, ndvi_diff, ndvi_pre, np, plt):
    # NDVI profile across the burn scar (center transect)
    center = ndvi_pre.shape[0] // 2
    pre_profile = ndvi_pre[center, :]
    post_profile = ndvi_post[center, :]
    diff_profile = ndvi_diff[center, :]

    fig, ax = plt.subplots(figsize=(14, 4))
    x_axis = np.arange(len(pre_profile))
    ax.fill_between(x_axis, 0, pre_profile, alpha=0.3, color="#2d6a2f", label="Pre-Fire NDVI")
    ax.fill_between(x_axis, 0, post_profile, alpha=0.3, color="#d9534f", label="Post-Fire NDVI")
    ax.plot(x_axis, pre_profile, color="#2d6a2f", lw=1.5)
    ax.plot(x_axis, post_profile, color="#d9534f", lw=1.5)
    ax.set_xlabel("Pixel Position Along Transect")
    ax.set_ylabel("NDVI")
    ax.set_title("NDVI Cross-Section Through Burn Scar Center", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    fig
    return center, diff_profile, post_profile, pre_profile, x_axis,


# ─── SENTINEL-2 ACCESS GUIDE ──────────────────────────────────────────────

@app.cell(hide_code=True)
def _():
    print("=" * 60)
    print("TO USE WITH REAL SENTINEL-2 DATA:")
    print("=" * 60)
    print()
    print("1. Register at https://dataspace.copernicus.eu/")
    print("2. pip install sentinelhub oauthlib")
    print("3. Run the download script:")
    print()
    print("   python3 scripts/download_sentinel2.py \\")
    print("     --lat -33.86 --lon 151.21 \\")
    print("     --pre-date 2019-10-01 --post-date 2020-02-01")
    print()
    print("See scripts/download_sentinel2.py for the full implementation.")


if __name__ == "__main__":
    app.run()
