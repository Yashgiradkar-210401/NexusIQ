import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from styles import load_css

load_css()

# =========================================================
# POSTGRESQL CONNECTION
# =========================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/nexusiq"
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("Executive Dashboard")

st.subheader(
    "Enterprise Decision Intelligence"
)

# =========================================================
# MAIN DATA QUERY
# =========================================================

base_query = """
SELECT
    f.sales,
    f.profit,

    c.region,

    p.category,

    d.year,
    d.month

FROM fact_sales f

JOIN dim_customer c
ON f.customer_id = c.customer_id

JOIN dim_product p
ON f.product_id = p.product_id

JOIN dim_date d
ON f.date_id = d.date_id
"""

df = pd.read_sql(base_query, engine)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

regions = sorted(df['region'].unique())

categories = sorted(df['category'].unique())

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df['region'] == selected_region
    ]

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df['category'] == selected_category
    ]

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered_df['sales'].sum()

total_profit = filtered_df['profit'].sum()

total_orders = len(filtered_df)

profit_margin = round(
    (total_profit / total_revenue) * 100,
    2
)

# =========================================================
# KPI CARDS
# =========================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Profit Margin %",
    f"{profit_margin}%"
)

col4.metric(
    "Total Orders",
    total_orders
)

# =========================================================
# REVENUE TREND ANALYSIS
# =========================================================

st.markdown("---")

st.subheader("Revenue Trend Analysis")

revenue_trend = filtered_df.groupby(
    ['year', 'month']
)['sales'].sum().reset_index()

revenue_trend['month_label'] = (
    revenue_trend['year'].astype(str)
    + "-"
    +
    revenue_trend['month'].astype(str)
)

st.line_chart(
    revenue_trend.set_index(
        'month_label'
    )['sales']
)

# =========================================================
# REGION REVENUE ANALYSIS
# =========================================================

st.markdown("---")

st.subheader("Region Wise Revenue")

region_revenue = filtered_df.groupby(
    'region'
)['sales'].sum()

st.bar_chart(region_revenue)

# =========================================================
# CATEGORY PROFITABILITY
# =========================================================

st.markdown("---")

st.subheader("Category Profitability")

category_profit = filtered_df.groupby(
    'category'
)['profit'].sum()

st.bar_chart(category_profit)

# =========================================================
# EXECUTIVE INSIGHTS
# =========================================================

st.markdown("---")

st.subheader("Executive Insights")

top_region = region_revenue.idxmax()

top_category = category_profit.idxmax()

st.info(
    f"""
    • {top_region} region is generating highest revenue.

    • {top_category} category is most profitable.

    • Current profit margin is {profit_margin}%.
    """
)