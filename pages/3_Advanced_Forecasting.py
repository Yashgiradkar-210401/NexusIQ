import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA

from database import engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Advanced Forecasting",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #020817 0%,
        #071224 50%,
        #0F172A 100%
    );
    color:white;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.stDeployButton{
    display:none;
}

[data-testid="metric-container"]{
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("Advanced Forecasting Engine")

st.subheader(
    "AI-Powered Enterprise Revenue Forecasting"
)

st.markdown("---")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.subheader("Forecast Controls")

forecast_days = st.sidebar.slider(

    "Forecast Horizon (Days)",

    30,

    365,

    90
)

model_type = st.sidebar.selectbox(

    "Forecast Model",

    [
        "Prophet",
        "ARIMA"
    ]
)

# =====================================================
# DATABASE QUERY
# =====================================================

query = """

SELECT

    d.order_date,
    SUM(f.sales) AS revenue

FROM fact_sales f

JOIN dim_date d
ON f.date_id = d.date_id

GROUP BY d.order_date

ORDER BY d.order_date

"""

df = pd.read_sql(
    query,
    engine
)

# =====================================================
# DATA PREPARATION
# =====================================================

df.columns = [
    "ds",
    "y"
]

df["ds"] = pd.to_datetime(
    df["ds"]
)

# =====================================================
# PROPHET MODEL
# =====================================================

if model_type == "Prophet":

    model = Prophet(

        yearly_seasonality=True,

        weekly_seasonality=True,

        daily_seasonality=False
    )

    model.fit(df)

    future = model.make_future_dataframe(
        periods=forecast_days
    )

    forecast = model.predict(future)

    actual_x = df["ds"]
    actual_y = df["y"]

    forecast_x = forecast["ds"]
    forecast_y = forecast["yhat"]

    upper_band = forecast["yhat_upper"]
    lower_band = forecast["yhat_lower"]

# =====================================================
# ARIMA MODEL
# =====================================================

else:

    arima_model = ARIMA(

        df["y"],

        order=(5,1,0)
    )

    arima_fit = arima_model.fit()

    predictions = arima_fit.forecast(
        steps=forecast_days
    )

    future_dates = pd.date_range(

        start=df["ds"].max(),

        periods=forecast_days + 1,

        freq="D"
    )[1:]

    forecast = pd.DataFrame({

        "ds": future_dates,

        "yhat": predictions
    })

    actual_x = df["ds"]
    actual_y = df["y"]

    forecast_x = forecast["ds"]
    forecast_y = forecast["yhat"]

# =====================================================
# KPI METRICS
# =====================================================

latest_actual = round(
    actual_y.iloc[-1],
    2
)

latest_forecast = round(
    forecast_y.iloc[-1],
    2
)

forecast_growth = round(

    (
        (
            latest_forecast
            -
            latest_actual
        )
        /
        latest_actual
    ) * 100,

    2

) if latest_actual > 0 else 0

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Forecast KPIs")

k1, k2, k3 = st.columns(3)

with k1:

    st.metric(

        "Latest Revenue",

        f"${latest_actual:,.2f}"
    )

with k2:

    st.metric(

        "Forecast Revenue",

        f"${latest_forecast:,.2f}"
    )

with k3:

    st.metric(

        "Forecast Growth",

        f"{forecast_growth}%"
    )

st.markdown("##")

# =====================================================
# FORECAST CHART
# =====================================================

st.subheader("Revenue Forecast Analysis")

fig = go.Figure()

# =====================================================
# ACTUAL REVENUE
# =====================================================

fig.add_trace(

    go.Scatter(

        x=actual_x,

        y=actual_y,

        mode="lines",

        name="Actual Revenue",

        line=dict(

            color="#7DD3FC",

            width=3
        )
    )
)

# =====================================================
# FORECAST LINE
# =====================================================

fig.add_trace(

    go.Scatter(

        x=forecast_x,

        y=forecast_y,

        mode="lines",

        name="Forecast Revenue",

        line=dict(

            color="#0066FF",

            width=3,

            dash="dash"
        )
    )
)

# =====================================================
# CONFIDENCE INTERVAL
# =====================================================

if model_type == "Prophet":

    fig.add_trace(

        go.Scatter(

            x=forecast_x,

            y=upper_band,

            mode="lines",

            line=dict(width=0),

            showlegend=False
        )
    )

    fig.add_trace(

        go.Scatter(

            x=forecast_x,

            y=lower_band,

            mode="lines",

            fill='tonexty',

            fillcolor='rgba(255,0,0,0.12)',

            line=dict(width=0),

            name="Confidence Interval"
        )
    )

# =====================================================
# CHART LAYOUT
# =====================================================

fig.update_layout(

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font_color="white",

    height=650,

    xaxis_title="Date",

    yaxis_title="Revenue",

    legend=dict(

        orientation="h",

        yanchor="bottom",

        y=1.02,

        xanchor="right",

        x=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FORECAST DATA TABLE
# =====================================================

st.subheader("Forecast Output")

if model_type == "Prophet":

    forecast_table = forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ].tail(30)

else:

    forecast_table = forecast[
        [
            "ds",
            "yhat"
        ]
    ].tail(30)

forecast_table.columns = [

    "Date",

    "Forecast Revenue",

    *(
        ["Lower Confidence", "Upper Confidence"]
        if model_type == "Prophet"
        else []
    )
]

st.dataframe(
    forecast_table,
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("AI Forecast Insights")

if forecast_growth > 0:

    st.success(f"""

    AI Insight:

    Revenue is expected to increase by
    {forecast_growth}%

    over the selected forecast horizon
    based on historical enterprise
    sales trends and seasonality.

    """)

else:

    st.warning(f"""

    AI Risk Alert:

    Revenue is projected to decline by
    {abs(forecast_growth)}%

    over the selected forecast period.

    Recommended:
    Review pricing strategy and
    category profitability.

    """)

# =====================================================
# MODEL INFORMATION
# =====================================================

st.subheader("Forecast Model Information")

if model_type == "Prophet":

    st.info("""

    Prophet Forecasting Model

    • Handles seasonality automatically

    • Supports trend analysis

    • Provides confidence intervals

    • Excellent for enterprise forecasting

    """)

else:

    st.info("""

    ARIMA Forecasting Model

    • Statistical time-series forecasting

    • Strong for historical pattern analysis

    • Widely used in financial forecasting

    • Enterprise-grade predictive modeling

    """)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Powered by NexusIQ AI Forecasting Engine"
)