"""
Users API Routes for Phase 14B
Handles user management and membership tiers
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
import sqlite3
import os

from app.db_models import get_db
from app.db_models.models import User, UserEvent, UserBadge, Badge

router = APIRouter()

COMMENTS_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "comments.db")

class UserBase(BaseModel):
    username: str
    email: EmailStr
    membership_tier: str = "Free"

class UserCreate(UserBase):
    password_hash: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    membership_tier: Optional[str] = None

class UserResponse(UserBase):
    id: int
    join_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    membership_tier: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all users with optional membership tier filter"""
    query = db.query(User)
    if membership_tier:
        query = query.filter(User.membership_tier == membership_tier)
    users = query.offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get a user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return None

@router.get("/username/{username}")
def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get user profile with activity history and badges"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_events = db.query(UserEvent).filter(UserEvent.user_id == user.id).all()
    
    user_badges_query = db.query(UserBadge, Badge).join(
        Badge, UserBadge.badge_id == Badge.id
    ).filter(UserBadge.user_id == user.id).all()
    
    badges = [
        {
            "id": badge.id,
            "name": badge.name,
            "description": badge.description,
            "icon": badge.icon,
            "earned_at": user_badge.earned_at.isoformat()
        }
        for user_badge, badge in user_badges_query
    ]
    
    comments = []
    try:
        conn = sqlite3.connect(COMMENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, article_id, content, created_at FROM comments WHERE author = ? ORDER BY created_at DESC LIMIT 10",
            (username,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        comments = [
            {
                "id": row[0],
                "article_id": row[1],
                "content": row[2],
                "created_at": row[3]
            }
            for row in rows
        ]
    except Exception as e:
        pass
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "membership_tier": user.membership_tier,
        "join_date": user.join_date.isoformat(),
        "events": [
            {
                "id": ue.id,
                "event_id": ue.event_id,
                "status": ue.status,
                "created_at": ue.created_at.isoformat()
            }
            for ue in user_events
        ],
        "badges": badges,
        "comments": comments,
        "stats": {
            "total_events": len(user_events),
            "total_badges": len(badges),
            "total_comments": len(comments)
        }
    }
