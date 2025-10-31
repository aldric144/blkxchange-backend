"""
Partners API Routes for Phase 14B
Handles partner organization management
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db_models import get_db
from app.db_models.models import Partner

router = APIRouter()

class PartnerBase(BaseModel):
    org_name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(PartnerBase):
    pass

class PartnerResponse(PartnerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[PartnerResponse])
def get_partners(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all partner organizations"""
    partners = db.query(Partner).offset(skip).limit(limit).all()
    return partners

@router.get("/{partner_id}", response_model=PartnerResponse)
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    """Get a single partner by ID"""
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

@router.post("/", response_model=PartnerResponse, status_code=201)
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db)):
    """Create a new partner organization"""
    db_partner = Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

@router.put("/{partner_id}", response_model=PartnerResponse)
def update_partner(
    partner_id: int,
    partner: PartnerUpdate,
    db: Session = Depends(get_db)
):
    """Update a partner"""
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    for key, value in partner.dict(exclude_unset=True).items():
        setattr(db_partner, key, value)
    
    db.commit()
    db.refresh(db_partner)
    return db_partner

@router.delete("/{partner_id}", status_code=204)
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    """Delete a partner"""
    db_partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    db.delete(db_partner)
    db.commit()
    return None
