from app.database.database import engine
from app.models.models import InsuranceApplication

# Drop the insurance_applications table
print("Dropping insurance_applications table...")
InsuranceApplication.__table__.drop(engine)
print("Table dropped successfully. It will be recreated on the next API request or server restart.")
