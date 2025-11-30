import streamlit as st
import pandas as pd
import numpy as np
from utils.charts import line_chart
import plotly.graph_objects as go

# -----------------------------------------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="RBI Monetary Policy Dashboard", layout="wide")

st.title("📊 RBI Monetary Policy Dashboard + Riskometer")
st.write("Simulate how changes in interest rate, liquidity and inflation affect the economy.")

# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/sample_data.csv", parse_dates=["date"])

df = load_data()

# -----------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------
st.sidebar.header("Monetary Policy Options")

scenario = st.sidebar.selectbox(
    "Select Policy Action",
    [
        "Baseline (No Change)",
        "Increase Interest Rate (+1%)",
        "Increase Liquidity",
        "Increase Inflation (+2%)"
    ]
)

horizon = st.sidebar.slider("Shock Horizon (quarters)", 1, 8, 4)

data = df.copy()

# -----------------------------------------------------------
# APPLY POLICY SHOCK
# -----------------------------------------------------------
if scenario == "Increase Interest Rate (+1%)":
    data["policy_rate"] += 1
    data["gdp_growth"] -= 0.6 * (horizon / 4)
    data["inflation"] -= 0.4 * (horizon / 4)
    data["unemployment"] += 0.2 * (horizon / 4)

elif scenario == "Increase Liquidity":
    data["liquidity_gap"] += 1
    data["inflation"] += 0.6 * (horizon / 4)
    data["gdp_growth"] += 0.5 * (horizon / 4)

elif scenario == "Increase Inflation (+2%)":
    data["inflation"] += 2
    data["gdp_growth"] -= 0.4 * (horizon / 4)
    data["unemployment"] += 0.3 * (horizon / 4)

# -----------------------------------------------------------
# RISKOMETER MODEL
# -----------------------------------------------------------
def risk_interest(rate):
    return np
