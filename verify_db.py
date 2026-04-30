from app.database.database import engine, get_db
from app.models.models import User
from sqlalchemy.orm import Session

def verify():
    db = next(get_db())
    try:
        user = db.query(User).first()
        print("Successfully queried User.")
        if user:
            print(f"User email: {user.email}, phone: {user.phone}")
        else:
            print("No users found.")
    except Exception as e:
        print(f"Error querying User: {e}")

if __name__ == "__main__":
    verify()
