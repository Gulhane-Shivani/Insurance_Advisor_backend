from app.database.database import SessionLocal
from app.models.models import User, UserRole

db = SessionLocal()
try:
    stats = {}
    for role in UserRole:
        print(f"Counting for role: {role}")
        count = db.query(User).filter(User.role == role).count()
        stats[role.value] = count
    print(f"Stats: {stats}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
