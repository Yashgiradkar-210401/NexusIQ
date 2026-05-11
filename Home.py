import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
logo = Image.open("assets/logo.png")
from database import engine
from auth import login, logout

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="NexusIQ",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =====================================================
# LOGIN CHECK
# =====================================================

if not st.session_state.authenticated:
    login()
    st.stop()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* BACKGROUND */

.stApp{
    background: linear-gradient(
        135deg,
        #020817 0%,
        #071224 50%,
        #0F172A 100%
    );
    color:white;
}

/* REMOVE STREAMLIT STYLING */

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

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #020817,
        #071224
    );
}

/* METRICS */

[data-testid="metric-container"]{
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
}

/* TEXT */

h1,h2,h3{
    color:white !important;
}

.stMarkdown,
.stText{
    color:white !important;
}

/* MOBILE */

@media screen and (max-width:768px){

    h1{
        font-size:42px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================


st.markdown("""
<style>

@media (max-width: 768px){

    h1{
        font-size:42px !important;
    }

    p{
        font-size:16px !important;
    }

}

</style>
""", unsafe_allow_html=True)
with st.sidebar:
    col1, col2 = st.columns([1.2,4])

with col1:

    st.image(
        logo,
        width=90
    )

with col2:

    st.markdown(
        """
        <h1 style='
            margin-bottom:0;
            color:white;
            font-size:48px;
            font-weight:800;
        '>
        NexusIQ
        </h1>

        <p style='
            color:#CBD5E1;
            font-size:18px;
            margin-top:-10px;
        '>
        Enterprise Decision Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.write(
        f"👤 {st.session_state.username}"
    )

    st.write(
        f"🛡️ {st.session_state.role}"
    )

    st.markdown("---")

    st.subheader("Global Filters")

    region = st.selectbox(
        "Region",
        ["All", "North", "South", "East", "West"]
    )

    category = st.selectbox(
        "Category",
        ["All", "Technology", "Furniture", "Office Supplies"]
    )

    business = st.selectbox(
        "Business Unit",
        ["All", "Consumer", "Corporate", "Home Office"]
    )

    st.markdown("---")

    logout()

# =====================================================
# HERO SECTION
# =====================================================

hero1, hero2 = st.columns([4,1])

with hero1:

    st.title("NexusIQ")

    st.subheader(
        "Enterprise Decision Intelligence Platform"
    )

with hero2:

    st.metric(
        "AI Engine",
        "ACTIVE"
    )

    st.caption(
        f"Last Sync: {datetime.now().strftime('%H:%M:%S')}"
    )

st.markdown("---")

# =====================================================
# DATABASE QUERY
# =====================================================

query = """

SELECT

    f.sales,
    f.profit,
    f.discount,

    c.region,
    c.segment,
    c.customer_id,

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

df = pd.read_sql(
    query,
    engine
)

# =====================================================
# FILTERING LOGIC
# =====================================================

filtered_df = df.copy()

if region != "All":

    filtered_df = filtered_df[
        filtered_df["region"] == region
    ]

if category != "All":

    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

if business != "All":

    filtered_df = filtered_df[
        filtered_df["segment"] == business
    ]

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = filtered_df["sales"].sum()

total_profit = filtered_df["profit"].sum()

total_orders = len(filtered_df)

profit_margin = round(

    (total_profit / total_revenue) * 100,

    2

) if total_revenue > 0 else 0

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("Enterprise KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Revenue",
        f"${total_revenue:,.2f}",
        "+12%"
    )

with k2:

    st.metric(
        "Profit",
        f"${total_profit:,.2f}",
        "+8%"
    )

with k3:

    st.metric(
        "Profit Margin",
        f"{profit_margin}%",
        "+3%"
    )

with k4:

    st.metric(
        "Orders",
        total_orders,
        "+5%"
    )

st.markdown("##")

# =====================================================
# MODULES
# =====================================================

st.subheader("Platform Modules")

m1, m2, m3 = st.columns(3)

with m1:

    st.info("""
    📊 Executive Dashboard

    Enterprise KPIs, profitability,
    revenue intelligence and analytics.
    """)

with m2:

    st.info("""
    👥 Customer Intelligence

    Customer segmentation,
    retention and LTV analysis.
    """)

with m3:

    st.info("""
    📈 Forecasting Engine

    AI-driven revenue prediction
    and trend forecasting.
    """)

st.markdown("##")

# =====================================================
# REVENUE TREND
# =====================================================

revenue_trend = filtered_df.groupby(
    ['year', 'month']
)['sales'].sum().reset_index()

revenue_trend['month_label'] = (

    revenue_trend['year'].astype(str)
    +
    "-"
    +
    revenue_trend['month'].astype(str)

)

# =====================================================
# CHARTS
# =====================================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("Revenue Trend")

    fig = px.line(

        revenue_trend,

        x="month_label",

        y="sales",

        markers=True
    )

    fig.update_layout(

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with c2:

    st.subheader("Region Wise Revenue")

    region_df = filtered_df.groupby(
        "region"
    )["sales"].sum().reset_index()

    region_chart = px.bar(

        region_df,

        x="region",

        y="sales",

        color="region"
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
# AI INSIGHTS
# =====================================================

st.subheader("AI Executive Insights")

if len(filtered_df) > 0:

    top_region = filtered_df.groupby(
        "region"
    )["sales"].sum().idxmax()

    top_category = filtered_df.groupby(
        "category"
    )["sales"].sum().idxmax()

    st.success(f"""
    Revenue Growth Detected

    {top_region} region is generating
    the highest revenue currently.
    """)

    st.warning(f"""
    Category Performance Alert

    {top_category} category is showing
    strong business performance.
    """)

# =====================================================
# DATA PREVIEW
# =====================================================

st.subheader("Filtered Data Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Powered by NexusIQ Decision Intelligence Engine • Version 1.0 Enterprise"
)