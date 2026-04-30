from app.database.database import engine
from sqlalchemy import text

def complete_migration():
    print("Starting complete migration for 'users' table...")
    with engine.connect() as conn:
        try:
            # 1. Rename password to password_hash
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='users' AND table_schema='public' AND column_name='password';
            """))
            if result.fetchone():
                conn.execute(text("ALTER TABLE users RENAME COLUMN password TO password_hash;"))
                print("Renamed 'password' to 'password_hash'.")

            # 2. Add role enum and column
            result = conn.execute(text("SELECT typname FROM pg_type WHERE typname = 'userrole';"))
            if not result.fetchone():
                conn.execute(text("CREATE TYPE userrole AS ENUM ('SUPER_ADMIN', 'ADMIN', 'AGENT', 'CSR', 'USER');"))
                print("Created ENUM 'userrole'.")

            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='users' AND table_schema='public' AND column_name='role';
            """))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE users ADD COLUMN role userrole DEFAULT 'USER' NOT NULL;"))
                print("Added 'role' column.")
            
            # 3. Add is_active column
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='users' AND table_schema='public' AND column_name='is_active';
            """))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;"))
                print("Added 'is_active' column.")

            # 4. Add updated_at column
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='users' AND table_schema='public' AND column_name='updated_at';
            """))
            if not result.fetchone():
                conn.execute(text("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();"))
                print("Added 'updated_at' column.")

            conn.commit()
            print("Migration completed successfully.")
        except Exception as e:
            print(f"Migration failed. Error details:")
            print(e)
            conn.rollback()

if __name__ == "__main__":
    complete_migration()
