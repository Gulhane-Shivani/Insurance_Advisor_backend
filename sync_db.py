from app.database.database import engine, Base
from sqlalchemy import text
# Import models to ensure they are registered with Base.metadata
from app.models.models import User, ContactMessage, InsuranceApplication

print("Dropping all tables with CASCADE...")
with engine.connect() as conn:
    # Get all table names
    result = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
    tables = [row[0] for row in result]
    
    for table in tables:
        print(f"Dropping table {table}...")
        conn.execute(text(f"DROP TABLE IF EXISTS \"{table}\" CASCADE"))
    
    # Explicitly drop the enum type if it exists
    print("Dropping enum type userrole...")
    conn.execute(text("DROP TYPE IF EXISTS userrole CASCADE"))
    
    conn.commit()

print("All tables dropped successfully.")

print("Recreating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables recreated successfully.")
