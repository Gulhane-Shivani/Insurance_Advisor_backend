from app.database.database import engine
from sqlalchemy import text

def run_migration():
    print("Starting migration: Adding 'phone' column to 'users' table...")
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR;"))
            conn.commit()
            print("Migration successful: 'phone' column added.")
        except Exception as e:
            print(f"Migration failed or column already exists. Error details:")
            print(e)
            conn.rollback()

if __name__ == "__main__":
    run_migration()
