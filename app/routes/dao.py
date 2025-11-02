from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db_models import get_db
from app.db_models.models import DAOProposal, DAOVote, User, Wallet
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/dao", tags=["dao"])

class ProposalCreate(BaseModel):
    title: str
    summary: str
    description: Optional[str] = None
    category: Optional[str] = None

class ProposalResponse(BaseModel):
    id: int
    user_id: int
    username: str
    title: str
    summary: str
    description: Optional[str]
    category: Optional[str]
    status: str
    votes_for: int
    votes_against: int
    total_points_for: int
    total_points_against: int
    created_at: datetime
    user_has_voted: bool
    user_vote_value: Optional[str]
    
    class Config:
        from_attributes = True

class VoteRequest(BaseModel):
    proposal_id: int
    vote_value: str  # "for" or "against"
    points_to_use: int

@router.get("/proposals", response_model=List[ProposalResponse])
def get_proposals(
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all DAO proposals with optional status filter"""
    query = db.query(DAOProposal)
    
    if status_filter:
        query = query.filter(DAOProposal.status == status_filter)
    
    proposals = query.order_by(DAOProposal.created_at.desc()).all()
    
    user_votes = {
        vote.proposal_id: vote.vote_value
        for vote in db.query(DAOVote).filter(DAOVote.user_id == current_user.id).all()
    }
    
    result = []
    for proposal in proposals:
        creator = db.query(User).filter(User.id == proposal.user_id).first()
        username = creator.username if creator else "Unknown"
        
        user_has_voted = proposal.id in user_votes
        user_vote_value = user_votes.get(proposal.id)
        
        result.append(ProposalResponse(
            id=proposal.id,
            user_id=proposal.user_id,
            username=username,
            title=proposal.title,
            summary=proposal.summary,
            description=proposal.description,
            category=proposal.category,
            status=proposal.status,
            votes_for=proposal.votes_for,
            votes_against=proposal.votes_against,
            total_points_for=proposal.total_points_for,
            total_points_against=proposal.total_points_against,
            created_at=proposal.created_at,
            user_has_voted=user_has_voted,
            user_vote_value=user_vote_value
        ))
    
    return result

@router.post("/propose")
def create_proposal(
    proposal: ProposalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new DAO proposal (Investor tier only)"""
    if current_user.membership_tier != "Investor":
        raise HTTPException(
            status_code=403,
            detail="Only Investor tier members can create proposals"
        )
    
    new_proposal = DAOProposal(
        user_id=current_user.id,
        title=proposal.title,
        summary=proposal.summary,
        description=proposal.description,
        category=proposal.category,
        status="active"
    )
    
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)
    
    return {
        "message": "Proposal created successfully",
        "proposal_id": new_proposal.id,
        "status": new_proposal.status
    }

@router.post("/vote")
def cast_vote(
    vote_request: VoteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cast a vote on a DAO proposal with weighted voting"""
    if vote_request.vote_value not in ["for", "against"]:
        raise HTTPException(status_code=400, detail="Vote value must be 'for' or 'against'")
    
    proposal = db.query(DAOProposal).filter(DAOProposal.id == vote_request.proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if proposal.status != "active":
        raise HTTPException(status_code=400, detail="Proposal is not active for voting")
    
    existing_vote = db.query(DAOVote).filter(
        DAOVote.proposal_id == vote_request.proposal_id,
        DAOVote.user_id == current_user.id
    ).first()
    
    if existing_vote:
        raise HTTPException(status_code=400, detail="You have already voted on this proposal")
    
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet or wallet.points_balance < vote_request.points_to_use:
        raise HTTPException(status_code=400, detail="Insufficient BlkPoints")
    
    tier_weights = {"Free": 1, "Premium": 2, "Investor": 5}
    vote_weight = tier_weights.get(current_user.membership_tier, 1)
    
    total_voting_power = vote_request.points_to_use * vote_weight
    
    vote = DAOVote(
        proposal_id=vote_request.proposal_id,
        user_id=current_user.id,
        vote_value=vote_request.vote_value,
        points_used=vote_request.points_to_use,
        vote_weight=vote_weight
    )
    db.add(vote)
    
    if vote_request.vote_value == "for":
        proposal.votes_for += 1
        proposal.total_points_for += total_voting_power
    else:
        proposal.votes_against += 1
        proposal.total_points_against += total_voting_power
    
    wallet.points_balance -= vote_request.points_to_use
    
    db.commit()
    
    return {
        "message": "Vote cast successfully",
        "vote_value": vote_request.vote_value,
        "points_used": vote_request.points_to_use,
        "vote_weight": vote_weight,
        "total_voting_power": total_voting_power,
        "new_balance": wallet.points_balance
    }

@router.get("/results/{proposal_id}")
def get_proposal_results(
    proposal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed voting results for a proposal"""
    proposal = db.query(DAOProposal).filter(DAOProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    votes = db.query(DAOVote).filter(DAOVote.proposal_id == proposal_id).all()
    
    total_votes = len(votes)
    total_points_used = sum(vote.points_used for vote in votes)
    
    tier_breakdown = {}
    for vote in votes:
        user = db.query(User).filter(User.id == vote.user_id).first()
        if user:
            tier = user.membership_tier
            if tier not in tier_breakdown:
                tier_breakdown[tier] = {"for": 0, "against": 0}
            tier_breakdown[tier][vote.vote_value] += 1
    
    return {
        "proposal_id": proposal.id,
        "title": proposal.title,
        "status": proposal.status,
        "votes_for": proposal.votes_for,
        "votes_against": proposal.votes_against,
        "total_points_for": proposal.total_points_for,
        "total_points_against": proposal.total_points_against,
        "total_votes": total_votes,
        "total_points_used": total_points_used,
        "tier_breakdown": tier_breakdown,
        "for_percentage": (proposal.votes_for / total_votes * 100) if total_votes > 0 else 0,
        "against_percentage": (proposal.votes_against / total_votes * 100) if total_votes > 0 else 0
    }

@router.put("/proposals/{proposal_id}/status")
def update_proposal_status(
    proposal_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update proposal status (proposal creator or admin only)"""
    proposal = db.query(DAOProposal).filter(DAOProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if proposal.user_id != current_user.id and current_user.membership_tier != "Investor":
        raise HTTPException(status_code=403, detail="Not authorized to update this proposal")
    
    valid_statuses = ["active", "passed", "rejected", "pending"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    proposal.status = new_status
    db.commit()
    
    return {
        "message": "Proposal status updated successfully",
        "proposal_id": proposal.id,
        "new_status": new_status
    }
