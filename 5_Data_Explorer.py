import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from styles import load_css

load_css()

engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/nexusiq"
)

st.title("Data Explorer")

query = """
SELECT *
FROM fact_sales
LIMIT 100;
"""

df = pd.read_sql(query, engine)

st.dataframe(df)