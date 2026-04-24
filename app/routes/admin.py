from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

from ..utils import security
from ..schemas import schemas

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    # Basic check: if current_user is the admin email
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_count = db.query(models.User).count()
    contact_count = db.query(models.ContactMessage).count()
    insurance_count = db.query(models.InsuranceApplication).count()
    return {
        "users": user_count,
        "contacts": contact_count,
        "insurance": insurance_count
    }

# Contacts Management
@router.get("/contacts", response_model=List[schemas.ContactMessageResponse])
def get_all_contacts(
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    contacts = db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()
    return contacts

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    contact = db.query(models.ContactMessage).filter(models.ContactMessage.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()

# Users Management
@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return users

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# Insurance Applications Management
@router.get("/insurance", response_model=List[schemas.InsuranceApplicationResponse])
def get_all_insurance(
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    insurances = db.query(models.InsuranceApplication).order_by(models.InsuranceApplication.applied_date.desc()).all()
    return insurances

@router.put("/insurance/{insurance_id}/status", response_model=schemas.InsuranceApplicationResponse)
def update_insurance_status(
    insurance_id: int, 
    status_update: schemas.InsuranceApplicationStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(security.get_current_user)
):
    if current_user != security.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not authorized")
    insurance = db.query(models.InsuranceApplication).filter(models.InsuranceApplication.id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance application not found")
    insurance.status = status_update.status
    db.commit()
    db.refresh(insurance)
    return insurance
