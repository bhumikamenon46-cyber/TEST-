import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Monetary Policy Dashboard", layout="wide")

st.title("📘 Monetary Policy Dashboard – RBI Internship Project")
st.markdown("### A dashboard to study Interest Rates, Liquidity, Inflation and Macro Risks.")

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

    # Higher interest rate increases recession risk
    if interest > 8:
        score += 2
    elif interest > 6:
        score += 1

    # Higher liquidity increases inflation risk
    if liquidity > 5:
        score += 2
    elif liquidity > 2:
        score += 1

    # Higher inflation increases instability
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
# RISK-O-METER GAUGE CHART
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
            {"range": [0, 1], "color": "#C6F6D5"},
            {"range": [1, 2], "color": "#9AE6B4"},
            {"range": [2, 3], "color": "#FAF089"},
            {"range": [3, 4], "color": "#F6AD55"},
            {"range": [4, 5], "color": "#FC8181"},
            {"range": [5, 6], "color": "#E53E3E"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------
# MACRO VARIABLES SECTION
# -----------------------------------------------------------
st.subheader("📉 Monetary Policy Impact Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Interest Rate", f"{interest_rate}%")

with col2:
    st.metric("Liquidity", f"{liquidity} Lakh Cr")

with col3:
    st.metric("Inflation", f"{inflation}%")

# -----------------------------------------------------------
# SIMULATED MONTHLY DATA
# -----------------------------------------------------------
st.subheader("📈 CPI, Inflation & Liquidity – Simulated Trend")

months = pd.date_range("2023-01-01", periods=12, freq="M")
cpi = np.random.uniform(150, 190, 12)
infl = np.random.uniform(4, 8, 12)
liq = np.random.uniform(-2, 6, 12)

df = pd.DataFrame({"Month": months, "CPI": cpi, "Inflation": infl, "Liquidity": liq})

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["Month"], y=df["CPI"], name="CPI"))
fig2.add_trace(go.Scatter(x=df["Month"], y=df["Inflation"], name="Inflation (%)"))
fig2.add_trace(go.Scatter(x=df["Month"], y=df["Liquidity"], name="Liquidity (₹ Lakh Cr)"))

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------------
# EXPLANATION SECTION
# -----------------------------------------------------------
st.subheader("📘 Monetary Policy – Risk Explanation")

st.markdown("""
### 🔺 **1. Risk of Increasing Interest Rate**
- Loans become expensive  
- Investments slow down  
- Growth reduces  
- Stock market impact  

### 🔺 **2. Risk of Increasing Liquidity**
- May lead to inflation  
- Rupee depreciation  
- Asset bubbles  

### 🔺 **3. Risk of High Inflation**
- Reduced purchasing power  
- RBI must tighten policy  
- Business uncertainty  
""")
