"""
Scholarships API Routes for Phase 14B
Handles scholarship opportunities and applications
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db_models import get_db
from app.db_models.models import Scholarship

router = APIRouter()

class ScholarshipBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    apply_url: Optional[str] = None
    amount: Optional[float] = None

class ScholarshipCreate(ScholarshipBase):
    pass

class ScholarshipUpdate(ScholarshipBase):
    pass

class ScholarshipResponse(ScholarshipBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ScholarshipResponse])
def get_scholarships(
    skip: int = 0,
    limit: int = 100,
    min_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get all scholarships with optional amount filter"""
    query = db.query(Scholarship)
    if min_amount:
        query = query.filter(Scholarship.amount >= min_amount)
    scholarships = query.order_by(Scholarship.created_at.desc()).offset(skip).limit(limit).all()
    return scholarships

@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
def get_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    """Get a single scholarship by ID"""
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship

@router.post("/", response_model=ScholarshipResponse, status_code=201)
def create_scholarship(scholarship: ScholarshipCreate, db: Session = Depends(get_db)):
    """Create a new scholarship"""
    db_scholarship = Scholarship(**scholarship.dict())
    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship

@router.put("/{scholarship_id}", response_model=ScholarshipResponse)
def update_scholarship(
    scholarship_id: int,
    scholarship: ScholarshipUpdate,
    db: Session = Depends(get_db)
):
    """Update a scholarship"""
    db_scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not db_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    
    for key, value in scholarship.dict(exclude_unset=True).items():
        setattr(db_scholarship, key, value)
    
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship

@router.delete("/{scholarship_id}", status_code=204)
def delete_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    """Delete a scholarship"""
    db_scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not db_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    
    db.delete(db_scholarship)
    db.commit()
    return None
