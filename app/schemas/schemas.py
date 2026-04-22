from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Contact Message Schemas
class ContactMessageCreate(BaseModel):
    full_name: str
    email: EmailStr
    subject: str
    message: str

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Insurance Schemas
class InsuranceApplicationBase(BaseModel):
    user_name: str
    type: str
    amount: str
    status: str = "Pending"

class InsuranceApplicationResponse(InsuranceApplicationBase):
    id: int
    applied_date: datetime

    class Config:
        from_attributes = True

class InsuranceApplicationStatusUpdate(BaseModel):
    status: str

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[dict] = None

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str
