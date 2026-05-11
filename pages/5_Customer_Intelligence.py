import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="👥",
    layout="wide"
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("Customer Intelligence Engine")

st.subheader(
    "Enterprise Customer Analytics & Insights"
)

st.markdown("---")

# =====================================================
# DATABASE QUERY
# =====================================================

query = """

SELECT

    f.sales,
    f.profit,

    c.customer_id,
    c.customer_name,
    c.segment,
    c.region,

    d.order_date

FROM fact_sales f

JOIN dim_customer c
ON f.customer_id = c.customer_id

JOIN dim_date d
ON f.date_id = d.date_id

"""

df = pd.read_sql(
    query,
    engine
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = df["customer_id"].nunique()

total_revenue = df["sales"].sum()

customer_ltv = round(

    total_revenue / total_customers,

    2

)

repeat_customers = (

    df.groupby("customer_id")
    .size()
    > 1

).sum()

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Customer KPIs")

k1, k2, k3 = st.columns(3)

with k1:

    st.metric(
        "Total Customers",
        total_customers
    )

with k2:

    st.metric(
        "Customer Lifetime Value",
        f"${customer_ltv:,.2f}"
    )

with k3:

    st.metric(
        "Repeat Customers",
        repeat_customers
    )

st.markdown("##")

# =====================================================
# SEGMENT ANALYSIS
# =====================================================

st.subheader("Customer Segment Analysis")

segment_df = df.groupby(
    "segment"
)["sales"].sum().reset_index()

segment_chart = px.pie(

    segment_df,

    names="segment",

    values="sales",

    hole=0.5
)

segment_chart.update_layout(

    paper_bgcolor="#0F172A",

    font_color="white"
)

st.plotly_chart(
    segment_chart,
    use_container_width=True
)

# =====================================================
# TOP CUSTOMERS
# =====================================================

st.subheader("Top Customers")

top_customers = df.groupby(

    "customer_name"

)["sales"].sum().reset_index()

top_customers = top_customers.sort_values(

    by="sales",

    ascending=False

).head(10)

customer_chart = px.bar(

    top_customers,

    x="customer_name",

    y="sales",

    color="sales"
)

customer_chart.update_layout(

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font_color="white"
)

st.plotly_chart(
    customer_chart,
    use_container_width=True
)

# =====================================================
# AI CUSTOMER INSIGHTS
# =====================================================

st.subheader("AI Customer Insights")

top_segment = segment_df.loc[
    segment_df["sales"].idxmax()
]["segment"]

st.success(f"""

AI Insight:

{top_segment} customers are contributing
the highest share of enterprise revenue.

Customer retention levels indicate
strong repeat purchase behavior.

""")