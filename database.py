from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_zkZl6OmfIYL9@ep-winter-lake-aqh78g6b-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(
    DATABASE_URL
)