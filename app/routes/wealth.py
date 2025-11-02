from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db_models import get_db
from app.db_models.models import WealthModule, WealthProgress, User, Wallet, Transaction
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/wealth", tags=["wealth"])

class WealthModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    content: str
    tier_required: str
    points_reward: int
    duration_minutes: int
    category: str
    order_index: int
    is_locked: bool
    is_completed: bool
    
    class Config:
        from_attributes = True

class WealthProgressResponse(BaseModel):
    id: int
    module_id: int
    completed_at: datetime
    points_earned: int
    
    class Config:
        from_attributes = True

class CompleteModuleRequest(BaseModel):
    module_id: int

@router.get("/modules", response_model=List[WealthModuleResponse])
def get_wealth_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all wealth modules with locked/completed status for current user"""
    modules = db.query(WealthModule).order_by(WealthModule.order_index).all()
    
    completed_module_ids = set(
        progress.module_id 
        for progress in db.query(WealthProgress).filter(
            WealthProgress.user_id == current_user.id
        ).all()
    )
    
    tier_hierarchy = {"Free": 0, "Premium": 1, "Investor": 2}
    user_tier_level = tier_hierarchy.get(current_user.membership_tier, 0)
    
    result = []
    for module in modules:
        module_tier_level = tier_hierarchy.get(module.tier_required, 0)
        is_locked = module_tier_level > user_tier_level
        is_completed = module.id in completed_module_ids
        
        result.append(WealthModuleResponse(
            id=module.id,
            title=module.title,
            description=module.description or "",
            content=module.content or "",
            tier_required=module.tier_required,
            points_reward=module.points_reward,
            duration_minutes=module.duration_minutes or 0,
            category=module.category or "",
            order_index=module.order_index,
            is_locked=is_locked,
            is_completed=is_completed
        ))
    
    return result

@router.get("/progress", response_model=List[WealthProgressResponse])
def get_wealth_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wealth module completion progress"""
    progress = db.query(WealthProgress).filter(
        WealthProgress.user_id == current_user.id
    ).all()
    
    return progress

@router.post("/complete")
def complete_wealth_module(
    request: CompleteModuleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a wealth module as completed and award BlkPoints"""
    module = db.query(WealthModule).filter(WealthModule.id == request.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    tier_hierarchy = {"Free": 0, "Premium": 1, "Investor": 2}
    user_tier_level = tier_hierarchy.get(current_user.membership_tier, 0)
    module_tier_level = tier_hierarchy.get(module.tier_required, 0)
    
    if module_tier_level > user_tier_level:
        raise HTTPException(
            status_code=403, 
            detail=f"This module requires {module.tier_required} tier or higher"
        )
    
    existing_progress = db.query(WealthProgress).filter(
        WealthProgress.user_id == current_user.id,
        WealthProgress.module_id == request.module_id
    ).first()
    
    if existing_progress:
        raise HTTPException(status_code=400, detail="Module already completed")
    
    progress = WealthProgress(
        user_id=current_user.id,
        module_id=request.module_id,
        points_earned=module.points_reward
    )
    db.add(progress)
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if wallet:
        wallet.points_balance += module.points_reward
        wallet.total_earned += module.points_reward
        
        transaction = Transaction(
            user_id=current_user.id,
            transaction_type="earn",
            points=module.points_reward,
            description=f"Completed wealth module: {module.title}",
            reference_id=f"module_{module.id}"
        )
        db.add(transaction)
    
    db.commit()
    
    return {
        "message": "Module completed successfully",
        "points_earned": module.points_reward,
        "new_balance": wallet.points_balance if wallet else 0
    }

@router.get("/stats")
def get_wealth_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wealth learning statistics"""
    total_modules = db.query(WealthModule).count()
    completed_count = db.query(WealthProgress).filter(
        WealthProgress.user_id == current_user.id
    ).count()
    
    total_points_earned = db.query(WealthProgress).filter(
        WealthProgress.user_id == current_user.id
    ).with_entities(WealthProgress.points_earned).all()
    
    total_wealth_points = sum(p[0] for p in total_points_earned)
    
    tier_hierarchy = {"Free": 0, "Premium": 1, "Investor": 2}
    user_tier_level = tier_hierarchy.get(current_user.membership_tier, 0)
    
    next_tier = None
    if user_tier_level == 0:
        next_tier = "Premium"
    elif user_tier_level == 1:
        next_tier = "Investor"
    
    return {
        "total_modules": total_modules,
        "completed_modules": completed_count,
        "completion_percentage": (completed_count / total_modules * 100) if total_modules > 0 else 0,
        "total_wealth_points": total_wealth_points,
        "current_tier": current_user.membership_tier,
        "next_unlock_goal": next_tier
    }
