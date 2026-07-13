#!/usr/bin/env python3
"""
Project 1: Forest Fire Risk Prediction — ABARES Forest Fire Data (2016-2021)

Predict whether a forest region will experience an unplanned fire in the 2020-21
season based on tenure type, forest category, state, and prior fire history.

Target: unplanned_fire_2021 (binary) — 1 if an unplanned fire occurred, 0 otherwise.
Features: tenure type, forest type, state, prior fire count, prior planned burns.

Source: ABARES (agriculture.gov.au/abares/forestsaustralia)
"""
import pandas as pd
import numpy as np
import json
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

# ─── CONFIG ─────────────────────────────────────────────────────────────────
RAW_FILE = "Fire_For16-21_Attributes.csv"  # Symlinked/copied from bushfire-history
TARGET_COL = "unplanned_fire_2021"
RANDOM_STATE = 42
TEST_SIZE = 0.2
# ────────────────────────────────────────────────────────────────────────────


def load_data():
    """Load the ABARES forest fire attribute table."""
    csv_path = RAW / RAW_FILE
    if not csv_path.exists():
        # Try symlink source
        alt = Path("/home/abdodameen/australian-ml-datasets/daily-datasets/climate/bushfire-history/raw") / RAW_FILE
        if alt.exists():
            csv_path = alt
        else:
            raise FileNotFoundError(f"Can't find {RAW_FILE} anywhere")
    
    print(f"Loading {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def run_eda(df):
    """Burn analysis summary."""
    print(f"\n=== EDA ===")
    print(f"Shape: {df.shape}")
    total_area = df['COUNT'].sum()
    forest_area = df[df['FOREST'] == 1]['COUNT'].sum()
    print(f"Total pixels: {total_area:,}")
    print(f"Forest pixels: {forest_area:,} ({forest_area/total_area*100:.1f}%)")
    
    burnt = df[df['FOR_BURNS'] >= 0]
    print(f"\nBurn count distribution:")
    for b in sorted(burnt['FOR_BURNS'].unique()):
        count = (burnt['FOR_BURNS'] == b).sum()
        pct = count / len(burnt) * 100
        print(f"  {b} burns: {count} pixels ({pct:.1f}%)")
    
    print(f"\nBy state (mean burns):")
    for state, grp in df[df['FOR_BURNS'] >= 0].groupby('STATE'):
        if state.strip():
            print(f"  {state}: {grp['FOR_BURNS'].mean():.2f} avg burns ({len(grp)} pixels)")


def decode_fire_patterns(df):
    """
    Decode the ALL_FIRE field into structured columns.
    ALL_FIRE is a fixed-width string where each position = one fire season:
    Position 0 (offset): padding spaces
    Position 1: FIRE_1617
    Position 2: FIRE_1718  
    Position 3: FIRE_1819
    Position 4: FIRE_1920
    Position 5: FIRE_2021
    
    Values: ' ' = no fire, 'P' = planned burn, 'U' = unplanned fire
    """
    df = df.copy()
    
    # Parse the ALL_FIRE pattern
    def parse_fire_pattern(s):
        """Extract fire pattern from padded string."""
        s = str(s).strip()
        # Pad to 5 chars representing 5 fire seasons
        while len(s) < 5:
            s = s + ' '
        s = s[-5:]  # Take last 5 chars
        return [
            1 if len(s) > i and s[i] == 'U' else 0 for i in range(5)
        ] + [
            1 if len(s) > i and s[i] == 'P' else 0 for i in range(5)
        ]
    
    fire_cols = df['ALL_FIRE'].apply(parse_fire_pattern)
    fire_df = pd.DataFrame(fire_cols.tolist(), 
                          columns=[f'unplanned_{y}' for y in range(1,6)] + 
                                  [f'planned_{y}' for y in range(1,6)])
    df = pd.concat([df, fire_df], axis=1)
    
    print(f"Decoded fire patterns for {len(df)} rows")
    print(f"  Unplanned fire in most recent season (5): {df['unplanned_5'].sum()} pixels ({df['unplanned_5'].mean()*100:.1f}%)")
    return df


def engineer_features(df):
    """Create feature set for ML."""
    df = df.copy()
    print(f"\n=== Feature Engineering ===")
    
    # Drop rows that aren't forest (FOREST == 0) — we only care about forest fire risk
    # and rows with no state
    before = len(df)
    df = df[df['FOREST'] == 1].copy()
    df = df[df['STATE'].notna() & (df['STATE'].str.strip() != '')].copy()
    print(f"Dropped {before - len(df)} non-forest / no-state rows (kept {len(df)})")
    
    # Drop rows with no fire data (FOR_BURNS == -9 means non-forest area)
    before = len(df)
    df = df[df['FOR_BURNS'] >= 0].copy()
    print(f"Dropped {before - len(df)} non-burn-area rows (kept {len(df)})")
    
    # --- Features ---
    
    # 1. One-hot encode FOR_TEN (tenure type)
    ten_dummies = pd.get_dummies(df['FOR_TEN'], prefix='tenure')
    ten_dummies = ten_dummies.astype(int)
    df = pd.concat([df, ten_dummies], axis=1)
    print(f"One-hot encoded FOR_TEN → {len(ten_dummies.columns)} columns")
    
    # 2. One-hot encode FOR_CATEGO (forest category)
    cat_dummies = pd.get_dummies(df['FOR_CATEGO'], prefix='forest_cat')
    cat_dummies = cat_dummies.astype(int)
    df = pd.concat([df, cat_dummies], axis=1)
    print(f"One-hot encoded FOR_CATEGO → {len(cat_dummies.columns)} columns")
    
    # 3. One-hot encode STATE
    state_dummies = pd.get_dummies(df['STATE'], prefix='state')
    state_dummies = state_dummies.astype(int)
    df = pd.concat([df, state_dummies], axis=1)
    print(f"One-hot encoded STATE → {len(state_dummies.columns)} columns")
    
    # 4. Prior fire features
    df['prior_burns'] = df['FOR_BURNS']
    df['prior_unplanned'] = df[[f'unplanned_{i}' for i in range(1,5)]].sum(axis=1)  # years 1-4
    df['prior_planned'] = df[[f'planned_{i}' for i in range(1,5)]].sum(axis=1)
    df['any_prior_unplanned'] = (df['prior_unplanned'] > 0).astype(int)
    df['any_prior_planned'] = (df['prior_planned'] > 0).astype(int)
    print(f"Created prior fire history features")
    
    # 5. Interaction: tenure x prior unplanned fire
    df['priv_x_prior_fire'] = df.get('tenure_PRIV', 0) * df['prior_unplanned']
    df['lease_x_prior_fire'] = df.get('tenure_LEASE', 0) * df['prior_unplanned']
    df['ncr_x_prior_fire'] = df.get('tenure_NCR', 0) * df['prior_unplanned']
    print(f"Created tenure x prior fire interactions")
    
    print(f"\nFinal feature set: {len(df.columns)} columns, {len(df)} rows")
    return df


def prepare_ml(df):
    """Prepare ML-ready data."""
    print(f"\n=== ML Preparation ===")
    
    # Target: unplanned fire in the most recent season (2020-21)
    df[TARGET_COL] = df['unplanned_5']
    print(f"Target distribution:\n  No fire: {(df[TARGET_COL] == 0).sum()} ({100 - df[TARGET_COL].mean()*100:.1f}%)\n  Fire: {(df[TARGET_COL] == 1).sum()} ({df[TARGET_COL].mean()*100:.1f}%)")
    
    # Feature columns (all numeric)
    feature_cols = [c for c in df.columns if c.startswith((
        'tenure_', 'forest_cat_', 'state_', 'prior_', 'any_', 
        'priv_', 'lease_', 'ncr_'))
    ]
    
    print(f"Feature columns ({len(feature_cols)}): {feature_cols}")
    
    X = df[feature_cols].values
    y = df[TARGET_COL].values
    
    # Handle any NaN/Inf
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save
    PROCESSED.mkdir(parents=True, exist_ok=True)
    FEATURES.mkdir(parents=True, exist_ok=True)
    
    clean_path = PROCESSED / "forest_fire_risk_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"Saved cleaned data: {clean_path}")
    
    np.savetxt(FEATURES / "X_train_scaled.csv", X_train_scaled, delimiter=",")
    np.savetxt(FEATURES / "X_test_scaled.csv", X_test_scaled, delimiter=",")
    np.savetxt(FEATURES / "y_train.csv", y_train, delimiter=",", fmt="%d")
    np.savetxt(FEATURES / "y_test.csv", y_test, delimiter=",", fmt="%d")
    with open(FEATURES / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("Saved ML-ready files to features/")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_cols


def train_and_evaluate(X_train, X_test, y_train, y_test, feature_cols):
    """Train a Random Forest and evaluate."""
    print(f"\n=== Training ===")
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=50,
        class_weight='balanced',
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                               target_names=['No Fire', 'Unplanned Fire']))
    
    auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC: {auc:.4f}")
    
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"              Pred No Fire  Pred Fire")
    print(f"Actual No Fire   {cm[0,0]:6d}      {cm[0,1]:5d}")
    print(f"Actual Fire      {cm[1,0]:6d}      {cm[1,1]:5d}")
    
    # Feature importance
    importances = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 Feature Importances:")
    for i, row in importances.head(10).iterrows():
        print(f"  {row['feature']:35s} {row['importance']:.4f}")
    
    # Save model
    with open(FEATURES / "random_forest_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    # Save results
    results = {
        "model": "RandomForestClassifier",
        "n_estimators": 200,
        "max_depth": 12,
        "roc_auc": float(auc),
        "accuracy": float(model.score(X_test, y_test)),
        "feature_count": len(feature_cols),
        "top_features": importances.head(10).to_dict('records')
    }
    with open(PROCESSED / "model_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return model


def generate_metadata(df):
    metadata = {
        "project": "Forest Fire Risk Prediction",
        "source": "ABARES Forest Fire Data 2016-2021",
        "source_url": "https://www.agriculture.gov.au/abares/forestsaustralia/forest-data-maps-and-tools/spatial-data/forest-fire",
        "created_date": str(datetime.now()),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "target_column": TARGET_COL,
        "ml_task": "Binary classification — predict unplanned forest fire in 2020-21 season",
        "features": [
            "Tenure type (PRIV, LEASE, NCR, OCL, MUF, ND) — one-hot encoded",
            "Forest category (Native forest, Non-forest, Plantation) — one-hot encoded",
            "State/territory — one-hot encoded",
            "Prior burn count (1-5 years)",
            "Prior unplanned fire count (years 1-4)",
            "Prior planned burn count (years 1-4)",
            "Tenure × prior fire interactions"
        ],
        "transformations": [
            "Decoded ALL_FIRE pattern into per-year unplanned/planned indicators",
            "Dropped non-forest and non-burn-area rows",
            "One-hot encoded categorical features",
            "StandardScaler normalization",
            "80/20 stratified train/test split"
        ],
        "class_balance": {
            "no_fire_pct": round(100 - df[TARGET_COL].mean() * 100, 1),
            "fire_pct": round(df[TARGET_COL].mean() * 100, 1)
        }
    }
    meta_path = BASE / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata: {meta_path}")


def main():
    print("=" * 60)
    print("PROJECT 1: Forest Fire Risk Prediction")
    print("=" * 60)
    
    df = load_data()
    run_eda(df)
    df = decode_fire_patterns(df)
    df = engineer_features(df)
    X_train, X_test, y_train, y_test, feature_cols = prepare_ml(df)
    model = train_and_evaluate(X_train, X_test, y_train, y_test, feature_cols)
    generate_metadata(df)
    
    print(f"\n{'='*60}")
    print("PROJECT 1 COMPLETE — see processed/ and features/ for outputs")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
