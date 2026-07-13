#!/usr/bin/env python3
"""
Project 2: Fire Resource Allocation Optimisation

Predicts seasonal fire resource demand (appliances, crews, equipment) based on
ABARES fire history and tenure/forest characteristics. Includes a cost-optimised
allocation model that distributes resources across states proportional to risk.

Designed for procurement and operational planning contexts — shows how data
science drives fire service budgeting decisions.
"""
import pandas as pd
import numpy as np
import json
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

warnings.filterwarnings('ignore')

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "models"
OUTPUTS_DIR = BASE / "outputs"

RANDOM_STATE = 42

# ─── Resource cost assumptions (AUD, illustrative) ──────────────────────────
RESOURCE_COSTS = {
    "appliance_heavy": 2500000,   # Heavy tanker appliance
    "appliance_light": 800000,    # Light unit / patrol
    "crew_member": 120000,        # Annual salary per firefighter
    "helicopter": 5000000,        # Helitac deployment per season
    "bulldozer": 350000,          # Per season hire
    "aerial_tanker": 8000000      # Large air tanker per season
}

# Resource requirements per predicted fire (illustrative)
RESOURCES_PER_FIRE = {
    "appliance_heavy": 0.3,       # 1 heavy appliance per ~3 fires
    "appliance_light": 0.8,       # 1 light unit per ~1.25 fires
    "crew_member": 4.0,           # 4 crew per fire
    "helicopter": 0.05,           # 1 heli per ~20 fires (large fires)
}


def load_fire_data():
    """Load ABARES data aggregated by state + tenure."""
    csv_path = BASE.parent / "project-1-risk-prediction" / "processed" / "forest_fire_risk_clean.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Run project-1 first: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from Project 1 output")
    return df


