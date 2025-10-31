"""
Testimonials API Routes for Phase 14B
Handles customer testimonials and reviews
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db_models import get_db
from app.db_models.models import Testimonial

router = APIRouter()

class TestimonialBase(BaseModel):
    user_name: str
    photo_url: Optional[str] = None
    quote: str
    rating: int = 5

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(TestimonialBase):
    pass

class TestimonialResponse(TestimonialBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[TestimonialResponse])
def get_testimonials(
    skip: int = 0,
    limit: int = 100,
    min_rating: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all testimonials with optional rating filter"""
    query = db.query(Testimonial)
    if min_rating:
        query = query.filter(Testimonial.rating >= min_rating)
    testimonials = query.order_by(Testimonial.created_at.desc()).offset(skip).limit(limit).all()
    return testimonials

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
def get_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    """Get a single testimonial by ID"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return testimonial

@router.post("/", response_model=TestimonialResponse, status_code=201)
def create_testimonial(testimonial: TestimonialCreate, db: Session = Depends(get_db)):
    """Create a new testimonial"""
    if testimonial.rating < 1 or testimonial.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    db_testimonial = Testimonial(**testimonial.dict())
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial

@router.put("/{testimonial_id}", response_model=TestimonialResponse)
def update_testimonial(
    testimonial_id: int,
    testimonial: TestimonialUpdate,
    db: Session = Depends(get_db)
):
    """Update a testimonial"""
    db_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    if testimonial.rating and (testimonial.rating < 1 or testimonial.rating > 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    for key, value in testimonial.dict(exclude_unset=True).items():
        setattr(db_testimonial, key, value)
    
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial

@router.delete("/{testimonial_id}", status_code=204)
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    """Delete a testimonial"""
    db_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    db.delete(db_testimonial)
    db.commit()
    return None
