import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()
# Replace the following URL with your actual database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)

# Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Drop all tables
metadata.drop_all(engine)

print("All tables have been dropped.")
