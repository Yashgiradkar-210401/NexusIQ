import streamlit as st

# =====================================================
# PAGE CONFIG MUST BE FIRST
# =====================================================

st.set_page_config(
    page_title="Forecasting",
    layout="wide"
)

import pandas as pd
from sklearn.linear_model import LinearRegression
from database import engine
from styles import load_css

# =====================================================
# LOAD CSS
# =====================================================

load_css()



# =====================================================
# PAGE TITLE
# =====================================================

st.title("Forecasting Dashboard")

st.write("Forecasting Page Loaded Successfully")

# =====================================================
# QUERY
# =====================================================

query = """
SELECT
    d.year,
    d.month,
    SUM(f.sales) AS revenue

FROM fact_sales f

JOIN dim_date d
ON f.date_id = d.date_id

GROUP BY d.year, d.month

ORDER BY d.year, d.month
"""

df = pd.read_sql(query, engine)

# =====================================================
# SHOW DATA
# =====================================================

st.subheader("Revenue Dataset")

st.dataframe(df)

# =====================================================
# SIMPLE FORECAST
# =====================================================

df['time_index'] = range(len(df))

X = df[['time_index']]

y = df['revenue']

model = LinearRegression()

model.fit(X, y)

future_df = pd.DataFrame({
    'time_index': [len(df)]
})

prediction = model.predict(future_df)

st.subheader("Next Month Revenue Prediction")

st.metric(
    "Forecast Revenue",
    f"${prediction[0]:,.2f}"
)