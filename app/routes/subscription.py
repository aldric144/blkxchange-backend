from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from app.db_models import get_db
from app.db_models.models import User, Subscription
from app.routes.auth import get_current_user

router = APIRouter()

class SubscriptionUpgradeRequest(BaseModel):
    subscription_type: str  # "Free", "Premium", "Investor"
    stripe_subscription_id: Optional[str] = None

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    subscription_type: str
    start_date: datetime
    end_date: Optional[datetime]
    status: str
    created_at: datetime

@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's subscription status"""
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).order_by(Subscription.created_at.desc()).first()
    
    if not subscription:
        subscription = Subscription(
            user_id=current_user.id,
            subscription_type="Free",
            start_date=datetime.utcnow(),
            status="active"
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    
    return subscription

@router.post("/upgrade", response_model=SubscriptionResponse)
async def upgrade_subscription(
    request: SubscriptionUpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upgrade user subscription"""
    
    valid_types = ["Free", "Premium", "Investor"]
    if request.subscription_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid subscription type. Must be one of: {', '.join(valid_types)}"
        )
    
    current_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if current_subscription:
        current_subscription.status = "inactive"
        current_subscription.end_date = datetime.utcnow()
        db.commit()
    
    end_date = None
    if request.subscription_type in ["Premium", "Investor"]:
        end_date = datetime.utcnow() + timedelta(days=365)
    
    new_subscription = Subscription(
        user_id=current_user.id,
        subscription_type=request.subscription_type,
        start_date=datetime.utcnow(),
        end_date=end_date,
        status="active",
        stripe_subscription_id=request.stripe_subscription_id
    )
    
    db.add(new_subscription)
    
    current_user.membership_tier = request.subscription_type
    
    db.commit()
    db.refresh(new_subscription)
    
    return new_subscription

@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel current subscription (downgrade to Free)"""
    
    current_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if not current_subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    current_subscription.status = "inactive"
    current_subscription.end_date = datetime.utcnow()
    
    free_subscription = Subscription(
        user_id=current_user.id,
        subscription_type="Free",
        start_date=datetime.utcnow(),
        status="active"
    )
    
    db.add(free_subscription)
    
    current_user.membership_tier = "Free"
    
    db.commit()
    
    return {"message": "Subscription cancelled successfully", "new_tier": "Free"}
