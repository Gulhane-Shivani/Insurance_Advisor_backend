from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas
from ..utils import security

router = APIRouter(tags=["Insurance"])

@router.post("/insurance/apply", status_code=status.HTTP_201_CREATED, response_model=schemas.InsuranceApplicationResponse)
def apply_for_insurance(
    application: schemas.InsuranceApplicationBase, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.get_current_user)
):
    new_app = models.InsuranceApplication(
        full_name=application.full_name,
        email=application.email,
        phone_number=application.phone_number,
        insurance_type=application.insurance_type,
        vehicle_make=application.vehicle_make,
        vehicle_model=application.vehicle_model,
        manufacturing_year=application.manufacturing_year,
        registration_number=application.registration_number,
        message=application.message,
        status="Pending"
    )
    
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    return new_app

@router.get("/my-applications", response_model=list[schemas.InsuranceApplicationResponse])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(security.get_current_user)
):
    # current_user is a dict containing email and role
    user_email = current_user.get("email")
    applications = db.query(models.InsuranceApplication).filter(models.InsuranceApplication.email == user_email).all()
    return applications
