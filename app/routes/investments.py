from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

from app.db_models import get_db
from app.db_models.models import Investment

router = APIRouter()

class InvestmentResponse(BaseModel):
    id: int
    category: str
    recipient_name: str
    amount: float
    description: str
    date: datetime

class InvestmentSummary(BaseModel):
    total_invested: float
    category_breakdown: Dict[str, float]
    recent_investments: List[InvestmentResponse]
    hbcu_count: int
    startup_count: int
    bank_count: int

@router.get("", response_model=InvestmentSummary)
async def get_investments(db: Session = Depends(get_db)):
    """Get investment transparency data showing 3% reinvestment allocation"""
    
    investments = db.query(Investment).order_by(Investment.date.desc()).all()
    
    total_invested = sum(inv.amount for inv in investments)
    
    category_breakdown = {}
    hbcu_count = 0
    startup_count = 0
    bank_count = 0
    
    for inv in investments:
        category = inv.category
        if category not in category_breakdown:
            category_breakdown[category] = 0
        category_breakdown[category] += inv.amount
        
        if category.lower() == "hbcu":
            hbcu_count += 1
        elif category.lower() == "startup":
            startup_count += 1
        elif category.lower() in ["bank", "black bank"]:
            bank_count += 1
    
    recent_investments = investments[:10]
    
    return {
        "total_invested": total_invested,
        "category_breakdown": category_breakdown,
        "recent_investments": [
            {
                "id": inv.id,
                "category": inv.category,
                "recipient_name": inv.recipient_name,
                "amount": inv.amount,
                "description": inv.description or "",
                "date": inv.date
            }
            for inv in recent_investments
        ],
        "hbcu_count": hbcu_count,
        "startup_count": startup_count,
        "bank_count": bank_count
    }

@router.get("/by-category/{category}", response_model=List[InvestmentResponse])
async def get_investments_by_category(category: str, db: Session = Depends(get_db)):
    """Get investments filtered by category (HBCU, Startup, Bank)"""
    
    investments = db.query(Investment).filter(
        Investment.category.ilike(f"%{category}%")
    ).order_by(Investment.date.desc()).all()
    
    return [
        {
            "id": inv.id,
            "category": inv.category,
            "recipient_name": inv.recipient_name,
            "amount": inv.amount,
            "description": inv.description or "",
            "date": inv.date
        }
        for inv in investments
    ]
