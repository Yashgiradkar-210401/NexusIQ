import pandas as pd

from database import engine

# Read CSV file
df = pd.read_csv("datasets/raw/superstore.csv")

# =========================
# CUSTOMER DIMENSION
# =========================

dim_customer = df[
    ['Customer Name', 'Segment', 'Region']
].drop_duplicates()

dim_customer.columns = [
    'customer_name',
    'segment',
    'region'
]

dim_customer.to_sql(
    'dim_customer',
    engine,
    if_exists='append',
    index=False
)

# =========================
# PRODUCT DIMENSION
# =========================

dim_product = df[
    ['Category', 'Sub-Category', 'Product Name']
].drop_duplicates()

dim_product.columns = [
    'category',
    'sub_category',
    'product_name'
]

dim_product.to_sql(
    'dim_product',
    engine,
    if_exists='append',
    index=False
)




print("Data Loaded Successfully")

df['Order Date'] = pd.to_datetime(df['Order Date'])

dim_date = df[['Order Date']].drop_duplicates()

dim_date['year'] = dim_date['Order Date'].dt.year
dim_date['quarter'] = dim_date['Order Date'].dt.quarter
dim_date['month'] = dim_date['Order Date'].dt.month

dim_date.columns = [
    'order_date',
    'year',
    'quarter',
    'month'
]

dim_date.to_sql(
    'dim_date',
    engine,
    if_exists='append',
    index=False
)

print("Date Dimension Loaded")

# =========================
# LOAD DIMENSION TABLES
# =========================

customer_df = pd.read_sql(
    "SELECT * FROM dim_customer",
    engine
)

product_df = pd.read_sql(
    "SELECT * FROM dim_product",
    engine
)

date_df = pd.read_sql(
    "SELECT * FROM dim_date",
    engine
)

# =========================
# PREPARE FACT TABLE
# =========================

fact_df = df.copy()

# CUSTOMER JOIN
fact_df = fact_df.merge(
    customer_df,
    left_on=['Customer Name', 'Segment', 'Region'],
    right_on=['customer_name', 'segment', 'region'],
    how='left'
)

# PRODUCT JOIN
fact_df = fact_df.merge(
    product_df,
    left_on=['Category', 'Sub-Category', 'Product Name'],
    right_on=['category', 'sub_category', 'product_name'],
    how='left'
)

# DATE JOIN
date_df['order_date'] = pd.to_datetime(date_df['order_date'])

fact_df = fact_df.merge(
    date_df,
    left_on='Order Date',
    right_on='order_date',
    how='left'
)

# =========================
# FINAL FACT TABLE
# =========================

fact_sales = fact_df[
    [
        'customer_id',
        'product_id',
        'date_id',
        'Sales',
        'Profit',
        'Quantity',
        'Discount'
    ]
]

fact_sales.columns = [
    'customer_id',
    'product_id',
    'date_id',
    'sales',
    'profit',
    'quantity',
    'discount'
]

# =========================
# LOAD FACT TABLE
# =========================

fact_sales.to_sql(
    'fact_sales',
    engine,
    if_exists='append',
    index=False
)

print("Fact Sales Loaded Successfully")