def build_state_forecast(df):
    """Build a model that forecasts fire incidents by state and tenure."""
    print(f"\n=== Building Resource Demand Forecast Model ===")
    
    # Aggregate: predict number of unplanned fires per state per tenure per prior burn level
    agg = df.groupby(['state_Qld', 'state_NSW', 'state_NT', 'state_WA', 'state_Vic', 
                      'state_SA', 'state_Tas', 'state_ACT',
                      'tenure_PRIV', 'tenure_LEASE', 'tenure_NCR', 'tenure_OCL',
                      'tenure_MUF', 'tenure_ND',
                      'prior_burns']).agg(
        pixel_count=('unplanned_5', 'count'),
        fires=('unplanned_5', 'sum')
    ).reset_index()
    
    # Fire rate per group
    agg['fire_rate'] = agg['fires'] / agg['pixel_count']
    
    print(f"Aggregated into {len(agg)} region-tenure groups")
    print(f"Total fires across all groups: {agg['fires'].sum()}")
    
    # Build regression model to predict fire count
    feature_cols = [c for c in agg.columns if c not in ['fires', 'fire_rate', 'pixel_count']]
    X = agg[feature_cols].values
    y = agg['fires'].values
    
    # Handle any NaN
    X = np.nan_to_num(X, nan=0.0)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    model = GradientBoostingRegressor(
        n_estimators=150, max_depth=4, min_samples_leaf=20,
        random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\nForecast Model Performance:")
    print(f"  R²: {r2:.4f}")
    print(f"  MAE: {mae:.2f} fires per group")
    
    # Save model
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODELS_DIR / "demand_forecast_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    # Save aggregated data
    agg.to_csv(DATA_DIR / "state_tenure_aggregated.csv", index=False)
    
    return model, agg, feature_cols


def allocate_resources(agg, model, feature_cols):
    """Allocate resources across states based on predicted fire demand."""
    print(f"\n{'='*60}")
    print("RESOURCE ALLOCATION OPTIMISATION")
    print(f"{'='*60}")
    
    # Predict fires for each group
    X_all = agg[feature_cols].values
    X_all = np.nan_to_num(X_all, nan=0.0)
    agg['predicted_fires'] = model.predict(X_all)
    
    # Aggregate predictions by state
    state_cols = [c for c in feature_cols if c.startswith('state_')]
    
    state_results = []
    for state_col in state_cols:
        state_name = state_col.replace('state_', '')
        state_data = agg[agg[state_col] == 1]
        
        if len(state_data) == 0:
            continue
            
        total_predicted = max(0, state_data['predicted_fires'].sum())
        pixel_count = state_data['pixel_count'].sum()
        
        # Calculate resource requirements
        resources = {}
        for resource, per_fire in RESOURCES_PER_FIRE.items():
            resources[resource] = int(np.ceil(total_predicted * per_fire))
        
        # Calculate cost
        total_cost = sum(
            resources[r] * RESOURCE_COSTS[r] 
            for r in resources if r in RESOURCE_COSTS
        )
        
        state_results.append({
            'state': state_name,
            'predicted_fires': int(total_predicted),
            'pixel_count': int(pixel_count),
            'risk_density': round(total_predicted / pixel_count, 4) if pixel_count > 0 else 0,
            'resources': resources,
            'budget_estimate_aud': int(total_cost)
        })
    
    # Sort by predicted fires descending
    state_results.sort(key=lambda x: x['predicted_fires'], reverse=True)
    
    total_budget = sum(s['budget_estimate_aud'] for s in state_results)
    total_fires = sum(s['predicted_fires'] for s in state_results)
    
    print(f"\nTotal predicted fires (next season): {total_fires:,}")
    print(f"Total estimated budget: ${total_budget:,}")
    print()
    
    print(f"{'State':10s} {'Fires':>8s} {'Heavy':>6s} {'Light':>6s} {'Crews':>6s} {'Budget':>14s}")
    print("-" * 60)
    for s in state_results:
        r = s['resources']
        budget_str = f"${s['budget_estimate_aud']:>10,}"
        print(f"{s['state']:10s} {s['predicted_fires']:>8d} {r['appliance_heavy']:>6d} {r['appliance_light']:>6d} {r['crew_member']:>6d} {budget_str}")
    
    print("-" * 60)
    total_budget_str = f"${total_budget:>10,}"
    print(f"{'TOTAL':10s} {total_fires:>8d} {'':>6s} {'':>6s} {'':>6s} {total_budget_str}")
    
    # Sensitivity: what if fire season is 20% worse?
    print(f"\n--- Sensitivity Analysis ---")
    print(f"Scenario: 20% worse fire season (+20% predicted fires)")
    uplifted_budget = int(total_budget * 1.2)
    uplifted_fires = int(total_fires * 1.2)
    print(f"  Predicted fires: {total_fires:,} → {uplifted_fires:,}")
    print(f"  Budget needed: ${total_budget:,} → ${uplifted_budget:,}")
    print(f"  Additional budget: ${uplifted_budget - total_budget:,}")
    
    # Top 3 tenure types by fire risk
    print(f"\n--- Fire Risk by Tenure Type ---")
    tenure_cols = [c for c in feature_cols if c.startswith('tenure_')]
    for tc in tenure_cols:
        ten_data = agg[agg[tc] == 1]
        if len(ten_data) > 0:
            rate = ten_data['fires'].sum() / ten_data['pixel_count'].sum()
            name = tc.replace('tenure_', '')
            print(f"  {name:15s}: {rate:.4f} fire rate per pixel")
    
    # Save allocation plan
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    allocation_plan = {
        "season": "2021-22 (forecast from 2016-21 data)",
        "total_predicted_fires": total_fires,
        "total_budget_aud": total_budget,
        "allocation": state_results,
        "sensitivity_20pct_uplift": {
            "fires": uplifted_fires,
            "budget_aud": uplifted_budget,
            "additional_budget_aud": uplifted_budget - total_budget
        }
    }
    
    with open(OUTPUTS_DIR / "resource_allocation_plan.json", "w") as f:
        json.dump(allocation_plan, f, indent=2)
    
    print(f"\nSaved allocation plan to outputs/resource_allocation_plan.json")
    
    return allocation_plan


def generate_metadata():
    metadata = {
        "project": "Fire Resource Allocation Optimisation",
        "data_source": "ABARES Forest Fire Data 2016-2021 (via Project 1 output)",
        "created_date": str(datetime.now()),
        "model": "GradientBoostingRegressor per-region fire count forecast",
        "ml_task": "Regression — forecast fire incident counts by state/tenure group",
        "resource_costs": RESOURCE_COSTS,
        "resource_rates": RESOURCES_PER_FIRE,
        "features": [
            "State indicators (8 states/territories)",
            "Tenure type indicators (6 types)",
            "Prior burn count (0-5 historical years)",
            "Pixel count (area weight)"
        ],
        "outputs": [
            "models/demand_forecast_model.pkl — trained regressor",
            "data/state_tenure_aggregated.csv — aggregated fire rates",
            "outputs/resource_allocation_plan.json — planned allocation by state"
        ]
    }
    
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata")


def main():
    print("=" * 60)
    print("PROJECT 2: Fire Resource Allocation Optimisation")
    print("=" * 60)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    df = load_fire_data()
    model, agg, feature_cols = build_state_forecast(df)
    allocation = allocate_resources(agg, model, feature_cols)
    generate_metadata()
    
    print(f"\n{'='*60}")
    print("PROJECT 2 COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
