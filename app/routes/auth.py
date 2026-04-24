from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas
from ..utils import security

router = APIRouter(tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = security.get_password_hash(user.password)
    
    # Create new user
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Check for hardcoded admin credentials
    if login_data.email == security.ADMIN_EMAIL and login_data.password == security.ADMIN_PASSWORD:
        access_token = security.create_access_token(data={"sub": security.ADMIN_EMAIL})
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user": {
                "id": "admin",
                "email": security.ADMIN_EMAIL,
                "full_name": "Administrator",
                "role": "admin"
            }
        }

    # Find user by email
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    
    if not user or not security.verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    access_token = security.create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": "user"
        }
    }
