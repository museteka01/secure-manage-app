from app.database import engine

with engine.connect() as conn:
    print("✅ Connected to PostgreSQL")
