# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas",
#     "numpy",
#     "scikit-learn",
#     "matplotlib",
#     "seaborn",
# ]
# ///
# -*- coding: utf-8 -*-
"""
ABARES Forest Fire Data Explorer — Marimo notebook

Opens the ABARES fire attribute table and lets you explore fire patterns
interactively by state, tenure type, and forest category.

Usage:  marimo edit abares_explorer.py
"""

import marimo

__generated_with = "0.23.14"
app = marimo.App()


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        # 🔥 ABARES Forest Fire Data Explorer

        Interactive exploration of Australia's forest fire records (2016–2021).

        Data source: ABARES (agriculture.gov.au/abares/forestsaustralia)
        """
    )
    return


@app.cell
def __():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    return pd, np, plt, sns, Path


@app.cell
def __(pd, Path):
    # Load the ABARES fire data
    csv_path = Path("../daily-datasets/climate/bushfire-history/raw/Fire_For16-21_Attributes.csv")
    df = pd.read_csv(csv_path)
    df
    return df, csv_path


@app.cell
def __(df, pd):
    # Decode ALL_FIRE — each position = one fire season
    def parse_fire(s):
        s = str(s).strip().ljust(5)
        return [1 if i < len(s) and s[i] == 'U' else 0 for i in range(5)]

    fire_cols = df['ALL_FIRE'].apply(parse_fire)
    fire_df = pd.DataFrame(fire_cols.tolist(),
                           columns=[f'unplanned_{y}' for y in range(1, 6)])
    df_explore = pd.concat([df, fire_df], axis=1)
    df_explore['any_fire'] = (df_explore['FOR_BURNS'] > 0).astype(int)

    # Summary
    print(f"Total regions: {len(df_explore):,}")
    print(f"States: {df_explore['STATE'].unique()}")
    print(f"Tenure types: {df_explore['FOR_TEN'].unique()}")
    print(f"Mean burns: {df_explore[df_explore['FOR_BURNS'] >= 0]['FOR_BURNS'].mean():.2f}")
    df_explore[['STATE', 'FOR_TEN', 'FOR_CATEGO', 'FOR_BURNS', 'any_fire']].head(10)
    return df_explore, fire_cols, fire_df, parse_fire


@app.cell
def __(df_explore, plt, sns):
    # Fire count by state
    burns = df_explore[df_explore['FOR_BURNS'] >= 0]
    state_burns = burns.groupby('STATE')['FOR_BURNS'].mean().sort_values()

    plt.figure(figsize=(10, 5))
    state_burns.plot(kind='barh', color='#d9534f')
    plt.xlabel('Mean Number of Burns (2016-2021)')
    plt.title('Fire Frequency by State / Territory')
    plt.tight_layout()
    plt.gca()
    return burns, state_burns


@app.cell
def __(df_explore, plt, sns):
    # Fire rate by tenure type
    tenure_fire = df_explore[df_explore['FOR_BURNS'] >= 0].groupby('FOR_TEN')['unplanned_5'].mean().sort_values()

    plt.figure(figsize=(10, 5))
    colors = ['#5cb85c' if v < 0.1 else '#f0ad4e' if v < 0.2 else '#d9534f' for v in tenure_fire.values]
    tenure_fire.plot(kind='barh', color=colors)
    plt.xlabel('Unplanned Fire Rate (2020-21 Season)')
    plt.title('Wildfire Risk by Tenure Type')
    plt.tight_layout()
    plt.gca()
    return tenure_fire, colors


@app.cell
def __(df_explore):
    # Filterable table — change the state filter below
    state_filter = "NSW"
    subset = df_explore[
        (df_explore['STATE'] == state_filter) &
        (df_explore['FOR_BURNS'] >= 0)
    ]
    print(f"Rows for {state_filter}: {len(subset)}")
    subset.groupby('FOR_TEN')[['FOR_BURNS', 'unplanned_5']].agg(['mean', 'count'])
    return state_filter, subset


@app.cell
def __(df_explore):
    # Top 10 highest-risk regions
    high_risk = df_explore[
        (df_explore['FOREST'] == 1) &
        (df_explore['FOR_BURNS'] >= 0)
    ].nlargest(10, 'FOR_BURNS')
    high_risk[['STATE', 'FOR_TEN', 'FOR_CATEGO', 'FOR_BURNS', 'unplanned_5', 'COUNT']]
    return high_risk,


if __name__ == "__main__":
    app.run()
