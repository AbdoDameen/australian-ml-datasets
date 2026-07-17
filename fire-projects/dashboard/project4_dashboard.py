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
        # 📈 Project 4: Bushfire Analytics Dashboard

        Ties together all 3 projects into a single interactive overview.
        Explore fire risk, resource allocation, and burn scar data from one place.

        **Projects:** ① Risk Prediction ② Resource Allocation ③ Burn Scar Mapping
        """
    )


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    import json
    import warnings
    warnings.filterwarnings('ignore')
    sns.set_theme(style="whitegrid", palette="muted")
    return Path, json, np, pd, plt, sns, warnings


# ─── LOAD ALL PROJECT DATA ─────────────────────────────────────────────────

@app.cell
def _(Path, json, np, pd):
    base = Path("..")

    # Project 1
    p1_csv = base / "risk-prediction" / "processed" / "forest_fire_risk_clean.csv"
    if p1_csv.exists():
        df1 = pd.read_csv(p1_csv)
        state_cols = [c for c in df1.columns if c.startswith('state_')]
        tenure_cols = [c for c in df1.columns if c.startswith('tenure_')]
        df1 = None
        print("❌ Project 1 data not found — run project1 first")

    # Project 2
    p2_json = base / "resource-allocation" / "outputs" / "resource_allocation_plan.json"
    if p2_json.exists():
        with open(p2_json) as f:
            plan = json.load(f)
        df2 = pd.DataFrame(plan['allocation'])
        print(f"✅ Project 2: {len(df2)} states, ${plan['total_budget_aud']:,} budget")
    else:
        df2 = None
        plan = None
        print("❌ Project 2 data not found")

    # Project 3
    p3_mask = base / "burn-scar-mapping" / "outputs" / "burn_mask.npy"
    p3_diff = base / "burn-scar-mapping" / "outputs" / "ndvi_diff.npy"
    if p3_mask.exists() and p3_diff.exists():
        burn_mask = np.load(p3_mask)
        ndvi_diff = np.load(p3_diff)
        print(f"✅ Project 3: burn_mask {burn_mask.shape}, {burn_mask.mean()*100:.1f}% burned")
    else:
        burn_mask = None
        ndvi_diff = None
        print("❌ Project 3 data not found")

    return base, burn_mask, df1, df2, ndvi_diff, p1_csv, p2_json, p3_diff, p3_mask, plan


# ─── DASHBOARD OVERVIEW ────────────────────────────────────────────────────

@app.cell
def _(df1, df2, plan, plt, sns):
    __fig = plt.figure(figsize=(16, 10))
    __fig.suptitle("Bushfire Analytics Dashboard — Project Overview", fontsize=16, fontweight="bold")

    # Top-left: Fire rate by state (1)
    ax1 = _fig.add_subplot(3, 3, 1)
    if df1 is not None:
        _state_cols = [c for c in df1.columns if c.startswith('state_')]
        __rates = []
        for _sc in _state_cols:
            _name = _sc.replace('state_', '')
            _sub = df1[df1[_sc] == 1]
            if len(_sub):
                __rates.append({'state': _name, 'fire_rate': _sub['unplanned_5'].mean()})
        __rates_df = pd.DataFrame(__rates).sort_values('fire_rate')
        colors = ["#d9534f" if v > 0.15 else "#f0ad4e" if v > 0.05 else "#5cb85c" for v in rates_df['fire_rate']]
        ax1.barh(__rates_df['state'], rates_df['fire_rate'], color=colors)
        ax1.set_title("Unplanned Fire Rate by State", fontweight="bold")
        ax1.set_xlabel("Rate")

    # Top-center: Budget allocation (2)
    ax2 = fig.add_subplot(3, 3, 2)
    if df2 is not None:
        df2_sorted = df2.sort_values('budget', ascending=True)
        ax2.barh(df2_sorted['state'], df2_sorted['budget'] / 1e9,
                 color=sns.color_palette("Blues_r", len(df2_sorted)))
        ax2.set_title("Budget Allocation by State ($B)", fontweight="bold")
        ax2.set_xlabel("$ Billions")

    # Top-right: Resource breakdown (2)
    ax3 = fig.add_subplot(3, 3, 3)
    if df2 is not None:
        res = df2.melt(id_vars='state',
                       value_vars=['appliance_heavy', 'appliance_light', 'crew_member'],
                       var_name='resource', value_name='count')
        sns.barplot(data=res, x='resource', y='count', hue='state', ax=ax3, palette="Set2")
        ax3.set_title("Resource Requirements", fontweight="bold")
        ax3.tick_params(axis='x', rotation=30)

    # Mid-left: Tenure risk (1)
    ax4 = fig.add_subplot(3, 3, 4)
    if df1 is not None:
        ten_cols = [c for c in df1.columns if c.startswith('tenure_')]
        ten_rates = []
        for tc in ten_cols:
            _name = tc.replace('tenure_', '')
            _sub = df1[df1[tc] == 1]
            if len(_sub):
                ten___rates.append({'tenure': _name, 'fire_rate': _sub['unplanned_5'].mean()})
        ten_df = pd.DataFrame(ten_rates).sort_values('fire_rate')
        colors = ["#d9534f" if v > 0.15 else "#f0ad4e" if v > 0.05 else "#5cb85c" for v in ten_df['fire_rate']]
        ax4.barh(ten_df['tenure'], ten_df['fire_rate'], color=colors)
        ax4.set_title("Fire Risk by Tenure Type", fontweight="bold")
        ax4.set_xlabel("Rate")

    # Mid-center: Sensitivity (2)
    ax5 = fig.add_subplot(3, 3, 5)
    if plan:
        scenarios = ['Base', '+10%', '+20%', '+30%', '+50%']
        mults = [1.0, 1.1, 1.2, 1.3, 1.5]
        budgets = [plan['total_budget_aud'] * m / 1e9 for m in mults]
        ax5.plot(scenarios, budgets, 'o-', color="#d9534f", lw=2, ms=8)
        ax5.fill_between(range(len(scenarios)), budgets, alpha=0.15, color="#d9534f")
        ax5.set_title("Budget Sensitivity", fontweight="bold")
        ax5.set_ylabel("$ Billions")

    # Mid-right: Prior burns distribution (1)
    ax6 = fig.add_subplot(3, 3, 6)
    if df1 is not None and 'prior_burns' in df1.columns:
        burns = df1[df1['prior_burns'] >= 0]['prior_burns']
        sns.histplot(burns, bins=6, discrete=True, ax=ax6, color="#f0ad4e")
        ax6.set_title("Burn Frequency Distribution", fontweight="bold")
        ax6.set_xlabel("Number of Burns")

    # Bottom: Key metrics
    ax7 = fig.add_subplot(3, 3, (7, 9))
    ax7.axis("off")
    stats = []
    if df1 is not None:
        stats.append(f"🌲 Forest regions analyzed: {len(df1):,}")
        stats.append(f"🔥 Unplanned fire rate: {df1['unplanned_5'].mean()*100:.1f}%")
        if 'prior_burns' in df1.columns:
            stats.append(f"📊 Avg prior burns: {df1['prior_burns'].mean():.1f}")
    if plan:
        stats.append(f"💰 Total budget: ${plan['total_budget_aud']:,}")
        stats.append(f"🔮 Predicted fires: {plan['total_predicted_fires']:,}")
    if burn_mask is not None:
        stats.append(f"🛰️ Burn scar: {burn_mask.mean()*100:.1f}% of scene")

    ax7.text(0.02, 0.5, "\n".join(stats), fontsize=14, va="center",
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#dee2e6"))
    ax7.set_title("Key Metrics", fontweight="bold")

    plt.tight_layout()
    fig


# ─── COMPARISON: FIRE RATE × BUDGET ───────────────────────────────────────

@app.cell
def _(df1, df2, plt, sns):
    _out = None
    if df1 is not None and df2 is not None:
        _state_cols = [c for c in df1.columns if c.startswith('state_')]
        rates = {}
        for _sc in _state_cols:
            _name = _sc.replace('state_', '')
            _sub = df1[df1[_sc] == 1]
            if len(_sub):
                rates[_name] = _sub['unplanned_5'].mean()

        comp = df2.copy()
        comp['fire_rate'] = comp['state'].map(rates)
        comp = comp.dropna()

        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(comp['fire_rate'], comp['budget'] / 1e9,
                            s=comp['fires'] * 2, c=range(len(comp)),
                            cmap="YlOrRd", alpha=0.7, edgecolors="black", linewidth=0.5)
        for _, r in comp.iterrows():
            ax.annotate(r['state'], (r['fire_rate'], r['budget'] / 1e9),
                       fontsize=10, ha='center', va='bottom')
        ax.set_xlabel("Fire Rate (2020-21)")
        ax.set_ylabel("Budget ($ Billions)")
        ax.set_title("Budget vs Fire Rate by State\n(Bubble size = predicted fire count)",
                    fontweight="bold")
        plt.tight_layout()
        _out = fig
    else:
        _out = print("Need both Project 1 and 2 data for comparison view")
    return comp, _rates, scatter,


# ─── BURN SCAR STATS ──────────────────────────────────────────────────────

@app.cell
def _(burn_mask, ndvi_diff, np, plt, sns):
    if burn_mask is not None and ndvi_diff is not None:
        _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))

        # Burn scar size distribution
        from scipy import ndimage as ndi
        labeled, n_features = ndi.label(burn_mask)
        sizes = pd.Series([(labeled == i).sum() for i in range(1, n_features + 1)])
        if len(sizes) > 0:
            sns.histplot(sizes, bins=30, ax=axes[0], color="#d9534f")
            axes[0].set_title(f"Burn Patch Size Distribution ({n_features} patches)",
                             fontweight="bold")
            axes[0].set_xlabel("Patch Size (pixels)")
            axes[0].set_ylabel("Count")

        # NDVI diff distribution (burned vs unburned)
        diff_burned = ndvi_diff[burn_mask]
        diff_unburned = ndvi_diff[~burn_mask]
        sns.histplot(diff_unburned, bins=50, alpha=0.5, label="Unburned",
                    ax=_axes[1], color="#2d6a2f")
        sns.histplot(diff_burned, bins=50, alpha=0.5, label="Burned",
                    ax=_axes[1], color="#d9534f")
        axes[1].set_title("NDVI Change: Burned vs Unburned Areas", fontweight="bold")
        axes[1].set_xlabel("NDVI Difference (Pre − Post)")
        axes[1].legend()

        plt.tight_layout()
        fig
    else:
        _out2 = print("Run Project 3 first for burn scar data")
        diff_burned = diff_unburned = labeled = n_features = ndi = sizes = None
    _ = _out2


# ─── COMBINED DATA TABLE ──────────────────────────────────────────────────

@app.cell
def _(df1, df2):
    if df1 is not None and df2 is not None:
        _state_cols = [c for c in df1.columns if c.startswith('state_')]
        summary = []
        for _sc in _state_cols:
            _name = _sc.replace('state_', '')
            _sub = df1[df1[_sc] == 1]
            if len(_sub):
                alloc_row = df2[df2['state'] == _name]
                budget = alloc_row['budget'].values[0] if len(alloc_row) > 0 else 0
                summary.append({
                    'State': _name,
                    'Regions': len(_sub),
                    'Fire Rate': f"{_sub['unplanned_5'].mean()*100:.1f}%",
                    'Avg Prior Burns': f"{_sub['prior_burns'].mean():.2f}",
                    'Budget ($M)': f"${budget/1e6:.0f}M" if budget else "N/A"
                })
        _ = pd.DataFrame(summary)
        _summary_df = _
    else:
        _summary_df = "Run projects 1 and 2 first"
    _summary_df


# ─── HOW TO USE ────────────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _():
    print("=" * 60)
    print("TO RUN THIS DASHBOARD:")
    print("=" * 60)
    print()
    print("  1. Run all 3 project notebooks first:")
    print("     marimo edit project-1-risk-prediction/project1_fire_risk.py")
    print("     marimo edit project-2-resource-allocation/project2_resource_allocation.py")
    print("     marimo edit project-3-burn-scar-mapping/project3_burn_scar.py")
    print()
    print("  2. Then run this dashboard:")
    print("     marimo edit project-4-dashboard/project4_dashboard.py")
    print()
    print("  All data is passed through shared processed/ and outputs/ folders.")


if __name__ == "__main__":
    app.run()
