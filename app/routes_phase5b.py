"""
Phase 5B Routes: BlkCoin™ Rewards Engine + Scholarship Portal
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
from datetime import datetime
from app.database import db
from app.models import (
    Blk360BlkCoinWallet, Blk360BlkCoinTransaction, Blk360BlkCoinReward,
    BlkCoinEarnRequest, BlkCoinRedeemRequest,
    Blk360Scholarship, Blk360ScholarshipCreate,
    Blk360ScholarshipApplication, Blk360ScholarshipApplicationCreate,
    Blk360ScholarshipDonation, Blk360ScholarshipDonationCreate,
    ScholarshipApprovalRequest,
    ImpactMetricsV2
)
import os

router = APIRouter()

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "changeme")

def verify_admin(x_admin_secret: Optional[str] = Header(None)):
    """Verify admin authentication"""
    if not x_admin_secret or x_admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.post("/api/blkcoin/wallet/create")
def create_blkcoin_wallet(user_id: str, email: str):
    """Create a new BlkCoin wallet for a user"""
    existing_wallet = db.get_blkcoin_wallet(user_id)
    if existing_wallet:
        return existing_wallet
    
    wallet = db.create_blkcoin_wallet(user_id, email)
    return wallet

@router.get("/api/blkcoin/wallet/{user_id}")
def get_blkcoin_wallet(user_id: str):
    """Get BlkCoin wallet by user_id"""
    wallet = db.get_blkcoin_wallet(user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/api/blkcoin/earn")
def earn_blkcoins(request: BlkCoinEarnRequest):
    """Award BlkCoins for completing an activity"""
    wallet = db.get_blkcoin_wallet(request.user_id)
    if not wallet:
        wallet = db.create_blkcoin_wallet(request.user_id, request.metadata.get("email", ""))
    
    reward_amount = db.get_blkcoin_reward_amount(request.activity_type)
    if reward_amount == 0:
        raise HTTPException(status_code=400, detail="Invalid activity type or reward not configured")
    
    updated_wallet = db.update_blkcoin_balance(
        user_id=request.user_id,
        amount=reward_amount,
        transaction_type="earn",
        activity_type=request.activity_type,
        reason=request.reason,
        metadata=request.metadata
    )
    
    if not updated_wallet:
        raise HTTPException(status_code=500, detail="Failed to update wallet")
    
    return {
        "success": True,
        "amount_earned": reward_amount,
        "new_balance": updated_wallet["balance"],
        "wallet": updated_wallet
    }

@router.post("/api/blkcoin/redeem")
def redeem_blkcoins(request: BlkCoinRedeemRequest):
    """Redeem BlkCoins for rewards"""
    wallet = db.get_blkcoin_wallet(request.user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    if wallet["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient BlkCoin balance")
    
    updated_wallet = db.update_blkcoin_balance(
        user_id=request.user_id,
        amount=request.amount,
        transaction_type="redeem",
        activity_type=request.redemption_type,
        reason=request.reason,
        metadata=request.metadata
    )
    
    if not updated_wallet:
        raise HTTPException(status_code=500, detail="Failed to redeem BlkCoins")
    
    return {
        "success": True,
        "amount_redeemed": request.amount,
        "new_balance": updated_wallet["balance"],
        "wallet": updated_wallet
    }

@router.get("/api/blkcoin/transactions/{user_id}")
def get_blkcoin_transactions(user_id: str, limit: int = 50):
    """Get transaction history for a user"""
    transactions = db.get_blkcoin_transactions(user_id, limit)
    return transactions

@router.get("/api/blkcoin/rewards")
def get_blkcoin_rewards():
    """Get all BlkCoin reward rules"""
    rewards = list(db.blk360_blkcoin_rewards.values())
    return rewards

@router.get("/api/admin/blkcoin/wallets")
def get_all_blkcoin_wallets(x_admin_secret: Optional[str] = Header(None)):
    """Admin: Get all BlkCoin wallets"""
    verify_admin(x_admin_secret)
    wallets = list(db.blk360_blkcoin_wallets.values())
    return wallets

@router.post("/api/admin/blkcoin/adjust")
def admin_adjust_blkcoin_balance(
    user_id: str,
    amount: float,
    reason: str,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Manually adjust a user's BlkCoin balance"""
    verify_admin(x_admin_secret)
    
    wallet = db.get_blkcoin_wallet(user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    transaction_type = "earn" if amount > 0 else "redeem"
    updated_wallet = db.update_blkcoin_balance(
        user_id=user_id,
        amount=abs(amount),
        transaction_type=transaction_type,
        activity_type="admin_bonus",
        reason=f"Admin adjustment: {reason}",
        metadata={"admin_action": True}
    )
    
    return {
        "success": True,
        "wallet": updated_wallet
    }


@router.post("/api/scholarships")
def create_scholarship(
    scholarship: Blk360ScholarshipCreate,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Create a new scholarship"""
    verify_admin(x_admin_secret)
    
    new_scholarship = db.create_scholarship(
        title=scholarship.title,
        description=scholarship.description,
        amount=scholarship.amount,
        deadline=scholarship.deadline.isoformat(),
        goal_category=scholarship.goal_category,
        requirements=scholarship.requirements,
        eligibility_criteria=scholarship.eligibility_criteria
    )
    
    return new_scholarship

@router.get("/api/scholarships")
def get_scholarships(status: Optional[str] = None):
    """Get all scholarships, optionally filtered by status"""
    scholarships = db.get_scholarships(status)
    return scholarships

@router.get("/api/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: str):
    """Get a specific scholarship"""
    scholarship = db.get_scholarship(scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship

@router.put("/api/scholarships/{scholarship_id}")
def update_scholarship(
    scholarship_id: str,
    updates: dict,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Update a scholarship"""
    verify_admin(x_admin_secret)
    
    updated_scholarship = db.update_scholarship(scholarship_id, updates)
    if not updated_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    
    return updated_scholarship

@router.post("/api/scholarships/apply")
def apply_for_scholarship(application: Blk360ScholarshipApplicationCreate):
    """Submit a scholarship application"""
    scholarship = db.get_scholarship(application.scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    
    if scholarship["status"] != "open":
        raise HTTPException(status_code=400, detail="Scholarship is not accepting applications")
    
    new_application = db.create_scholarship_application(
        user_id=application.user_id,
        scholarship_id=application.scholarship_id,
        applicant_name=application.applicant_name,
        email=application.email,
        phone=application.phone,
        essay=application.essay,
        goal_category=application.goal_category,
        amount_requested=application.amount_requested,
        additional_info=application.additional_info
    )
    
    wallet = db.get_blkcoin_wallet(application.user_id)
    if wallet:
        db.update_blkcoin_balance(
            user_id=application.user_id,
            amount=15.0,
            transaction_type="earn",
            activity_type="scholarship_application",
            reason=f"Applied for scholarship: {scholarship['title']}",
            metadata={"scholarship_id": application.scholarship_id}
        )
    
    return new_application

@router.get("/api/scholarships/applications")
def get_scholarship_applications(
    scholarship_id: Optional[str] = None,
    status: Optional[str] = None,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Get scholarship applications"""
    verify_admin(x_admin_secret)
    
    applications = db.get_scholarship_applications(scholarship_id, status)
    return applications

@router.get("/api/scholarships/applications/{application_id}")
def get_scholarship_application(
    application_id: str,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Get a specific scholarship application"""
    verify_admin(x_admin_secret)
    
    application = db.get_scholarship_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return application

@router.put("/api/scholarships/applications/{application_id}/review")
def review_scholarship_application(
    application_id: str,
    review: ScholarshipApprovalRequest,
    x_admin_secret: Optional[str] = Header(None)
):
    """Admin: Approve or reject a scholarship application"""
    verify_admin(x_admin_secret)
    
    updated_application = db.update_scholarship_application(
        application_id=application_id,
        status=review.status,
        admin_notes=review.admin_notes,
        reviewed_by="admin",
        award_amount=review.award_amount
    )
    
    if not updated_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return updated_application

@router.post("/api/scholarships/donate")
def donate_to_scholarship(donation: Blk360ScholarshipDonationCreate):
    """Make a donation to a scholarship"""
    scholarship = db.get_scholarship(donation.scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    
    new_donation = db.create_scholarship_donation(
        user_id=donation.user_id,
        scholarship_id=donation.scholarship_id,
        donor_name=donation.donor_name,
        email=donation.email,
        amount=donation.amount,
        is_anonymous=donation.is_anonymous
    )
    
    wallet = db.get_blkcoin_wallet(donation.user_id)
    if wallet:
        blkcoin_reward = (donation.amount // 10) * 20
        if blkcoin_reward > 0:
            db.update_blkcoin_balance(
                user_id=donation.user_id,
                amount=blkcoin_reward,
                transaction_type="earn",
                activity_type="donation",
                reason=f"Donated ${donation.amount} to scholarship: {scholarship['title']}",
                metadata={"scholarship_id": donation.scholarship_id, "donation_amount": donation.amount}
            )
    
    return new_donation

@router.get("/api/scholarships/{scholarship_id}/donations")
def get_scholarship_donations(scholarship_id: str):
    """Get donations for a specific scholarship"""
    donations = db.get_scholarship_donations(scholarship_id)
    return donations


@router.get("/api/impact/metrics/v2")
def get_impact_metrics_v2(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Get comprehensive impact metrics including Phase 5B data"""
    if not start_date:
        start_date = "2024-01-01"
    if not end_date:
        end_date = datetime.now().isoformat()
    
    metrics = db.get_impact_metrics_v2(start_date, end_date)
    return metrics
