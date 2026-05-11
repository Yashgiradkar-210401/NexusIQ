import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from database import engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Scenario Simulation",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("Scenario Simulation Engine")

st.subheader(
    "Enterprise Decision Intelligence Simulator"
)

st.markdown("---")

# =====================================================
# DATABASE QUERY
# =====================================================

query = """

SELECT

    SUM(f.sales) AS revenue,

    SUM(f.profit) AS profit

FROM fact_sales f

"""

df = pd.read_sql(
    query,
    engine
)

base_revenue = df["revenue"].iloc[0]

base_profit = df["profit"].iloc[0]

# =====================================================
# SIMULATION CONTROLS
# =====================================================

st.sidebar.subheader("Simulation Controls")

discount_change = st.sidebar.slider(

    "Discount Increase (%)",

    0,

    50,

    10
)

growth_change = st.sidebar.slider(

    "Revenue Growth (%)",

    -20,

    50,

    10
)

cost_increase = st.sidebar.slider(

    "Operational Cost Increase (%)",

    0,

    40,

    5
)

# =====================================================
# SIMULATION CALCULATIONS
# =====================================================

projected_revenue = (

    base_revenue

    *

    (
        1 + (growth_change / 100)
    )

)

discount_impact = (

    projected_revenue

    *

    (
        discount_change / 100
    )

    * 0.15
)

projected_profit = (

    base_profit

    +

    (
        projected_revenue - base_revenue
    )

    -

    discount_impact

)

operational_impact = (

    projected_profit

    *

    (
        cost_increase / 100
    )
)

projected_profit = (

    projected_profit
    -
    operational_impact
)

projected_margin = round(

    (
        projected_profit
        /
        projected_revenue
    ) * 100,

    2

)
# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Simulation Results")

k1, k2, k3 = st.columns(3)

with k1:

    st.metric(

        "Projected Revenue",

        f"${projected_revenue:,.2f}"
    )

with k2:

    st.metric(

        "Projected Profit",

        f"${projected_profit:,.2f}"
    )

with k3:

    st.metric(

        "Projected Margin",

        f"{projected_margin}%"
    )

st.markdown("##")


# =====================================================
# VISUALIZATION
# =====================================================

st.subheader("Scenario Impact Analysis")

fig = go.Figure()

fig.add_trace(

    go.Bar(

        x=[
            "Revenue",
            "Profit"
        ],

        y=[
            projected_revenue,
            projected_profit
        ],

        marker_color=[
            "#0066FF",
            "#00C853"
        ]
    )
)

fig.update_layout(

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font_color="white",

    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# AI RECOMMENDATIONS
# =====================================================

st.subheader("AI Strategic Recommendations")

if projected_margin < 10:

    st.error("""

    AI Alert:

    Profit margin is projected
    to decline significantly.

    Recommendation:
    Reduce aggressive discounting
    and control operational costs.

    """)

elif projected_margin < 20:

    st.warning("""

    AI Insight:

    Moderate profitability detected.

    Recommendation:
    Optimize pricing strategy
    for better margin stability.

    """)

else:

    st.success("""

    AI Insight:

    Business outlook is healthy.

    Current growth assumptions
    indicate strong profitability.

    """)