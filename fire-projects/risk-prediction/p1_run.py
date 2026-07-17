#!/usr/bin/env python3
"""
Project 1: Forest Fire Risk Prediction — standalone runner
Generates all graphs as PNG files. Run with: python3 p1_run.py
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score, RocCurveDisplay
import warnings; warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid", palette="muted")

BASE = Path(__file__).parent
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load & parse ──────────────────────────────────────────────────────
csv = Path("../../daily-datasets/climate/bushfire-history/raw/Fire_For16-21_Attributes.csv")
df = pd.read_csv(csv)
print(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} cols")

def parse_fire(s):
    s = str(s).strip().ljust(5)
    return [1 if i < len(s) and s[i] == 'U' else 0 for i in range(5)]
fire_cols = df['ALL_FIRE'].apply(parse_fire)
for i, col in enumerate(['unplanned_1','unplanned_2','unplanned_3','unplanned_4','unplanned_5'], 1):
    df[col] = fire_cols.apply(lambda x: x[i-1])
df['any_unplanned_prior'] = df[['unplanned_1','unplanned_2','unplanned_3','unplanned_4']].sum(axis=1).clip(0,1)
df['total_burns'] = df['FOR_BURNS'].clip(0,5)

forest = df[df['FOREST'] == 1].copy()
forest = forest[forest['STATE'].notna() & (forest['STATE'].str.strip() != '')]
burns = forest[forest['FOR_BURNS'] >= 0].copy()

print(f"Forest regions: {len(forest):,}, with burn data: {len(burns):,}")
print(f"Unplanned fire rate (2020-21): {burns['unplanned_5'].mean()*100:.1f}%")

# ── 1. State distribution ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Forest Fire Data Overview", fontsize=14, fontweight="bold")
state_counts = forest['STATE'].value_counts()
colors = sns.color_palette("Reds_r", len(state_counts))
axes[0].barh(state_counts.index, state_counts.values, color=colors)
axes[0].set_xlabel("Pixels (thousands)"); axes[0].set_title("Forest Regions by State")
sns.histplot(burns['FOR_BURNS'], bins=6, discrete=True, ax=axes[1], color="#d9534f")
axes[1].set_xlabel("Number of Burns"); axes[1].set_ylabel("Pixel Count")
axes[1].set_title("Fire Frequency Distribution")
tenure_counts = forest['FOR_TEN'].value_counts()
axes[2].pie(tenure_counts.values, labels=tenure_counts.index, autopct="%1.1f%%",
            colors=sns.color_palette("YlOrRd", len(tenure_counts)), startangle=90)
axes[2].set_title("Land Tenure Breakdown")
plt.tight_layout(); fig.savefig(OUT / "01_overview.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 01_overview.png")

# ── 2. Fire rate by state & tenure ────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
state_avg = burns.groupby('STATE')['FOR_BURNS'].mean().sort_values()
_colors = ["#d9534f" if v > 1.5 else "#f0ad4e" if v > 0.5 else "#5cb85c" for v in state_avg.values]
axes[0].barh(state_avg.index, state_avg.values, color=_colors)
axes[0].set_xlabel("Mean Burns (2016-2021)"); axes[0].set_title("Average Fire Frequency by State")
ten_avg = burns.groupby('FOR_TEN')['FOR_BURNS'].mean().sort_values()
_colors2 = ["#d9534f" if v > 2 else "#f0ad4e" if v > 1 else "#5cb85c" for v in ten_avg.values]
axes[1].barh(ten_avg.index, ten_avg.values, color=_colors2)
axes[1].set_xlabel("Mean Burns (2016-2021)"); axes[1].set_title("Average Fire Frequency by Tenure")
plt.tight_layout(); fig.savefig(OUT / "02_fire_rate_bars.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 02_fire_rate_bars.png")

# ── 3. State × Tenure heatmap ─────────────────────────────────────────
heat = burns.groupby(['STATE', 'FOR_TEN'])['unplanned_5'].mean().unstack()
fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(heat, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5,
            cbar_kws={"label": "Unplanned Fire Rate (2020-21)"}, ax=ax)
ax.set_title("Wildfire Risk: State × Tenure Type", fontsize=13, fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "03_heatmap_state_tenure.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 03_heatmap_state_tenure.png")

# ── 4. Boxplots ───────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.boxplot(data=burns, x='FOR_TEN', y='FOR_BURNS', ax=axes[0],
            palette="YlOrRd", order=sorted(burns['FOR_TEN'].unique()))
axes[0].set_title("Burn Count by Tenure", fontweight="bold")
sns.boxplot(data=burns, x='STATE', y='FOR_BURNS', ax=axes[1],
            palette="RdYlGn_r", order=sorted(burns['STATE'].unique()))
axes[1].set_title("Burn Count by State", fontweight="bold")
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout(); fig.savefig(OUT / "04_boxplots.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 04_boxplots.png")

# ── 5. ML: prepare and train ──────────────────────────────────────────
ml = burns.copy()
features = pd.get_dummies(ml[['STATE','FOR_TEN','FOR_CATEGO']], drop_first=False).astype(int)
features['prior_burns'] = ml['FOR_BURNS']
features['any_unplanned_prior'] = ml['any_unplanned_prior']
y = ml['unplanned_5'].values
X = np.nan_to_num(features.values, nan=0.0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train); X_test_s = scaler.transform(X_test)
model = RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_leaf=50,
                               class_weight='balanced', random_state=42, n_jobs=-1)
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s); y_proba = model.predict_proba(X_test_s)[:,1]
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)
imp = pd.DataFrame({'feature': features.columns, 'importance': model.feature_importances_}).sort_values('importance', ascending=False).head(15)
print(f"  Model: ROC-AUC={auc:.4f}, features={features.shape[1]}")

# ── 6. Confusion matrix ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["No Fire","Fire"], yticklabels=["No Fire","Fire"], ax=ax)
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
ax.set_title("Confusion Matrix", fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "05_confusion_matrix.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 05_confusion_matrix.png")

# ── 7. Feature importance ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
_colors3 = ["#d9534f" if i < 3 else "#f0ad4e" if i < 6 else "#5cb85c" for i in range(len(imp))]
sns.barplot(data=imp, y='feature', x='importance', palette=_colors3, ax=ax)
ax.set_xlabel("Importance"); ax.set_ylabel(""); ax.set_title("Top 15 Feature Importances", fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "06_feature_importance.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 06_feature_importance.png")

# ── 8. ROC curve ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax, color="#d9534f", linewidth=2)
ax.plot([0,1],[0,1],'k--', alpha=0.5)
ax.set_title(f"ROC Curve (AUC = {auc:.4f})", fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "07_roc_curve.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 07_roc_curve.png")

# ── 9. Fire rate 2020-21 by state & tenure ────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
rate_state = ml.groupby('STATE')['unplanned_5'].mean().sort_values()
axes[0].bar(rate_state.index, rate_state.values, color=sns.color_palette("Reds", len(rate_state)))
axes[0].set_title("2020-21 Unplanned Fire Rate by State", fontweight="bold")
axes[0].tick_params(axis='x', rotation=45)
rate_ten = ml.groupby('FOR_TEN')['unplanned_5'].mean().sort_values()
axes[1].bar(rate_ten.index, rate_ten.values, color=sns.color_palette("Oranges", len(rate_ten)))
axes[1].set_title("2020-21 Unplanned Fire Rate by Tenure", fontweight="bold")
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout(); fig.savefig(OUT / "08_fire_rate_2021.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 08_fire_rate_2021.png")

# ── 10. Top risk regions ──────────────────────────────────────────────
high_risk = ml[ml['unplanned_5'] == 1]
top = high_risk.groupby(['STATE','FOR_TEN']).size().reset_index(name='count').sort_values('count', ascending=False).head(15)
top['label'] = top['STATE'] + " — " + top['FOR_TEN']
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top, y='label', x='count', palette="Reds_r", ax=ax)
ax.set_xlabel("Number of High-Risk Regions"); ax.set_ylabel("")
ax.set_title("Top 15 Highest-Risk Region-Tenure Combinations", fontweight="bold")
plt.tight_layout(); fig.savefig(OUT / "09_top_risk.png", dpi=150, bbox_inches="tight")
plt.close(); print("  ✓ 09_top_risk.png")

# ── Summary ────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"PROJECT 1 COMPLETE — 10 charts saved to {OUT}")
print(f"{'='*50}")
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print(f"ROC-AUC: {auc:.4f}  |  Accuracy: {accuracy_score(y_test,y_pred):.4f}")
print(f"Recall: {recall_score(y_test,y_pred):.4f}  |  Precision: {precision_score(y_test,y_pred):.4f}")
print(f"F1: {f1_score(y_test,y_pred):.4f}  |  Features: {features.shape[1]}")
print(f"Fire rate: {ml['unplanned_5'].mean()*100:.1f}%  |  Train: {X_train.shape[0]}  Test: {X_test.shape[0]}")
