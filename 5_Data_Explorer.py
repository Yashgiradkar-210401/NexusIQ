import streamlit as st
import pandas as pd

from styles import load_css
from database import engine
load_css()


st.title("Data Explorer")

query = """
SELECT *
FROM fact_sales
LIMIT 100;
"""

df = pd.read_sql(query, engine)

st.dataframe(df)