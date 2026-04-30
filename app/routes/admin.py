from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas
from ..models.models import UserRole

from ..utils import security

router = APIRouter(prefix="/admin", tags=["Admin"])

# Define role-based access
admin_access = security.RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN])
staff_access = security.RoleChecker([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.AGENT, UserRole.CSR])

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_access)
):
    # If requester is ADMIN (not SUPER_ADMIN), only count non-admin users
    user_query = db.query(models.User)
    if current_user["role"] == UserRole.ADMIN:
        user_query = user_query.filter(models.User.role.notin_([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
    
    user_count = user_query.count()
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
    current_user: dict = Depends(staff_access)
):
    # Agents might not need all contacts, but CSRs and Admins do. 
    # For now, following the pattern of allowing staff.
    contacts = db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()
    return contacts

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_access)
):
    contact = db.query(models.ContactMessage).filter(models.ContactMessage.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()

# Users Management (Old, now handled by /users router but keeping for backward compatibility or basic list)
@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_access)
):
    query = db.query(models.User)
    # If requester is ADMIN (not SUPER_ADMIN), hide admin and super_admin data
    if current_user["role"] == UserRole.ADMIN:
        query = query.filter(models.User.role.notin_([UserRole.ADMIN, UserRole.SUPER_ADMIN]))
        
    users = query.order_by(models.User.created_at.desc()).all()
    return users

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_access)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# Insurance Applications Management
@router.get("/insurance", response_model=List[schemas.InsuranceApplicationResponse])
def get_all_insurance(
    db: Session = Depends(get_db),
    current_user: dict = Depends(staff_access)
):
    insurances = db.query(models.InsuranceApplication).order_by(models.InsuranceApplication.applied_date.desc()).all()
    return insurances

@router.put("/insurance/{insurance_id}/status", response_model=schemas.InsuranceApplicationResponse)
def update_insurance_status(
    insurance_id: int, 
    status_update: schemas.InsuranceApplicationStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(staff_access)
):
    insurance = db.query(models.InsuranceApplication).filter(models.InsuranceApplication.id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance application not found")
    insurance.status = status_update.status
    db.commit()
    db.refresh(insurance)
    return insurance
