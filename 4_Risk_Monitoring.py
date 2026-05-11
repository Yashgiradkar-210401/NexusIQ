import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from styles import load_css

load_css()

engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/nexusiq"
)

st.title("Risk Monitoring")

query = """
SELECT
    c.region,
    SUM(f.sales) AS sales,
    SUM(f.profit) AS profit,
    AVG(f.discount) AS discount
FROM fact_sales f
JOIN dim_customer c
ON f.customer_id = c.customer_id
GROUP BY c.region;
"""

df = pd.read_sql(query, engine)

df['margin'] = round(
    (df['profit'] / df['sales']) * 100,
    2
)

lowest_region = df.loc[
    df['margin'].idxmin()
]

st.subheader("Revenue Leakage Detection")

st.warning(
    f"""
    ALERT:
    {lowest_region['region']}
    has lowest margin:
    {lowest_region['margin']}%
    """
)

st.bar_chart(
    df.set_index('region')['margin']
)

# BUSINESS RISK

risk_score = 0

if df['margin'].mean() < 10:
    risk_score += 40

if df['discount'].mean() > 0.2:
    risk_score += 30

if risk_score < 30:
    risk_status = "Low Risk"

elif risk_score < 60:
    risk_status = "Moderate Risk"

else:
    risk_status = "High Risk"

st.subheader("Business Risk Score")

st.metric(
    "Risk Status",
    risk_status
)