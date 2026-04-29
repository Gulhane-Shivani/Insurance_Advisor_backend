from app.database.database import engine, Base
from sqlalchemy import text

print("Dropping all tables with CASCADE...")
with engine.connect() as conn:
    # Get all table names
    result = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
    tables = [row[0] for row in result]
    
    for table in tables:
        print(f"Dropping table {table}...")
        conn.execute(text(f"DROP TABLE IF EXISTS \"{table}\" CASCADE"))
    
    conn.commit()

print("All tables dropped successfully.")
print("Tables will be recreated on the next API request or server restart.")
