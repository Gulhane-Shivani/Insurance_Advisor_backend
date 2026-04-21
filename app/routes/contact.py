from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(tags=["Contact"])

@router.post("/contact", status_code=status.HTTP_201_CREATED)
def submit_contact_form(message: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    new_message = models.ContactMessage(
        full_name=message.full_name,
        email=message.email,
        subject=message.subject,
        message=message.message
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return {"message": "Your message has been submitted successfully"}
