#!/usr/bin/env python3
"""
Project 4: Bushfire Analytics Dashboard — standalone runner
Generates all graphs as PNG files. Run with: python3 p4_run.py
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path
import json, warnings
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid", palette="muted")

BASE = Path(__file__).parent
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load all project data ─────────────────────────────────────────────
base = Path("..")
loaded = []

# P1
p1_csv = base / "risk-prediction" / "processed" / "forest_fire_risk_clean.csv"
if p1_csv.exists():
    df1 = pd.read_csv(p1_csv)
    state_cols = [c for c in df1.columns if c.startswith('state_')]
    tenure_cols = [c for c in df1.columns if c.startswith('tenure_')]
    loaded.append(f"P1: {len(df1):,} rows")
else:
    df1 = None
    state_cols = tenure_cols = []
    loaded.append("P1: not found (run p1_run.py first)")

# P2
p2_json = base / "resource-allocation" / "outputs" / "resource_allocation_plan.json"
if p2_json.exists():
    with open(p2_json) as f: plan = json.load(f)
    df2 = pd.DataFrame(plan['allocation'])
    loaded.append(f"P2: {len(df2)} states, ${plan['total_budget_aud']:,}")
else:
    df2 = None; plan = None
    loaded.append("P2: not found")

# P3
p3_mask = base / "burn-scar-mapping" / "outputs" / "burn_mask.npy"
p3_diff = base / "burn-scar-mapping" / "outputs" / "ndvi_diff.npy"
if p3_mask.exists() and p3_diff.exists():
    burn_mask = np.load(p3_mask)
    ndvi_diff = np.load(p3_diff)
    loaded.append(f"P3: burn_mask {burn_mask.shape}, {burn_mask.mean()*100:.1f}% burned")
else:
    burn_mask = ndvi_diff = None
    loaded.append("P3: not found")

print("Loaded:", " | ".join(loaded))

# ── 1. Dashboard overview ────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12))
fig.suptitle("Bushfire Analytics Dashboard", fontsize=16, fontweight="bold")

# 1a. Fire rate by state
ax1 = fig.add_subplot(3, 3, 1)
if df1 is not None and state_cols:
    rates = []
    for sc in state_cols:
        name = sc.replace('state_','')
        sub = df1[df1[sc]==1]
        if len(sub):
            rates.append({'state':name,'fire_rate':sub['unplanned_5'].mean()})
    rdf = pd.DataFrame(rates).sort_values('fire_rate')
    colors = ["#d9534f" if v>0.15 else "#f0ad4e" if v>0.05 else "#5cb85c" for v in rdf['fire_rate']]
    ax1.barh(rdf['state'], rdf['fire_rate'], color=colors)
    ax1.set_title("Fire Rate by State"); ax1.set_xlabel("Rate")

# 1b. Budget allocation
ax2 = fig.add_subplot(3, 3, 2)
if df2 is not None:
    ds = df2.sort_values('budget_estimate_aud')
    ax2.barh(ds['state'], ds['budget_estimate_aud']/1e9, color=sns.color_palette("Blues_r", len(ds)))
    ax2.set_title("Budget ($B)"); ax2.set_xlabel("$ Billions")

# 1c. Resource breakdown
ax3 = fig.add_subplot(3, 3, 3)
if df2 is not None:
    # Unpack resources from dict column
    resources_df = df2['resources'].apply(pd.Series)
    df2 = pd.concat([df2.drop('resources', axis=1), resources_df], axis=1)
    res = df2.melt(id_vars='state', value_vars=['appliance_heavy','appliance_light','crew_member'],
                   var_name='resource', value_name='count')
    sns.barplot(data=res, x='resource', y='count', hue='state', ax=ax3, palette="Set2")
    ax3.set_title("Resources"); ax3.tick_params(axis='x', rotation=30)

# 1d. Tenure risk
ax4 = fig.add_subplot(3, 3, 4)
if df1 is not None and tenure_cols:
    tr = []
    for tc in tenure_cols:
        name = tc.replace('tenure_','')
        sub = df1[df1[tc]==1]
        if len(sub):
            tr.append({'tenure':name,'fire_rate':sub['unplanned_5'].mean()})
    tdf = pd.DataFrame(tr).sort_values('fire_rate')
    colors = ["#d9534f" if v>0.15 else "#f0ad4e" if v>0.05 else "#5cb85c" for v in tdf['fire_rate']]
    ax4.barh(tdf['tenure'], tdf['fire_rate'], color=colors)
    ax4.set_title("Risk by Tenure"); ax4.set_xlabel("Rate")

# 1e. Sensitivity
ax5 = fig.add_subplot(3, 3, 5)
if plan:
    scenarios = ['Base','+10%','+20%','+30%','+50%']
    budgets = [plan['total_budget_aud']*m/1e9 for m in [1.0,1.1,1.2,1.3,1.5]]
    ax5.plot(scenarios, budgets, 'o-', color="#d9534f", lw=2, ms=8)
    ax5.fill_between(range(5), budgets, alpha=0.15, color="#d9534f")
    ax5.set_title("Budget Sensitivity"); ax5.set_ylabel("$B")

# 1f. Prior burns distribution
ax6 = fig.add_subplot(3, 3, 6)
if df1 is not None and 'prior_burns' in df1.columns:
    b = df1[df1['prior_burns']>=0]['prior_burns']
    sns.histplot(b, bins=6, discrete=True, ax=ax6, color="#f0ad4e")
    ax6.set_title("Burn Frequency"); ax6.set_xlabel("Number of Burns")

# 1g. Key metrics
ax7 = fig.add_subplot(3, 3, (7, 9))
ax7.axis("off")
stats = []
if df1 is not None:
    stats.append(f"Forest regions: {len(df1):,}")
    stats.append(f"Unplanned fire rate: {df1['unplanned_5'].mean()*100:.1f}%")
if plan:
    stats.append(f"Total budget: ${plan['total_budget_aud']:,}")
    stats.append(f"Predicted fires: {plan['total_predicted_fires']:,}")
if burn_mask is not None:
    stats.append(f"Burn scar: {burn_mask.mean()*100:.1f}% of scene")
ax7.text(0.02, 0.5, "\n".join(stats), fontsize=14, va="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#dee2e6"))
ax7.set_title("Key Metrics", fontweight="bold")

plt.tight_layout(); fig.savefig(OUT / "p4_01_dashboard.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p4_01_dashboard.png")

# ── 2. Budget vs Fire Rate bubble chart ──────────────────────────────
if df1 is not None and df2 is not None and state_cols:
    rates = {}
    for sc in state_cols:
        name = sc.replace('state_','')
        sub = df1[df1[sc]==1]
        if len(sub): rates[name] = sub['unplanned_5'].mean()
    comp = df2.copy()
    comp['fire_rate'] = comp['state'].map(rates)
    comp = comp.dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(comp['fire_rate'], comp['budget_estimate_aud']/1e9, s=comp['predicted_fires']*2,
              c=range(len(comp)), cmap="YlOrRd", alpha=0.7, edgecolors="black", linewidth=0.5)
    for _, r in comp.iterrows():
        ax.annotate(r['state'], (r['fire_rate'], r['budget_estimate_aud']/1e9), fontsize=10, ha='center', va='bottom')
    ax.set_xlabel("Fire Rate (2020-21)"); ax.set_ylabel("Budget ($B)")
    ax.set_title("Budget vs Fire Rate (bubble = predicted fires)", fontweight="bold")
    plt.tight_layout(); fig.savefig(OUT / "p4_02_bubble.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ p4_02_bubble.png")

# ── 3. Burn scar stats ───────────────────────────────────────────────
if burn_mask is not None and ndvi_diff is not None:
    from scipy import ndimage as ndi
    labeled, nf = ndi.label(burn_mask)
    sizes = pd.Series([(labeled==i).sum() for i in range(1, nf+1)])
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(sizes, bins=30, ax=axes[0], color="#d9534f")
    axes[0].set_title(f"Burn Patch Size ({nf} patches)", fontweight="bold")
    axes[0].set_xlabel("Patch Size (pixels)")
    db = ndvi_diff[burn_mask]; du = ndvi_diff[~burn_mask]
    sns.histplot(du, bins=50, alpha=0.5, label="Unburned", ax=axes[1], color="#2d6a2f")
    sns.histplot(db, bins=50, alpha=0.5, label="Burned", ax=axes[1], color="#d9534f")
    axes[1].set_title("NDVI Change: Burned vs Unburned", fontweight="bold")
    axes[1].set_xlabel("NDVI Difference"); axes[1].legend()
    plt.tight_layout(); fig.savefig(OUT / "p4_03_burn_stats.png", dpi=150, bbox_inches="tight")
    plt.close(); print("  ✓ p4_03_burn_stats.png")

# ── 4. Combined data table ───────────────────────────────────────────
if df1 is not None and df2 is not None and state_cols:
    summary = []
    for sc in state_cols:
        name = sc.replace('state_','')
        sub = df1[df1[sc]==1]
        if len(sub):
            ar = df2[df2['state']==name]
            budget = ar['budget_estimate_aud'].values[0] if len(ar) > 0 else 0
            summary.append({'State':name,'Regions':len(sub),
                           'Fire Rate':f"{sub['unplanned_5'].mean()*100:.1f}%",
                           'Avg Prior Burns':f"{sub['prior_burns'].mean():.2f}",
                           'Budget':f"${budget/1e6:.0f}M" if budget else "N/A"})
    summary_df = pd.DataFrame(summary)
    print(f"\nCombined Data Table:\n{summary_df.to_string(index=False)}")

print(f"\n{'='*50}")
print(f"PROJECT 4 COMPLETE — charts saved to {OUT}")
print(f"{'='*50}")
