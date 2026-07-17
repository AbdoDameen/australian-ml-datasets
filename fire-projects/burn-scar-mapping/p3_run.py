#!/usr/bin/env python3
"""
Project 3: Satellite Burn Scar Mapping — standalone runner
Generates all graphs as PNG files. Run with: python3 p3_run.py
"""
import numpy as np, matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path
from matplotlib.colors import ListedColormap
import warnings; warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid", palette="muted")

BASE = Path(__file__).parent
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
np.random.seed(42)

# ── Generate synthetic scene ──────────────────────────────────────────
size = 300
ndvi_pre = np.random.normal(0.65, 0.12, (size, size)).clip(0.2, 0.92)
for _ in range(30):
    cx, cy = np.random.randint(0, size, 2)
    r = np.random.randint(8, 35)
    y, x = np.ogrid[:size, :size]
    ndvi_pre[(x-cx)**2 + (y-cy)**2 < r**2] = np.random.uniform(0.75, 0.95)
for _ in range(5):
    cx, cy = np.random.randint(0, size, 2)
    r = np.random.randint(3, 10)
    ndvi_pre[(np.ogrid[:size,:size][0]-cx)**2 + (np.ogrid[:size,:size][1]-cy)**2 < r**2] = np.random.uniform(-0.1, 0.05)

# ── Burn scar ─────────────────────────────────────────────────────────
ndvi_post = ndvi_pre.copy()
cx, cy = size//2, size//2-15
y, x = np.ogrid[:size, :size]
angle = np.random.uniform(0, np.pi)
cos_a, sin_a = np.cos(angle), np.sin(angle)
x_rot = (x-cx)*cos_a + (y-cy)*sin_a
y_rot = -(x-cx)*sin_a + (y-cy)*cos_a
a, b = size*0.2, size*0.12
burn = (x_rot/a)**2 + (y_rot/b)**2 < 1
burn = burn & (np.random.normal(0, 0.4, (size,size)) > -0.2)
ndvi_post[burn] = np.random.uniform(-0.15, 0.3, burn.sum())
cx2, cy2 = size//3, size//3
burn2 = ((x-cx2)/(a*0.3))**2 + ((y-cy2)/(b*0.3))**2 < 1
ndvi_post[burn2] = np.random.uniform(-0.1, 0.2, burn2.sum())

ndvi_diff = ndvi_pre - ndvi_post
burn_mask = (burn | burn2) | (ndvi_diff > 0.15)
severity = np.zeros_like(ndvi_diff, dtype=np.uint8)
severity[(ndvi_diff>0.15)&(ndvi_diff<=0.30)] = 1
severity[(ndvi_diff>0.30)&(ndvi_diff<=0.50)] = 2
severity[ndvi_diff>0.50] = 3
area_ha = burn_mask.sum()*100/10000
print(f"Scene: {size}×{size}  |  Burn: {burn_mask.sum():,} px ({burn_mask.mean()*100:.1f}%)")
print(f"Area: {area_ha:.1f} ha ({area_ha/100:.2f} km²)")

# ── 1. Pre-fire NDVI ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(ndvi_pre, cmap="YlGn", vmin=-0.2, vmax=1.0)
ax.set_title("Pre-Fire NDVI (Healthy Vegetation)", fontweight="bold"); ax.axis("off")
plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout(); fig.savefig(OUT / "p3_01_pre_fire_ndvi.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_01_pre_fire_ndvi.png")

# ── 2. Post-fire NDVI ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(ndvi_post, cmap="YlGn", vmin=-0.2, vmax=1.0)
ax.set_title("Post-Fire NDVI (Burn Scar Visible)", fontweight="bold"); ax.axis("off")
plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout(); fig.savefig(OUT / "p3_02_post_fire_ndvi.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_02_post_fire_ndvi.png")

# ── 3. NDVI difference ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(ndvi_diff, cmap="RdBu_r", vmin=-0.3, vmax=0.7)
ax.set_title("NDVI Difference (Δ = Pre − Post)", fontweight="bold"); ax.axis("off")
plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout(); fig.savefig(OUT / "p3_03_ndvi_diff.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_03_ndvi_diff.png")

