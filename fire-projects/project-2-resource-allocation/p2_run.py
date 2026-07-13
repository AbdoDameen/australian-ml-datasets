#!/usr/bin/env python3
"""
Project 2: Fire Resource Allocation Optimisation — standalone runner
Generates all graphs as PNG files. Run with: python3 p2_run.py
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import warnings; warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid", palette="muted")

BASE = Path(__file__).parent
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load ──────────────────────────────────────────────────────────────
# Try Project 1 output first, fall back to raw ABARES
csv = Path("../project-1-risk-prediction/processed/forest_fire_risk_clean.csv")
unc = 0
if csv.exists():
    df = pd.read_csv(csv); print(f"Loaded Project 1 output: {len(df):,} rows")
    # If it has one-hot cols, we can use directly
    state_cols = [c for c in df.columns if c.startswith('state_')]
    tenure_cols = [c for c in df.columns if c.startswith('tenure_')]
    if state_cols:
        agg_data = []
        for sc in state_cols:
            sname = sc.replace('state_','')
            for tc in tenure_cols:
                tname = tc.replace('tenure_','')
                sub = df[(df[sc]==1) & (df[tc]==1)]
                if len(sub):
                    agg_data.append({'state':sname,'tenure':tname,'region_count':len(sub),
                                     'fires':sub['unplanned_5'].sum(),'fire_rate':sub['unplanned_5'].mean()})
        agg = pd.DataFrame(agg_data)
        unc = 0
    else:
        unc = 1
else:
    unc = 1

if unc:
    print("Loading raw ABARES data...")
    csv2 = Path("../../daily-datasets/climate/bushfire-history/raw/Fire_For16-21_Attributes.csv")
    df = pd.read_csv(csv2)
    forest = df[df['FOREST']==1].copy()
    forest = forest[forest['STATE'].notna() & (forest['STATE'].str.strip()!='')]
    forest = forest[forest['FOR_BURNS']>=0]
    agg = forest.groupby(['STATE','FOR_TEN']).agg(
        region_count=('FOR_BURNS','count'), fires=('FOR_BURNS','count'),
        fire_rate=('FOR_BURNS', lambda x: (x>0).mean())
    ).reset_index()
    agg.columns = ['state','tenure','region_count','fires','fire_rate']

print(f"Aggregated {len(agg)} state-tenure groups, {agg['fires'].sum():,} total fires")

# ── 1. Fires by state ─────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Fire Resource Allocation — Overview", fontsize=14, fontweight="bold")
state_fires = agg.groupby('state')['fires'].sum().sort_values()
axes[0].bar(state_fires.index, state_fires.values, color=sns.color_palette("Reds_r", len(state_fires)))
axes[0].set_title("Total Fires by State"); axes[0].tick_params(axis='x', rotation=45)
state_rate = agg.groupby('state')['fire_rate'].mean().sort_values()
axes[1].bar(state_rate.index, state_rate.values, color=sns.color_palette("Oranges_r", len(state_rate)))
axes[1].set_title("Mean Fire Rate by State"); axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout(); fig.savefig(OUT / "p2_01_fires_by_state.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p2_01_fires_by_state.png")

# ── 2. Resource demand model + allocation ─────────────────────────────
resource_costs = {'appliance_heavy':2_500_000,'appliance_light':800_000,'crew_member':120_000,'helicopter':5_000_000}
resources_per_fire = {'appliance_heavy':0.3,'appliance_light':0.8,'crew_member':4.0,'helicopter':0.05}
feat = pd.get_dummies(agg[['state','tenure']], drop_first=False).astype(int)
feat['pixel_count'] = agg['region_count']
X = np.nan_to_num(feat.values, nan=0.0); y = agg['fires'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingRegressor(n_estimators=150, max_depth=4, min_samples_leaf=20, random_state=42)
model.fit(X_train, y_train)
agg['predicted_fires'] = model.predict(feat.values).clip(0)
allocation = []
for s in agg['state'].unique():
    sd = agg[agg['state']==s]
    total = max(0, int(sd['predicted_fires'].sum()))
    resources = {r: max(1, int(np.ceil(total*rate))) for r,rate in resources_per_fire.items()}
    budget = sum(resources[r]*resource_costs[r] for r in resources)
    allocation.append({'state':s,'fires':total,**resources,'budget':budget})
alloc = pd.DataFrame(allocation).sort_values('fires', ascending=False)
print(f"  Total fires: {alloc['fires'].sum():,}  |  Budget: ${alloc['budget'].sum():,}")

# ── 3. Budget by state ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Budget & Resource Allocation", fontsize=14, fontweight="bold")
axes[0].bar(alloc['state'], alloc['fires'], color=sns.color_palette("Reds", len(alloc)))
axes[0].set_title("Predicted Fires by State"); axes[0].tick_params(axis='x', rotation=45)
_budget_b = alloc['budget'] / 1e9
axes[1].bar(alloc['state'], _budget_b, color=sns.color_palette("Blues", len(alloc)))
axes[1].set_title("Budget by State ($B)"); axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout(); fig.savefig(OUT / "p2_02_budget_by_state.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p2_02_budget_by_state.png")

# ── 4. Resource breakdown ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
melt = alloc.melt(id_vars=['state','fires','budget'],
                  value_vars=['appliance_heavy','appliance_light','crew_member','helicopter'],
                  var_name='resource', value_name='count')
sns.barplot(data=melt, x='state', y='count', hue='resource', ax=ax, palette="Set2")
ax.set_title("Resource Requirements by State", fontweight="bold"); ax.legend(title="Resource")
plt.tight_layout(); fig.savefig(OUT / "p2_03_resource_breakdown.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p2_03_resource_breakdown.png")

# ── 5. Sensitivity analysis ───────────────────────────────────────────
scenarios = ['Baseline','+10%','+20%','+30%','+50%']
multipliers = [1.0, 1.1, 1.2, 1.3, 1.5]
base_budget = alloc['budget'].sum(); base_fires = alloc['fires'].sum()
budgets = [int(base_budget*m) for m in multipliers]
fires = [int(base_fires*m) for m in multipliers]
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Sensitivity Analysis", fontsize=14, fontweight="bold")
axes[0].plot(scenarios, [b/1e9 for b in budgets], 'o-', color="#d9534f", lw=2, ms=8)
axes[0].fill_between(range(len(scenarios)), [b/1e9 for b in budgets], alpha=0.15, color="#d9534f")
axes[0].set_title("Budget Sensitivity"); axes[0].set_ylabel("$ Billions")
axes[1].plot(scenarios, fires, 's-', color="#f0ad4e", lw=2, ms=8)
axes[1].fill_between(range(len(scenarios)), fires, alpha=0.15, color="#f0ad4e")
axes[1].set_title("Fire Volume Sensitivity"); axes[1].set_ylabel("Fires")
plt.tight_layout(); fig.savefig(OUT / "p2_04_sensitivity.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p2_04_sensitivity.png")

# ── 6. Fire rate by tenure pie (bonus) ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))
ten_fires = agg.groupby('tenure')['fires'].sum().sort_values()
ax.pie(ten_fires.values, labels=ten_fires.index, autopct="%1.1f%%",
       colors=sns.color_palette("YlOrRd", len(ten_fires)), startangle=90)
ax.set_title("Fire Distribution by Tenure Type", fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "p2_05_tenure_pie.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ p2_05_tenure_pie.png")

# ── 7. Allocation table ────────────────────────────────────────────────
print(f"\n{'='*60}")
print("RESOURCE ALLOCATION PLAN")
print(f"{'='*60}")
print(f"{'State':10s} {'Fires':>8s} {'Heavy':>6s} {'Light':>6s} {'Crews':>7s} {'Heli':>5s} {'Budget':>14s}")
print("-"*60)
for _, r in alloc.iterrows():
    print(f"{r['state']:10s} {r['fires']:>8d} {r['appliance_heavy']:>6d} {r['appliance_light']:>6d} {r['crew_member']:>7d} {r['helicopter']:>5d} ${r['budget']:>10,}")
print("-"*60)
print(f"{'TOTAL':10s} {alloc['fires'].sum():>8d} {'':>6s} {'':>6s} {'':>7s} {'':>5s} ${alloc['budget'].sum():>10,}")
print(f"\nSENSITIVITY:")
print(f"{'Scenario':15s} {'Fires':>10s} {'Budget':>16s}")
print("-"*45)
for i,s in enumerate(scenarios):
    print(f"{s:15s} {fires[i]:>10,d} ${budgets[i]:>12,}")

print(f"\n{'='*50}")
print(f"PROJECT 2 COMPLETE — 7 charts saved to {OUT}")
print(f"{'='*50}")
