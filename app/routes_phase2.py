from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
from app.database import db
from app.models import (
    Blk360Subscription, Blk360SubscriptionCreate,
    Blk360WealthModule, Blk360WealthModuleCreate,
    Blk360LegacyEntry, Blk360LegacyEntryCreate, LegacyEntryStatus,
    Blk360HistoryEntry, Blk360HistoryEntryCreate,
    Blk360ForumPost, Blk360ForumPostCreate,
    Blk360ForumReply, Blk360ForumReplyCreate,
    Blk360AnalyticsMetrics
)

router = APIRouter(prefix="/api/blk360", tags=["BlkXchange 360"])

@router.post("/subscriptions", response_model=Blk360Subscription)
async def create_subscription(subscription: Blk360SubscriptionCreate):
    existing = db.get_blk360_subscription_by_email(subscription.user_email)
    if existing:
        raise HTTPException(status_code=400, detail="User already has an active subscription")
    return db.create_blk360_subscription(subscription)

@router.get("/subscriptions/{email}", response_model=Blk360Subscription)
async def get_subscription(email: str):
    subscription = db.get_blk360_subscription_by_email(email)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.get("/subscriptions", response_model=List[Blk360Subscription])
async def get_all_subscriptions():
    return db.get_all_blk360_subscriptions()

@router.get("/wealth-modules", response_model=List[Blk360WealthModule])
async def get_wealth_modules(published_only: bool = True):
    return db.get_all_blk360_wealth_modules(published_only=published_only)

@router.post("/wealth-modules", response_model=Blk360WealthModule)
async def create_wealth_module(module: Blk360WealthModuleCreate):
    return db.create_blk360_wealth_module(module)

@router.put("/wealth-modules/{module_id}", response_model=Blk360WealthModule)
async def update_wealth_module(module_id: str, module: Blk360WealthModuleCreate):
    updated = db.update_blk360_wealth_module(module_id, module)
    if not updated:
        raise HTTPException(status_code=404, detail="Module not found")
    return updated

@router.delete("/wealth-modules/{module_id}")
async def delete_wealth_module(module_id: str):
    success = db.delete_blk360_wealth_module(module_id)
    if not success:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"message": "Module deleted successfully"}

@router.post("/legacy-entries", response_model=Blk360LegacyEntry)
async def create_legacy_entry(entry: Blk360LegacyEntryCreate):
    return db.create_blk360_legacy_entry(entry)

@router.get("/legacy-entries", response_model=List[Blk360LegacyEntry])
async def get_legacy_entries(status: Optional[LegacyEntryStatus] = None):
    return db.get_all_blk360_legacy_entries(status=status)

@router.put("/legacy-entries/{entry_id}/status")
async def update_legacy_entry_status(entry_id: str, status: LegacyEntryStatus, featured: bool = False):
    updated = db.update_blk360_legacy_entry_status(entry_id, status, featured)
    if not updated:
        raise HTTPException(status_code=404, detail="Entry not found")
    return updated

@router.get("/history-entries", response_model=List[Blk360HistoryEntry])
async def get_history_entries(approved_only: bool = True):
    return db.get_all_blk360_history_entries(approved_only=approved_only)

@router.post("/history-entries", response_model=Blk360HistoryEntry)
async def create_history_entry(entry: Blk360HistoryEntryCreate):
    return db.create_blk360_history_entry(entry)

@router.get("/forum-posts", response_model=List[Blk360ForumPost])
async def get_forum_posts(category: Optional[str] = None):
    from app.models import Forum360Category
    cat = Forum360Category(category) if category else None
    return db.get_all_blk360_forum_posts(category=cat)

@router.get("/forum-posts/{post_id}", response_model=Blk360ForumPost)
async def get_forum_post(post_id: str):
    post = db.get_blk360_forum_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/forum-posts", response_model=Blk360ForumPost)
async def create_forum_post(post: Blk360ForumPostCreate):
    return db.create_blk360_forum_post(post)

@router.get("/forum-posts/{post_id}/replies", response_model=List[Blk360ForumReply])
async def get_forum_replies(post_id: str):
    return db.get_blk360_forum_replies(post_id)

@router.post("/forum-replies", response_model=Blk360ForumReply)
async def create_forum_reply(reply: Blk360ForumReplyCreate):
    return db.create_blk360_forum_reply(reply)

@router.get("/analytics/metrics", response_model=Blk360AnalyticsMetrics)
async def get_360_analytics():
    return db.get_blk360_analytics_metrics()
