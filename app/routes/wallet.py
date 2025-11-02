from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.db_models import get_db
from app.db_models.models import User, Wallet, Transaction
from app.routes.auth import get_current_user

router = APIRouter()

class WalletResponse(BaseModel):
    id: int
    user_id: int
    points_balance: int
    total_earned: int
    total_redeemed: int
    created_at: datetime
    updated_at: datetime

class EarnPointsRequest(BaseModel):
    points: int
    description: str
    reference_id: Optional[str] = None

class RedeemPointsRequest(BaseModel):
    points: int
    description: str
    reference_id: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    points: int
    description: Optional[str]
    reference_id: Optional[str]
    created_at: datetime

@router.get("", response_model=WalletResponse)
async def get_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wallet balance"""
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    
    if not wallet:
        wallet = Wallet(
            user_id=current_user.id,
            points_balance=0,
            total_earned=0,
            total_redeemed=0
        )
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    
    return wallet

@router.post("/earn", response_model=WalletResponse)
async def earn_points(
    request: EarnPointsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add points to user's wallet"""
    
    if request.points <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Points must be greater than 0"
        )
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(
            user_id=current_user.id,
            points_balance=0,
            total_earned=0,
            total_redeemed=0
        )
        db.add(wallet)
        db.flush()
    
    wallet.points_balance += request.points
    wallet.total_earned += request.points
    wallet.updated_at = datetime.utcnow()
    
    transaction = Transaction(
        user_id=current_user.id,
        transaction_type="earn",
        points=request.points,
        description=request.description,
        reference_id=request.reference_id
    )
    db.add(transaction)
    
    db.commit()
    db.refresh(wallet)
    
    return wallet

@router.post("/redeem", response_model=WalletResponse)
async def redeem_points(
    request: RedeemPointsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Redeem points from user's wallet"""
    
    if request.points <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Points must be greater than 0"
        )
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    if wallet.points_balance < request.points:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient points. Available: {wallet.points_balance}, Required: {request.points}"
        )
    
    wallet.points_balance -= request.points
    wallet.total_redeemed += request.points
    wallet.updated_at = datetime.utcnow()
    
    transaction = Transaction(
        user_id=current_user.id,
        transaction_type="redeem",
        points=request.points,
        description=request.description,
        reference_id=request.reference_id
    )
    db.add(transaction)
    
    db.commit()
    db.refresh(wallet)
    
    return wallet

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get user's transaction history"""
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    return transactions
