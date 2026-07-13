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
        # 🔥 Project 1: Forest Fire Risk Prediction

        Predict unplanned forest fires across Australia using tenure type, forest category, and prior fire history.

        **Data:** ABARES Forest Fire 2016–2021 (agriculture.gov.au/abares/forestsaustralia)
        **Model:** Random Forest Classifier
        """
    )


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, RocCurveDisplay
    import warnings
    warnings.filterwarnings('ignore')
    sns.set_theme(style="whitegrid", palette="muted")

    return (
        Path, RandomForestClassifier, RocCurveDisplay, StandardScaler,
        classification_report, confusion_matrix, np, pd, plt,
        roc_auc_score, sns, train_test_split, warnings
    )


# ─── LOAD ───────────────────────────────────────────────────────────────────

@app.cell
def _(Path, pd):
    csv = Path("../daily-datasets/climate/bushfire-history/raw/Fire_For16-21_Attributes.csv")
    df = pd.read_csv(csv)
    print(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    df
    return csv, df


# ─── PARSE FIRE PATTERNS ────────────────────────────────────────────────────

@app.cell
def _(df, np, pd):
    def parse_fire(s):
        s = str(s).strip().ljust(5)
        return [1 if i < len(s) and s[i] == 'U' else 0 for i in range(5)]

    fire_cols = df['ALL_FIRE'].apply(parse_fire)
    fire_df = pd.DataFrame(fire_cols.tolist(), columns=[f'unplanned_{i}' for i in range(1, 6)])
    df2 = pd.concat([df, fire_df], axis=1)
    df2['any_unplanned_prior'] = df2[[f'unplanned_{i}' for i in range(1, 5)]].sum(axis=1).clip(0, 1)
    df2['total_burns'] = df2['FOR_BURNS'].clip(0, 5)
    print(f"Decoded {len(fire_df)} fire patterns")
    print(f"Unplanned fire rate in 2020-21: {df2['unplanned_5'].mean()*100:.1f}%")
    df2[['STATE', 'FOR_TEN', 'FOR_CATEGO', 'FOR_BURNS', 'unplanned_5']].head()
    return df2, fire_cols, fire_df, parse_fire


# ─── EDA: STATE DISTRIBUTION ────────────────────────────────────────────────

@app.cell
def _(df2, plt, sns):
    forest = df2[df2['FOREST'] == 1].copy()

    _fig, _axes = plt.subplots(1, 3, figsize=(18, 5))
    _fig.suptitle("Forest Fire Data Overview", fontsize=14, fontweight="bold")

    # 1) Pixel count by state
    state_counts = forest['STATE'].value_counts()
    _axes[0].barh(state_counts.index, state_counts.values, color=sns.color_palette("Reds_r", len(state_counts)))
    _axes[0].set_xlabel("Pixels (thousands)")
    _axes[0].set_title("Forest Regions by State")

    # 2) Burn count distribution
    burns = forest[forest['FOR_BURNS'] >= 0]
    sns.histplot(burns['FOR_BURNS'], bins=6, discrete=True, _ax=axes[1], color="#d9534f")
    _axes[1].set_xlabel("Number of Burns (2016-2021)")
    _axes[1].set_ylabel("Pixel Count")
    _axes[1].set_title("Fire Frequency Distribution")

    # 3) Tenure type breakdown
    tenure_counts = forest['FOR_TEN'].value_counts()
    colors = sns.color_palette("YlOrRd", len(tenure_counts))
    _axes[2].pie(tenure_counts.values, labels=tenure_counts.index, autopct="%1.1f%%",
                colors=colors, startangle=90)
    _axes[2].set_title("Land Tenure Breakdown")

    plt.tight_layout()
    _fig
    return _axes, burns, _fig, forest, state_counts, tenure_counts


# ─── EDA: FIRE RATE BY STATE ────────────────────────────────────────────────

@app.cell
def _(burns, plt, sns):
    _fig_a, _axes = plt.subplots(1, 2, figsize=(16, 5))

    # Avg burns by state
    state_avg = burns.groupby('STATE')['FOR_BURNS'].mean().sort_values()
    _colors = ["#d9534f" if v > 1.5 else "#f0ad4e" if v > 0.5 else "#5cb85c" for v in state_avg.values]
    axes[0].barh(state_avg.index, state_avg.values, color=_colors)
    _axes[0].set_xlabel("Mean Burns (2016-2021)")
    _axes[0].set_title("Average Fire Frequency by State")

    # Avg burns by tenure
    ten_avg = burns.groupby('FOR_TEN')['FOR_BURNS'].mean().sort_values()
    _colors2 = ["#d9534f" if v > 2 else "#f0ad4e" if v > 1 else "#5cb85c" for v in ten_avg.values]
    axes[1].barh(ten_avg.index, ten_avg.values, color=_colors2)
    _axes[1].set_xlabel("Mean Burns (2016-2021)")
    _axes[1].set_title("Average Fire Frequency by Tenure Type")

    plt.tight_layout()
    fig
    return state_avg, ten_avg


# ─── EDA: STATE × TENURE HEATMAP ────────────────────────────────────────────

@app.cell
def _(burns, plt, sns):
    # Fire rate heatmap: state x tenure
    heat = burns.groupby(['STATE', 'FOR_TEN'])['unplanned_5'].mean().unstack()

    _fig, _ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(heat, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5,
                cbar_kws={"label": "Unplanned Fire Rate (2020-21)"}, _ax=_ax)
    _ax.set_title("Wildfire Risk: State × Tenure Type", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig


# ─── EDA: BOXPLOT ──────────────────────────────────────────────────────────

@app.cell
def _(burns, plt, sns):
    __fig, _axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.boxplot(data=burns, x='FOR_TEN', y='FOR_BURNS', _ax=axes[0],
                palette="YlOrRd", order=sorted(burns['FOR_TEN'].unique()))
    _axes[0].set_title("Burn Count Distribution by Tenure", fontweight="bold")
    _axes[0].set_xlabel("Tenure Type")
    axes[0].set_ylabel("Total Burns (2016-2021)")

    sns.boxplot(data=burns, x='STATE', y='FOR_BURNS', _ax=axes[1],
                palette="RdYlGn_r", order=sorted(burns['STATE'].unique()))
    _axes[1].set_title("Burn Count Distribution by State", fontweight="bold")
    _axes[1].set_xlabel("State")
    _axes[1].set_ylabel("Total Burns (2016-2021)")

    plt.tight_layout()
    fig


# ─── ML: PREPARE FEATURES ──────────────────────────────────────────────────

@app.cell
def _(RandomForestClassifier, StandardScaler, df2, forest, np, pd, plt, sns, train_test_split):
    # Feature engineering
    ml = forest[forest['FOR_BURNS'] >= 0].copy()
    ml = ml[ml['STATE'].notna() & (ml['STATE'].str.strip() != '')]

    features = pd.get_dummies(ml[['STATE', 'FOR_TEN', 'FOR_CATEGO']], drop_first=False).astype(int)
    features['prior_burns'] = ml['FOR_BURNS']
    features['any_unplanned_prior'] = ml['any_unplanned_prior']

    # Target: unplanned fire in 2020-21 season
    y = ml['unplanned_5'].values
    X = features.values

    X = np.nan_to_num(X, nan=0.0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=200, max_depth=12,
                                   min_samples_leaf=50, class_weight='balanced',
                                   random_state=42, n_jobs=-1)
    model.fit(X_train_s, y_train)

    y_pred = model.predict(X_test_s)
    y_proba = model.predict_proba(X_test_s)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    print(f"Features: {X_train.shape[1]}")
    print(f"Class balance: {y.mean()*100:.1f}% positive")
    print(f"ROC-AUC: {auc:.4f}")

    # Feature importance
    imp = pd.DataFrame({'feature': features.columns, 'importance': model.feature_importances_})
    imp = imp.sort_values('importance', ascending=False).head(15)

    (X, X_test, X_test_s, X_train, X_train_s,
     auc, cm, features, imp, ml, model, scaler, y,
     y_pred, y_proba, y_test, y_train)
    return (
        X, X_test, X_test_s, X_train, X_train_s, auc, cm, features, imp,
        ml, model, scaler, y, y_pred, y_proba, y_test, y_train
    )


# ─── ML: CONFUSION MATRIX ──────────────────────────────────────────────────

@app.cell
def _(cm, plt, sns):
    _fig_b, _ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["No Fire", "Fire"], yticklabels=["No Fire", "Fire"], _ax=_ax)
    _ax.set_xlabel("Predicted")
    _ax.set_ylabel("Actual")
    _ax.set_title("Confusion Matrix — Random Forest", fontweight="bold")
    fig


# ─── ML: FEATURE IMPORTANCE ────────────────────────────────────────────────

@app.cell
def _(imp, plt, sns):
    _fig_b2, _ax = plt.subplots(figsize=(12, 6))
    _colors = ["#d9534f" if i < 3 else "#f0ad4e" if i < 6 else "#5cb85c" for i in range(len(imp))]
    sns.barplot(data=imp, y='feature', x='importance', palette=colors, _ax = _ax)
    _ax.set_xlabel("Importance")
    _ax.set_ylabel("")
    _ax.set_title("Top 15 Feature Importances", fontweight="bold")
    fig


# ─── ML: FIRE RATE BY STATE + TENURE (MODEL INSIGHT) ──────────────────────

@app.cell
def _(ml, plt, sns):
    _fig_a, _axes = plt.subplots(1, 2, figsize=(16, 5))

    # Fire rate by state (model target)
    rate_state = ml.groupby('STATE')['unplanned_5'].mean().sort_values()
    axes[0].bar(rate_state.index, rate_state.values, color=sns.color_palette("Reds", len(rate_state)))
    _axes[0].set_title("2020-21 Unplanned Fire Rate by State", fontweight="bold")
    axes[0].set_ylabel("Fire Rate")
    axes[0].tick_params(axis='x', rotation=45)

    # Fire rate by tenure
    rate_ten = ml.groupby('FOR_TEN')['unplanned_5'].mean().sort_values()
    axes[1].bar(rate_ten.index, rate_ten.values, color=sns.color_palette("Oranges", len(rate_ten)))
    _axes[1].set_title("2020-21 Unplanned Fire Rate by Tenure", fontweight="bold")
    _axes[1].set_ylabel("Fire Rate")
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig


# ─── TOP RISK REGIONS ──────────────────────────────────────────────────────

@app.cell
def _(ml, plt, sns):
    high_risk = ml[ml['unplanned_5'] == 1]
    top = high_risk.groupby(['STATE', 'FOR_TEN']).size().reset_index(name='count')
    top = top.sort_values('count', ascending=False).head(15)

    _figx2, _ax = plt.subplots(figsize=(12, 6))
    top['label'] = top['STATE'] + " — " + top['FOR_TEN']
    sns.barplot(data=top, y='label', x='count', palette="Reds_r", _ax=_ax)
    _ax.set_xlabel("Number of High-Risk Regions")
    _ax.set_ylabel("")
    _ax.set_title("Top 15 Highest-Risk Region-Tenure Combinations", fontweight="bold")
    fig


# ─── SUMMARY ───────────────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(auc, ml, model, y_pred, y_test):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("=" * 50)
    print("MODEL PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"ROC-AUC:      {auc:.4f}")
    print(f"Accuracy:     {acc:.4f}")
    print(f"Precision:    {prec:.4f}")
    print(f"Recall:       {rec:.4f}")
    print(f"F1-Score:     {f1:.4f}")
    print(f"Features:     {model.n_features_in_}")
    print(f"Trees:        {model.n_estimators}")
    print(f"Fire rate:    {ml['unplanned_5'].mean()*100:.1f}%")


if __name__ == "__main__":
    app.run()