# ── 4. Burn mask ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
ax.imshow(burn_mask, cmap=ListedColormap(["#228B22","#DC143C"]))
ax.set_title(f"Burn Scar Mask ({burn_mask.sum():,} px detected)", fontweight="bold"); ax.axis("off")
plt.tight_layout(); fig.savefig(OUT / "p3_04_burn_mask.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_04_burn_mask.png")

# ── 5. Severity classification ───────────────────────────────────────
sev_cmap = ListedColormap(["#2d6a2f","#f0ad4e","#d9534f","#8b0000"])
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(severity, cmap=sev_cmap, vmin=0, vmax=3)
ax.set_title("Burn Severity Classification", fontweight="bold"); ax.axis("off")
cbar = plt.colorbar(im, ax=ax, shrink=0.8, ticks=[0.4,1.15,2.0,2.85])
cbar.set_ticklabels(["Unburned","Low","Moderate","Severe"])
plt.tight_layout(); fig.savefig(OUT / "p3_05_severity.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_05_severity.png")

# ── 6. 3-panel comparison ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Satellite NDVI Analysis: Pre vs Post Fire", fontsize=14, fontweight="bold")
for ax, arr, title, cmap, vmin, vmax in [
    (axes[0], ndvi_pre, "Pre-Fire NDVI", "YlGn", -0.2, 1.0),
    (axes[1], ndvi_post, "Post-Fire NDVI", "YlGn", -0.2, 1.0),
    (axes[2], ndvi_diff, "NDVI Difference", "RdBu_r", -0.3, 0.7)]:
    im = ax.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(title); ax.axis("off"); plt.colorbar(im, ax=ax, shrink=0.8)
plt.tight_layout(); fig.savefig(OUT / "p3_06_three_panel.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_06_three_panel.png")

# ── 7. Severity pie + NDVI histogram ─────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sev_counts = [severity[severity==i].size for i in range(4)]
axes[0].pie(sev_counts, labels=["Unburned","Low","Moderate","Severe"],
            autopct="%1.1f%%", colors=["#2d6a2f","#f0ad4e","#d9534f","#8b0000"],
            explode=(0,0.05,0.05,0.1), startangle=90)
axes[0].set_title("Burn Severity Distribution", fontweight="bold")
sns.histplot(ndvi_pre.flatten(), bins=50, alpha=0.5, label="Pre-Fire", ax=axes[1], color="#2d6a2f")
sns.histplot(ndvi_post.flatten(), bins=50, alpha=0.5, label="Post-Fire", ax=axes[1], color="#d9534f")
axes[1].axvline(ndvi_pre.mean(), color="#2d6a2f", ls="--", lw=2)
axes[1].axvline(ndvi_post.mean(), color="#d9534f", ls="--", lw=2)
axes[1].set_xlabel("NDVI"); axes[1].set_ylabel("Pixel Count")
axes[1].set_title("NDVI Distribution: Pre vs Post Fire", fontweight="bold"); axes[1].legend()
plt.tight_layout(); fig.savefig(OUT / "p3_07_pie_hist.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_07_pie_hist.png")

# ── 8. Cross-section transect ─────────────────────────────────────────
center = size // 2
pre_profile = ndvi_pre[center, :]
post_profile = ndvi_post[center, :]
fig, ax = plt.subplots(figsize=(14, 4))
x_axis = np.arange(len(pre_profile))
ax.fill_between(x_axis, 0, pre_profile, alpha=0.3, color="#2d6a2f", label="Pre-Fire NDVI")
ax.fill_between(x_axis, 0, post_profile, alpha=0.3, color="#d9534f", label="Post-Fire NDVI")
ax.plot(x_axis, pre_profile, color="#2d6a2f", lw=1.5)
ax.plot(x_axis, post_profile, color="#d9534f", lw=1.5)
ax.set_xlabel("Pixel Position Along Transect"); ax.set_ylabel("NDVI")
ax.set_title("NDVI Cross-Section Through Burn Scar Center", fontweight="bold"); ax.legend()
plt.tight_layout(); fig.savefig(OUT / "p3_08_transect.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p3_08_transect.png")

print(f"\n{'='*50}")
print(f"PROJECT 3 COMPLETE — 8 charts saved to {OUT}")
print(f"{'='*50}")
