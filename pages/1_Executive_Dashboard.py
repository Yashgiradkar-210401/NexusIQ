import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="NexusIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOGIN CHECK
# =====================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True

if not st.session_state.authenticated:

    st.warning("Please login first.")
    st.stop()

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"]{

    font-family: Arial, sans-serif;
}

/* =====================================================
BACKGROUND
===================================================== */

.stApp{

    background:
        linear-gradient(
            135deg,
            #020817 0%,
            #071224 40%,
            #0B172B 100%
        );

    color:white;
}

/* =====================================================
REMOVE STREAMLIT DEFAULT
===================================================== */

header[data-testid="stHeader"]{

    background:transparent;
}

#MainMenu{

    visibility:hidden;
}

.stDeployButton{

    display:none;
}

/* =====================================================
MAIN LAYOUT
===================================================== */

.main .block-container{

    padding-top:0rem;

    padding-left:1.2rem;

    padding-right:1.2rem;

    padding-bottom:2rem;

    max-width:100%;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{

    background:
        linear-gradient(
            180deg,
            #020817 0%,
            #071224 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.06);
}

/* =====================================================
SIDEBAR TEXT
===================================================== */

section[data-testid="stSidebar"] *{

    color:white !important;
}

/* =====================================================
SIDEBAR SELECTBOX FIX
===================================================== */

.stSelectbox{

    margin-bottom:18px;
}

.stSelectbox label{

    font-size:16px !important;

    font-weight:600 !important;

    color:#E2E8F0 !important;

    margin-bottom:8px !important;
}

.stSelectbox div[data-baseweb="select"]{

    background:#0F172A !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    border-radius:14px !important;

    min-height:52px !important;

    box-shadow:
        0 4px 14px rgba(0,0,0,0.25);
}
.stSelectbox div[data-baseweb="select"] > div{

    background:#0F172A !important;

    color:white !important;

    border:none !important;
}

/* INPUT TEXT */

.stSelectbox input{

    color:white !important;
}

/* DROPDOWN VALUE */

.stSelectbox div[data-baseweb="single-select"]{

    color:white !important;

    background:#0F172A !important;
}

/* PLACEHOLDER */

.stSelectbox div[data-baseweb="placeholder"]{

    color:#CBD5E1 !important;
}

/* DROPDOWN ARROW */

.stSelectbox svg{

    fill:white !important;
}

/* DROPDOWN MENU */

div[role="listbox"]{

    background:#0F172A !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    color:white !important;
}

/* OPTIONS */

div[role="option"]{

    background:#0F172A !important;

    color:white !important;
}

div[role="option"]:hover{

    background:#0066FF !important;
}
/* =====================================================
SELECTED VALUE
===================================================== */

.stSelectbox span{

    color:white !important;

    font-size:15px !important;

    font-weight:500 !important;
}

/* =====================================================
HEADER
===================================================== */

.sticky-header{

    position:sticky;

    top:0;

    z-index:999;

    background:
        rgba(8,17,32,0.92);

    backdrop-filter:blur(14px);

    padding:18px;

    border-radius:0px 0px 18px 18px;

    border-bottom:
        1px solid rgba(255,255,255,0.06);

    margin-bottom:24px;
}

/* =====================================================
TABS
===================================================== */

.stTabs [data-baseweb="tab-list"]{

    gap:10px;

    background:
        rgba(255,255,255,0.03);

    padding:10px;

    border-radius:18px;

    overflow-x:auto;
}

.stTabs [data-baseweb="tab"]{

    background:
        rgba(255,255,255,0.04);

    border-radius:12px;

    padding:10px 18px;

    color:#CBD5E1;

    font-weight:600;

    transition:0.3s;
}

.stTabs [aria-selected="true"]{

    background:
        linear-gradient(
            90deg,
            #0066FF,
            #0050D4
        ) !important;

    color:white !important;
}

/* =====================================================
METRIC CARDS
===================================================== */

div[data-testid="metric-container"]{

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:18px;

    padding:18px;

    box-shadow:
        0 8px 20px rgba(0,0,0,0.25);

    backdrop-filter:blur(12px);

    transition:0.3s;
}

div[data-testid="metric-container"]:hover{

    transform:translateY(-3px);

    border:
        1px solid rgba(0,102,255,0.45);
}
/* =====================================================
KPI CARD TEXT FIX
===================================================== */

div[data-testid="metric-container"]{

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.92),
            rgba(30,41,59,0.92)
        ) !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    border-radius:20px !important;

    padding:22px !important;

    box-shadow:
        0 10px 25px rgba(0,0,0,0.35);

    backdrop-filter:blur(12px);
}

/* KPI LABEL */

div[data-testid="metric-container"] label{

    color:#CBD5E1 !important;

    font-size:16px !important;

    font-weight:600 !important;

    opacity:1 !important;
}

/* =====================================================
KPI VALUE FIX
===================================================== */

div[data-testid="metric-container"] > div {

    color:white !important;
}

div[data-testid="metric-container"] label {

    color:#CBD5E1 !important;

    opacity:1 !important;

    font-size:16px !important;

    font-weight:600 !important;
}

            
            /* =====================================================
FORCE KPI VISIBILITY
===================================================== */

div[data-testid="metric-container"]{

    opacity:1 !important;

    visibility:visible !important;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E293B
        ) !important;
}

div[data-testid="metric-container"] *{

    color:#FFFFFF !important;

    opacity:1 !important;
}
/* =====================================================
METRIC VALUE FINAL FIX
===================================================== */

div[data-testid="metric-container"] [data-testid="stMetricValue"] {

    color: #FFFFFF !important;

    font-size: 42px !important;

    font-weight: 800 !important;

    opacity: 1 !important;
}
            
            /* LABEL FIX */

