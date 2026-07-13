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
        # 📊 Project 2: Fire Resource Allocation Optimisation

        Forecast seasonal fire demand and allocate resources (appliances, crews, helicopters) with budget estimates.
        Designed for fire service procurement and operational planning.

        **Model:** Gradient Boosting Regressor | **Data:** ABARES (via Project 1)
        """
    )


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    import warnings
    warnings.filterwarnings('ignore')
    sns.set_theme(style="whitegrid", palette="muted")
    return (
        GradientBoostingRegressor, Path, mean_absolute_error, np, pd, plt,
        r2_score, sns, train_test_split, warnings
    )


# ─── LOAD ───────────────────────────────────────────────────────────────────

@app.cell
def _(Path, pd):
    csv = Path("../project-1-risk-prediction/processed/forest_fire_risk_clean.csv")
    if not csv.exists():
        csv = Path("../../daily-datasets/climate/bushfire-history/raw/Fire_For16-21_Attributes.csv")
        raw = pd.read_csv(csv)
        # Resample to Project 1 format
        forest = raw[raw['FOREST'] == 1].copy()
        forest = forest[forest['STATE'].notna() & (forest['STATE'].str.strip() != '')]
        forest = forest[forest['FOR_BURNS'] >= 0]
        df = forest
        print(f"Loaded raw ABARES data: {len(df):,} rows")
    else:
        df = pd.read_csv(csv)
        print(f"Loaded Project 1 output: {len(df):,} rows")
    df.head(3)
    return csv, df, forest, raw


# ─── AGGREGATE ──────────────────────────────────────────────────────────────

@app.cell
def _(df, pd, plt, sns):
    # Build state-tenure-prior_burns groups
    state_cols = [c for c in df.columns if c.startswith('state_')]
    tenure_cols = [c for c in df.columns if c.startswith('tenure_')]

    agg_data = []
    for sc in state_cols:
        sname = sc.replace('state_', '')
        for tc in tenure_cols:
            tname = tc.replace('tenure_', '')
            sub = df[(df[sc] == 1) & (df[tc] == 1)]
            if len(sub) > 0:
                agg_data.append({
                    'state': sname, 'tenure': tname,
                    'region_count': len(sub),
                    'pixel_count': sub['COUNT'].sum() if 'COUNT' in sub.columns else len(sub),
                    'fires': sub['unplanned_5'].sum(),
                    'fire_rate': sub['unplanned_5'].mean(),
                    'avg_prior_burns': sub['prior_burns'].mean() if 'prior_burns' in sub.columns else 0
                })
    agg = pd.DataFrame(agg_data)
    print(f"Aggregated into {len(agg)} state-tenure groups")
    print(f"Total predicted fires: {agg['fires'].sum():,}")
    agg.head(10)
    return agg, agg_data, sc, sname, state_cols, sub, tc, tenure_cols, tname


# ─── FIRE RATE BY STATE ────────────────────────────────────────────────────

@app.cell
def _(agg, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(16, 5))

    # Total fires by state
    state_fires = agg.groupby('state')['fires'].sum().sort_values()
    _colors = sns.color_palette("Reds_r", len(state_fires))
    axes[0].bar(state_fires.index, state_fires.values, color=_colors)
    axes[0].set_title("Total Predicted Fires by State", fontweight="bold")
    axes[0].set_ylabel("Fires")
    axes[0].tick_params(axis='x', rotation=45)

    # Fire rate by state
    state_rate = agg.groupby('state')['fire_rate'].mean().sort_values()
    axes[1].bar(state_rate.index, state_rate.values, color=sns.color_palette("Oranges_r", len(state_rate)))
    axes[1].set_title("Mean Fire Rate by State (2020-21)", fontweight="bold")
    axes[1].set_ylabel("Fire Rate")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig
    return state_fires, state_rate


# ─── RESOURCE DEMAND MODEL ─────────────────────────────────────────────────

@app.cell
def _(GradientBoostingRegressor, agg, np, plt, r2_score, mean_absolute_error, sns, train_test_split):
    # Resource costs (illustrative AUD)
    resource_costs = {
        'appliance_heavy': 2_500_000, 'appliance_light': 800_000,
        'crew_member': 120_000, 'helicopter': 5_000_000
    }
    resources_per_fire = {
        'appliance_heavy': 0.3, 'appliance_light': 0.8,
        'crew_member': 4.0, 'helicopter': 0.05
    }

    # Features: state (one-hot), tenure (one-hot) — from the agg data
    feat = pd.get_dummies(agg[['state', 'tenure']], drop_first=False).astype(int)
    feat['pixel_count'] = agg['pixel_count']

    X = feat.values
    y = agg['fires'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(n_estimators=150, max_depth=4, min_samples_leaf=20, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Predict for all groups
    agg['predicted_fires'] = model.predict(feat.values).clip(0)

    print(f"Model R²: {r2:.4f}")
    print(f"MAE: {mae:.2f} fires per group")

    # Build allocation by state
    allocation = []
    for s in agg['state'].unique():
        sdata = agg[agg['state'] == s]
        total_fires = max(0, int(sdata['predicted_fires'].sum()))

        resources = {}
        for rsrc, rate in resources_per_fire.items():
            resources[rsrc] = max(1, int(np.ceil(total_fires * rate)))

        budget = sum(resources[r] * resource_costs[r] for r in resources)
        allocation.append({'state': s, 'fires': total_fires, **resources, 'budget': budget})

    alloc = pd.DataFrame(allocation).sort_values('fires', ascending=False)
    total_budget = alloc['budget'].sum()
    total_fires = alloc['fires'].sum()

    print(f"\nTotal fires: {total_fires:,}")
    print(f"Total budget: ${total_budget:,}")
    alloc
    return (
        X, X_test, X_train, X_test, X_train, alloc, allocation,
        feat, mae, model, r2, resource_costs, resources_per_fire,
        s, sdata, total_budget, total_fires, y, y_pred, y_test, y_train,
    )


# ─── ALLOCATION BAR CHART ──────────────────────────────────────────────────

@app.cell
def _(alloc, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(16, 5))

    _colors = sns.color_palette("Reds", len(alloc))
    axes[0].bar(alloc['state'], alloc['fires'], color=colors)
    axes[0].set_title("Predicted Fires by State", fontweight="bold")
    axes[0].set_ylabel("Fires")

    budget_billions = alloc['budget'] / 1e9
    axes[1].bar(alloc['state'], budget_billions, color=sns.color_palette("Blues", len(alloc)))
    axes[1].set_title("Budget Allocation by State ($ Billions)", fontweight="bold")
    axes[1].set_ylabel("Budget ($B)")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig
    return budget_billions,


# ─── RESOURCE BREAKDOWN ────────────────────────────────────────────────────

@app.cell
def _(alloc, plt, sns):
    _fig, _ax = plt.subplots(figsize=(14, 6))

    melt = alloc.melt(id_vars=['state', 'fires', 'budget'],
                      value_vars=['appliance_heavy', 'appliance_light', 'crew_member', 'helicopter'],
                      var_name='resource', value_name='count')

    sns.barplot(data=melt, x='state', y='count', hue='resource', ax=ax, palette="Set2")
    ax.set_title("Resource Requirements by State", fontweight="bold")
    ax.set_ylabel("Units Required")
    ax.legend(title="Resource Type")
    plt.tight_layout()
    fig
    return melt,


# ─── SENSITIVITY ANALYSIS ──────────────────────────────────────────────────

@app.cell
def _(alloc, np, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(16, 5))

    scenarios = ['Baseline', '+10%', '+20%', '+30%', '+50%']
    multipliers = [1.0, 1.1, 1.2, 1.3, 1.5]

    base_budget = alloc['budget'].sum()
    budgets = [int(base_budget * m) for m in multipliers]
    base_fires = alloc['fires'].sum()
    fires = [int(base_fires * m) for m in multipliers]

    axes[0].plot(scenarios, [b / 1e9 for b in budgets], 'o-', color="#d9534f", linewidth=2, markersize=8)
    axes[0].fill_between(range(len(scenarios)), [b / 1e9 for b in budgets], alpha=0.15, color="#d9534f")
    axes[0].set_title("Budget Sensitivity to Fire Season Severity", fontweight="bold")
    axes[0].set_ylabel("Budget ($B)")
    axes[0].set_xlabel("Scenario")

    axes[1].plot(scenarios, fires, 's-', color="#f0ad4e", linewidth=2, markersize=8)
    axes[1].fill_between(range(len(scenarios)), fires, alpha=0.15, color="#f0ad4e")
    axes[1].set_title("Fire Volume Sensitivity", fontweight="bold")
    axes[1].set_ylabel("Predicted Fires")
    axes[1].set_xlabel("Scenario")

    plt.tight_layout()
    fig
    return base_budget, base_fires, budgets, fires, multipliers, scenarios


# ─── ALLOCATION TABLE ──────────────────────────────────────────────────────

@app.cell
def _(alloc):
    print("=" * 60)
    print("RESOURCE ALLOCATION PLAN")
    print("=" * 60)
    print(f"{'State':10s} {'Fires':>8s} {'Heavy':>6s} {'Light':>6s} {'Crews':>7s} {'Heli':>5s} {'Budget':>14s}")
    print("-" * 60)
    for _, r in alloc.iterrows():
        b = f"${r['budget']:>10,}"
        print(f"{r['state']:10s} {r['fires']:>8d} {r['appliance_heavy']:>6d} {r['appliance_light']:>6d} {r['crew_member']:>7d} {r['helicopter']:>5d} {b}")
    print("-" * 60)
    print(f"{'TOTAL':10s} {sum(alloc['fires']):>8d} {'':>6s} {'':>6s} {'':>7s} {'':>5s} ${sum(alloc['budget']):>10,}")


# ─── SENSITIVITY TABLE ─────────────────────────────────────────────────────

@app.cell
def _(base_budget, base_fires, budgets, fires, multipliers, scenarios):
    print("\nSENSITIVITY ANALYSIS")
    print(f"{'Scenario':15s} {'Fires':>10s} {'Budget':>16s} {'Additional':>16s}")
    print("-" * 60)
    for i, _s in enumerate(scenarios):
        add = budgets[i] - base_budget
        print(f"{_s:15s} {fires[i]:>10,d} ${budgets[i]:>12,d} ${add:>12,d}")


if __name__ == "__main__":
    app.run()
