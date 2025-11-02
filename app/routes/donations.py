from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import os

from app.db_models import get_db
from app.db_models.models import Donation, User, Wallet, Transaction
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/donations", tags=["donations"])

class DonationCreate(BaseModel):
    amount: float
    category: str

class DonationResponse(BaseModel):
    id: int
    amount: float
    category: str
    points_awarded: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/create-checkout")
def create_donation_checkout(
    donation: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe checkout session for donation"""
    if donation.amount < 25 or donation.amount > 250:
        raise HTTPException(
            status_code=400,
            detail="Donation amount must be between $25 and $250"
        )
    
    points_bonus = int(donation.amount * 5)
    
    new_donation = Donation(
        user_id=current_user.id,
        amount=donation.amount,
        category=donation.category,
        points_awarded=points_bonus,
        status="pending"
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    
    
    return {
        "checkout_url": f"https://checkout.stripe.com/mock/{new_donation.id}",
        "donation_id": new_donation.id,
        "amount": donation.amount,
        "points_bonus": points_bonus,
        "message": "Donation checkout created. Complete payment to receive BlkPoints bonus."
    }

@router.post("/webhook")
async def donation_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook for successful donation payments"""
    
    try:
        payload = await request.json()
        donation_id = payload.get("donation_id")
        stripe_payment_id = payload.get("payment_id")
        
        if not donation_id:
            raise HTTPException(status_code=400, detail="Missing donation_id")
        
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found")
        
        donation.status = "completed"
        donation.stripe_payment_id = stripe_payment_id
        
        wallet = db.query(Wallet).filter(Wallet.user_id == donation.user_id).first()
        if wallet:
            wallet.points_balance += donation.points_awarded
            wallet.total_earned += donation.points_awarded
            
            transaction = Transaction(
                user_id=donation.user_id,
                transaction_type="earn",
                points=donation.points_awarded,
                description=f"Donation bonus: ${donation.amount} to {donation.category}",
                reference_id=f"donation_{donation.id}"
            )
            db.add(transaction)
        
        db.commit()
        
        return {
            "message": "Donation processed successfully",
            "points_awarded": donation.points_awarded
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[DonationResponse])
def get_donation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's donation history"""
    donations = db.query(Donation).filter(
        Donation.user_id == current_user.id
    ).order_by(Donation.created_at.desc()).all()
    
    return donations

@router.post("/complete/{donation_id}")
def complete_donation_manual(
    donation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually complete a donation (for testing without Stripe)"""
    donation = db.query(Donation).filter(
        Donation.id == donation_id,
        Donation.user_id == current_user.id
    ).first()
    
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    if donation.status == "completed":
        raise HTTPException(status_code=400, detail="Donation already completed")
    
    donation.status = "completed"
    donation.stripe_payment_id = f"manual_test_{donation_id}"
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if wallet:
        wallet.points_balance += donation.points_awarded
        wallet.total_earned += donation.points_awarded
        
        transaction = Transaction(
            user_id=current_user.id,
            transaction_type="earn",
            points=donation.points_awarded,
            description=f"Donation bonus: ${donation.amount} to {donation.category}",
            reference_id=f"donation_{donation.id}"
        )
        db.add(transaction)
    
    db.commit()
    
    return {
        "message": "Donation completed successfully",
        "points_awarded": donation.points_awarded,
        "new_balance": wallet.points_balance if wallet else 0
    }
