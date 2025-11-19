import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Monetary Policy Dashboard", layout="wide")

st.title("📘 Monetary Policy Dashboard – RBI Internship Project")
st.markdown("### A complete dashboard to study Interest Rates, Liquidity, Inflation and Macro Risks.")

# -----------------------------------------------------------
# SIDEBAR – USER CONTROLS
# -----------------------------------------------------------
st.sidebar.header("🔧 Adjust Monetary Policy Variables")

interest_rate = st.sidebar.slider("Repo Rate (%)", 2.0, 12.0, 6.5)
liquidity = st.sidebar.slider("Liquidity (₹ lakh crore)", -10.0, 10.0, 2.0)
inflation = st.sidebar.slider("Inflation (%)", 0.0, 15.0, 5.2)

st.sidebar.write("---")

st.sidebar.markdown("### Created by: **Bhumika Menon**")

# -----------------------------------------------------------
# RISK-O-METER FUNCTION
# -----------------------------------------------------------
def risk_level(interest, liquidity, inflation):
    score = 0

    # HIGHER INTEREST RATE → slows growth
    if interest > 8:
        score += 2
    elif interest > 6:
        score += 1

    # HIGH LIQUIDITY → risk of inflation
    if liquidity > 5:
        score += 2
    elif liquidity > 2:
        score += 1

    # HIGH INFLATION → economic instability
    if inflation > 8:
        score += 3
    elif inflation > 5:
        score += 2
    else:
        score += 1

    return min(score, 6)

risk = risk_level(interest_rate, liquidity, inflation)

risk_labels = ["Very Low", "Low", "Moderate", "High", "Very High", "Extreme"]
risk_text = risk_labels[risk - 1]

# -----------------------------------------------------------
# RISK-O-METER GRAPH
# -----------------------------------------------------------
st.subheader("📊 Monetary Policy Risk-O-Meter")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk,
    title={"text": f"Risk Level: {risk_text}"},
    gauge={
        "axis": {"range": [0, 6]},
        "bar": {"color": "black"},
        "steps": [
            {"range": [0, 1], "col
