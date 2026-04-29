import os
from dotenv import load_dotenv
from app.database.database import SessionLocal
from app.models.models import User, UserRole
from app.utils.security import get_password_hash

load_dotenv()

def seed_admin():
    db = SessionLocal()
    try:
        email = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
        password = os.getenv("ADMIN_PASSWORD", "adminPass")
        
        # Check if already exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Admin {email} already exists.")
            return

        new_admin = User(
            full_name="Super Administrator",
            email=email,
            password_hash=get_password_hash(password),
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        print(f"Super Admin created: {email}")
    except Exception as e:
        print(f"Error seeding admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
