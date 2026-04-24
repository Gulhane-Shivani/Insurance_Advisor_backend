from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InsuranceApplication(Base):
    __tablename__ = "insurance_applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    insurance_type = Column(String, nullable=False)
    vehicle_make = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    manufacturing_year = Column(String, nullable=False)
    registration_number = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, default="Pending")
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