div[data-testid="metric-container"] label {

    color: #CBD5E1 !important;

    opacity: 1 !important;
}

/* FORCE ALL INNER TEXT WHITE */

div[data-testid="metric-container"] * {

    color: white !important;
}

div[data-testid="metric-container"] svg {

    color:#00C853 !important;
}
/* KPI DELTA */

div[data-testid="metric-container"] [data-testid="stMetricDelta"]{

    color:#00C853 !important;

    font-size:14px !important;

    font-weight:600 !important;
}

/* MOBILE KPI FIX */

@media screen and (max-width:768px){

    div[data-testid="metric-container"]{

        padding:18px !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"]{

        font-size:32px !important;
    }

    div[data-testid="metric-container"] label{

        font-size:14px !important;
    }
}
            


/* =====================================================
CHARTS
===================================================== */

/* =====================================================
CHART CONTAINER FIX
===================================================== */

[data-testid="stVerticalBlock"] canvas{

    background:
        rgba(15,23,42,0.92);

    border-radius:18px;
}
/* =====================================================
DATAFRAME
===================================================== */

.stDataFrame{

    border-radius:18px;

    overflow:hidden;
}

/* =====================================================
MOBILE RESPONSIVE
===================================================== */

@media screen and (max-width:768px){

    .main .block-container{

        padding-left:0.6rem;

        padding-right:0.6rem;
    }

    .stTabs [data-baseweb="tab"]{

        font-size:12px;

        padding:8px 10px;
    }

    div[data-testid="metric-container"]{

        padding:14px;
    }

    .stSelectbox div[data-baseweb="select"]{

        min-height:48px !important;
    }
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar{

    width:8px;
}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div style="position:sticky;top:0;z-index:999;background:#081120;padding:18px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:20px;">'
    
    '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">'
    
    '<div>'
    
    '<div style="font-size:52px;font-weight:800;color:white;">NexusIQ</div>'
    
    '<div style="color:#CBD5E1;font-size:16px;">Enterprise Decision Intelligence Platform</div>'
    
    '</div>'
    
    '<div style="color:#94A3B8;font-size:13px;text-align:right;">'
    
    'Live Enterprise Analytics<br>AI-Powered BI Engine'
    
    '</div>'
    
    '</div>'
    
    '</div>',
    
    unsafe_allow_html=True
)
# =====================================================
# DATABASE CONNECTION
# =====================================================

engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/nexusiq"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## NexusIQ")

    st.markdown(
        "Enterprise Intelligence Engine"
    )

    st.markdown("---")

    st.selectbox(
        "Region",
        [
            "All",
            "North",
            "South",
            "East",
            "West"
        ]
    )

    st.selectbox(
        "Business Unit",
        [
            "All",
            "Analytics",
            "Finance",
            "Operations"
        ]
    )

    st.selectbox(
        "Category",
        [
            "All",
            "Enterprise",
            "AI",
            "Finance"
        ]
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive",
    "Customer",
    "Forecasting",
    "Risk",
    "Explorer"
])

# =====================================================
# FETCH DATA
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

df = pd.read_sql(query, engine)

# =====================================================
# EXECUTIVE TAB
# =====================================================

with tab1:

    total_revenue = df['sales'].sum()

    total_profit = df['profit'].sum()

    total_orders = len(df)

    profit_margin = round(
        (total_profit / total_revenue) * 100,
        2
    )

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    c1.metric(
        "Revenue",
        f"${total_revenue:,.2f}"
    )

    c2.metric(
        "Profit",
        f"${total_profit:,.2f}"
    )

    c3.metric(
        "Profit Margin",
        f"{profit_margin}%"
    )

    c4.metric(
        "Orders",
        total_orders
    )

    revenue_trend = df.groupby(
        ['year', 'month']
    )['sales'].sum().reset_index()

    revenue_trend['month_label'] = (
        revenue_trend['year'].astype(str)
        + "-"
        +
        revenue_trend['month'].astype(str)
    )

    st.subheader("Revenue Trend")

    st.line_chart(
        revenue_trend.set_index(
            'month_label'
        )['sales']
    )

# =====================================================
# CUSTOMER TAB
# =====================================================

with tab2:

    st.subheader("Customer Segmentation")

    segment_revenue = df.groupby(
        'segment'
    )['sales'].sum()

    st.bar_chart(segment_revenue)

# =====================================================
# FORECASTING TAB
# =====================================================

with tab3:

    st.subheader("Revenue Forecasting")

    forecast_df = revenue_trend.copy()

    forecast_df['time_index'] = range(
        len(forecast_df)
    )

    X = forecast_df[['time_index']]

    y = forecast_df['sales']

    model = LinearRegression()

    model.fit(X, y)

    future_index = pd.DataFrame({

        'time_index': range(
            len(forecast_df),
            len(forecast_df) + 6
        )

    })

    predictions = model.predict(
        future_index
    )

    future_forecast = pd.DataFrame({

        'Future Month': [
            f'Month {i}'
            for i in range(1, 7)
        ],

        'Predicted Revenue': predictions

    })

    st.line_chart(
        future_forecast.set_index(
            'Future Month'
        )
    )

# =====================================================
# RISK TAB
# =====================================================

with tab4:

    st.subheader("Risk Monitoring")

    risk_df = df.groupby(
        'region'
    ).agg({

        'sales':'sum',
        'profit':'sum'

    }).reset_index()

    risk_df['margin'] = round(

        (
            risk_df['profit']
            /
            risk_df['sales']
        ) * 100,

        2
    )

    st.bar_chart(
        risk_df.set_index(
            'region'
        )['margin']
    )

# =====================================================
# EXPLORER TAB
# =====================================================

with tab5:

    st.subheader("Data Explorer")

    st.dataframe(df.head(100))