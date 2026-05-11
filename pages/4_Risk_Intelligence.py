import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Risk Intelligence",
    page_icon="⚠️",
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
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("Risk Intelligence Engine")

st.subheader(
    "Enterprise Business Risk Monitoring"
)

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.subheader("Risk Controls")

selected_region = st.sidebar.selectbox(

    "Region",

    [
        "All",
        "Central",
        "East",
        "South",
        "West"
    ]
)

selected_category = st.sidebar.selectbox(

    "Category",

    [
        "All",
        "Furniture",
        "Office Supplies",
        "Technology"
    ]
)

discount_threshold = st.sidebar.slider(

    "High Discount Threshold",

    0.0,

    1.0,

    0.4
)

# =====================================================
# DATABASE QUERY
# =====================================================

query = """

SELECT

    f.sales,
    f.profit,
    f.discount,
    f.quantity,

    c.region,
    c.segment,

    p.category,

    d.order_date

FROM fact_sales f

JOIN dim_customer c
ON f.customer_id = c.customer_id

JOIN dim_product p
ON f.product_id = p.product_id

JOIN dim_date d
ON f.date_id = d.date_id

"""

df = pd.read_sql(
    query,
    engine
)

# =====================================================
# FILTERING
# =====================================================

filtered_df = df.copy()

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

# =====================================================
# RISK METRICS
# =====================================================

high_discount_df = filtered_df[
    filtered_df["discount"] > discount_threshold
]

high_discount_count = len(
    high_discount_df
)

loss_df = filtered_df[
    filtered_df["profit"] < 0
]

loss_count = len(
    loss_df
)

total_transactions = len(
    filtered_df
)

risk_score = round(

    (
        (
            high_discount_count
            +
            loss_count
        )
        /
        total_transactions
    ) * 100,

    2

) if total_transactions > 0 else 0

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Business Risk KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Risk Score",
        f"{risk_score}%"
    )

with k2:

    st.metric(
        "High Discount Transactions",
        high_discount_count
    )

with k3:

    st.metric(
        "Loss-Making Transactions",
        loss_count
    )

with k4:

    st.metric(
        "Total Transactions",
        total_transactions
    )

st.markdown("##")

# =====================================================
# RISK GAUGE CHART
# =====================================================

st.subheader("Enterprise Risk Gauge")

gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=risk_score,

        title={
            'text': "Business Risk Score"
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "#0066FF"
            },

            'steps': [

                {
                    'range': [0, 30],
                    'color': "#00C853"
                },

                {
                    'range': [30, 70],
                    'color': "#FFB300"
                },

                {
                    'range': [70, 100],
                    'color': "#FF5252"
                }
            ]
        }
    )
)

gauge.update_layout(

    paper_bgcolor="#0F172A",

    font_color="white",

    height=400
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

# =====================================================
# REGION RISK ANALYSIS
# =====================================================

st.subheader("Region Risk Analysis")

region_risk = filtered_df.groupby(
    "region"
).agg({

    "discount":"mean",

    "profit":"sum"

}).reset_index()

region_chart = px.bar(

    region_risk,

    x="region",

    y="discount",

    color="region",

    title="Average Discount by Region"
)

region_chart.update_layout(

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font_color="white"
)

st.plotly_chart(
    region_chart,
    use_container_width=True
)

# =====================================================
# CATEGORY RISK HEATMAP
# =====================================================

st.subheader("Category Risk Heatmap")

category_risk = filtered_df.groupby(
    "category"
).agg({

    "discount":"mean",

    "profit":"sum"

}).reset_index()

heatmap = px.density_heatmap(

    category_risk,

    x="category",

    y="profit",

    z="discount"
)

heatmap.update_layout(

    paper_bgcolor="#0F172A",

    plot_bgcolor="#0F172A",

    font_color="white"
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# =====================================================
# HIGH RISK TRANSACTIONS
# =====================================================

st.subheader("High Risk Transactions")

high_risk_df = filtered_df[

    (
        filtered_df["discount"]
        >
        discount_threshold
    )

    |

    (
        filtered_df["profit"]
        <
        0
    )
]

st.dataframe(

    high_risk_df.head(100),

    use_container_width=True
)

# =====================================================
# AI RISK INSIGHTS
# =====================================================

st.subheader("AI Risk Insights")

if risk_score < 30:

    st.success("""

    AI Insight:

    Business operations are currently
    stable with low enterprise risk
    exposure.

    """)

elif risk_score < 70:

    st.warning("""

    AI Risk Alert:

    Moderate business risk detected.

    High discounts and declining
    profitability are increasing
    operational risk.

    """)

else:

    st.error("""

    Critical Risk Alert:

    Enterprise risk is significantly high.

    Immediate action recommended on:
    pricing strategy,
    discount controls,
    and profitability optimization.

    """)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Powered by NexusIQ Risk Intelligence Engine"
)