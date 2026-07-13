"""
Project 4: Interactive Bushfire Analytics Dashboard

A Streamlit dashboard that brings together all three fire projects:
1. ABARES fire risk data explorer
2. Resource allocation planner
3. Sample satellite burn scar viewer

Run with: streamlit run dashboard.py
"""
import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# ─── Conditional imports ────────────────────────────────────────────────────
HAS_STREAMLIT = False
try:
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_STREAMLIT = True
except ImportError:
    st_placeholder = type('st', (), {})()  # no-op stub


# ─── Paths ──────────────────────────────────────────────────────────────────

BASE = Path(__file__).parent
PROJ1 = BASE.parent / "project-1-risk-prediction"
PROJ2 = BASE.parent / "project-2-resource-allocation"
PROJ3 = BASE.parent / "project-3-burn-scar-mapping"


# ─── Data Loaders ───────────────────────────────────────────────────────────

def load_risk_data():
    path = PROJ1 / "processed" / "forest_fire_risk_clean.csv"
    if path.exists():
        df = pd.read_csv(path)
        state_cols = [c for c in df.columns if c.startswith('state_')]
        def get_state(row):
            for col in state_cols:
                if row.get(col, 0) == 1: return col.replace('state_', '')
            return "Unknown"
        df['state_name'] = df.apply(get_state, axis=1)
        return df
    return None


def load_allocation_plan():
    path = PROJ2 / "outputs" / "resource_allocation_plan.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def load_burn_data():
    bm = PROJ3 / "outputs" / "burn_mask.npy"
    nd = PROJ3 / "outputs" / "ndvi_diff.npy"
    if bm.exists() and nd.exists():
        return {'burn_mask': np.load(str(bm)), 'ndvi_diff': np.load(str(nd))}
    return None


# ─── Pages ──────────────────────────────────────────────────────────────────

def page_overview():
    st.title("🔥 Australian Bushfire Analytics")
    st.markdown("""
    A portfolio of data science projects for Australian fire service applications.

    **4 Projects:**
    1. **Forest Fire Risk Prediction** — ML model predicting unplanned fires  
    2. **Resource Allocation Optimisation** — Budget & equipment planning  
    3. **Satellite Burn Scar Mapping** — Sentinel-2 NDVI change detection  
    4. **Interactive Dashboard** — This app

    **Data Source:** ABARES Forest Fire Data (2016–2021)
    """)
    df = load_risk_data()
    if df is not None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Forest Regions", f"{len(df):,}")
        c2.metric("States/Territories", "8")
        c3.metric("Burn Rate (5yr)", f"{df['prior_burns'].mean():.1f} avg")
        c4.metric("Unplanned Fire (2021)", f"{df['unplanned_5'].sum():,} regions")


def page_risk_map():
    st.title("🗺️ Forest Fire Risk Explorer")
    df = load_risk_data()
    if df is None:
        st.warning("Run Project 1 pipeline first.")
        return

    state_cols = [c for c in df.columns if c.startswith('state_') and df[c].dtype in ('int64','int32')]
    tenure_cols = [c for c in df.columns if c.startswith('tenure_') and df[c].dtype in ('int64','int32')]

    rows = []
    for sc in state_cols:
        s = sc.replace('state_', '')
        for tc in tenure_cols:
            t = tc.replace('tenure_', '')
            sub = df[(df[sc] == 1) & (df[tc] == 1)]
            if len(sub):
                rows.append({'State': s, 'Tenure': t, 'Fire Rate': sub['unplanned_5'].mean(),
                             'Prior Burns': sub['prior_burns'].mean(), 'Count': len(sub)})
    agg = pd.DataFrame(rows)

    sel = st.selectbox("Filter state", ['All'] + sorted(agg['State'].unique()))
    if sel != 'All': agg = agg[agg['State'] == sel]

    fig = px.density_heatmap(agg, x='Tenure', y='State', z='Fire Rate',
                             title="Fire Risk Rate by Tenure & State",
                             color_continuous_scale='Reds', range_color=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(agg, x='Tenure', y='Fire Rate', color='State',
                  title="Fire Rate by Tenure Type", barmode='group')
    st.plotly_chart(fig2, use_container_width=True)


def page_resource():
    st.title("💰 Resource Allocation Planner")
    plan = load_allocation_plan()
    if plan is None:
        st.warning("Run Project 2 pipeline first.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted Fires", f"{plan['total_predicted_fires']:,}")
    c2.metric("Total Budget", f"${plan['total_budget_aud']:,}")
    c3.metric("20% Uplift", f"${plan['sensitivity_20pct_uplift']['budget_aud']:,}")

    alloc = pd.DataFrame(plan['allocation'])
    res = alloc['resources'].apply(pd.Series)
    alloc = pd.concat([alloc.drop('resources', axis=1), res], axis=1)

    fig = px.bar(alloc, x='state', y='budget_estimate_aud',
                 title="Budget by State ($AUD)")
    st.plotly_chart(fig, use_container_width=True)

    melt = alloc.melt(id_vars=['state', 'predicted_fires'],
                      value_vars=['appliance_heavy', 'appliance_light', 'crew_member'],
                      var_name='Resource', value_name='Count')
    fig2 = px.bar(melt, x='state', y='Count', color='Resource', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)


def page_burn():
    st.title("🛰️ Burn Scar Viewer")
    data = load_burn_data()
    if data is None:
        st.warning("Run Project 3 pipeline first.")
        return

    c1, c2 = st.columns(2)
    with c1:
        fig = px.imshow(data['ndvi_diff'], color_continuous_scale='RdBu',
                        title="NDVI Difference (Pre − Post)", aspect='auto')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.imshow(data['burn_mask'], color_continuous_scale=['green','red'],
                         title="Burn Scar (Red = Burned)", aspect='auto')
        st.plotly_chart(fig2, use_container_width=True)

    st.metric("Area Burned", f"{data['burn_mask'].mean()*100:.1f}% of scene")


# ─── Main ───────────────────────────────────────────────────────────────────

if not HAS_STREAMLIT:
    print("=" * 60)
    print("PROJECT 4: Interactive Bushfire Analytics Dashboard")
    print("=" * 60)
    print()
    print("Streamlit not installed. To run this dashboard:")
    print("  pip install streamlit plotly pandas numpy")
    print(f"  streamlit run {__file__}")
    print()
    print("--- Dashboard Pages ---")
    print("• Overview — project summary + key metrics")
    print("• Risk Explorer — ABARES fire risk by state & tenure")
    print("• Resource Planner — budget allocation simulator")
    print("• Burn Scar Viewer — NDVI change detection viewer")
    print()
    print("--- Data Sources ---")
    print("Uses outputs from Projects 1-3 pipelines.")
    for label, fn in [('Project 1 risk data', load_risk_data()),
                       ('Project 2 allocation', load_allocation_plan()),
                       ('Project 3 burn data', load_burn_data())]:
        print(f"  {label}: {'✅ FOUND' if fn is not None else '❌ NOT FOUND'}")
    print()
    print("=" * 60)
else:
    st.set_page_config(page_title="Australian Bushfire Analytics", page_icon="🔥", layout="wide")
    pages = {"Overview": page_overview, "Risk Explorer": page_risk_map,
             "Resource Planner": page_resource, "Burn Scar Viewer": page_burn}
    with st.sidebar:
        st.title("🔥 Bushfire Analytics")
        st.markdown("---")
        page = st.radio("Navigation", list(pages.keys()))
        st.caption("Built for Australian Fire Service applications")
    pages[page]()
