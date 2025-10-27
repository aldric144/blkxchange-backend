"""
BlkXchange™ Phase 5A Routes
Monetization + AI Automation System
"""

from fastapi import APIRouter, HTTPException, Header, Request, Depends
from typing import Optional, List, Dict
import secrets
import hashlib
from datetime import datetime, timedelta, date
from app.database import db
from app.models import (
    SubscriptionCreate, Subscription, SubscriptionPlanType,
    PayoutCreate, Payout,
    AffiliateCreate, Affiliate, AffiliateClick, AffiliateConversion,
    AIHistoryCreate, AIHistory, AIHistoryGenerateRequest,
    AIMentorshipCreate, AIMentorship, AIMentorMatchRequest,
    AIContentCreate, AIContent, AIContentGenerateRequest,
    ImpactMetrics,
    PaymentMetadata,
    AdminApprovalRequest,
    SystemHealthCheck,
    StripeWebhookEvent
)
import stripe
import openai
import wikipedia
from slowapi import Limiter
from slowapi.util import get_remote_address
import os
import psutil
import time

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_placeholder")
stripe.api_key = STRIPE_SECRET_KEY

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "changeme")


def verify_admin(x_admin_secret: Optional[str] = Header(None)):
    """Verify admin authentication"""
    if x_admin_secret != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid admin credentials")
    return True

def generate_referral_code(user_id: str) -> str:
    """Generate unique referral code"""
    timestamp = int(time.time())
    raw = f"{user_id}-{timestamp}-{secrets.token_hex(4)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12].upper()


@router.post("/api/payments/subscribe")
@limiter.limit("10/minute")
async def create_subscription(
    request: Request,
    subscription_data: SubscriptionCreate
):
    """
    Create a new subscription (Premium or Elite 360 Membership)
    Test mode: Returns mock subscription without actual Stripe charge
    """
    try:
        plan_amounts = {
            "premium": 29.99,
            "elite": 99.99
        }
        amount = plan_amounts.get(subscription_data.plan_type, 29.99)
        
        mock_customer_id = f"cus_test_{secrets.token_hex(12)}"
        mock_subscription_id = f"sub_test_{secrets.token_hex(12)}"
        
        subscription = db.create_subscription(
            user_id=subscription_data.user_id,
            email=subscription_data.email,
            stripe_customer_id=mock_customer_id,
            stripe_subscription_id=mock_subscription_id,
            plan_type=subscription_data.plan_type,
            amount=amount
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            subscription_data.user_id,
            "subscription_created",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "subscription": subscription,
            "message": f"{subscription_data.plan_type.capitalize()} subscription created successfully",
            "test_mode": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/payments/payouts")
@limiter.limit("5/minute")
async def create_payout(
    request: Request,
    payout_data: PayoutCreate,
    is_admin: bool = Depends(verify_admin)
):
    """
    Create vendor payout (Admin only)
    Test mode: Returns mock payout without actual Stripe transfer
    """
    try:
        vendor = db.get_vendor_by_id(payout_data.vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        
        mock_payout_id = f"po_test_{secrets.token_hex(12)}"
        
        payout = db.create_payout(
            vendor_id=payout_data.vendor_id,
            amount=payout_data.amount,
            stripe_payout_id=mock_payout_id
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            f"vendor_{payout_data.vendor_id}",
            "payout_created",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "payout": payout,
            "message": f"Payout of ${payout_data.amount} created for vendor",
            "test_mode": True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/payments/affiliate")
@limiter.limit("10/minute")
async def create_affiliate(
    request: Request,
    affiliate_data: AffiliateCreate
):
    """
    Create affiliate account with unique referral code and URL
    """
    try:
        existing = db.get_affiliate_by_user_id(affiliate_data.user_id)
        if existing:
            return {
                "success": True,
                "affiliate": existing,
                "message": "Affiliate account already exists"
            }
        
        referral_code = generate_referral_code(affiliate_data.user_id)
        referral_url = f"https://blkxchange.com?ref={referral_code}"
        
        affiliate = db.create_affiliate(
            user_id=affiliate_data.user_id,
            email=affiliate_data.email,
            referral_code=referral_code,
            referral_url=referral_url
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            affiliate_data.user_id,
            "affiliate_created",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "affiliate": affiliate,
            "message": "Affiliate account created successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/payments/affiliate/{user_id}")
async def get_affiliate_stats(user_id: str):
    """Get affiliate statistics and performance metrics"""
    try:
        affiliate = db.get_affiliate_by_user_id(user_id)
        if not affiliate:
            raise HTTPException(status_code=404, detail="Affiliate not found")
        
        conversion_rate = 0.0
        if affiliate.clicks > 0:
            conversion_rate = round((affiliate.conversions / affiliate.clicks) * 100, 2)
        
        return {
            "success": True,
            "affiliate": affiliate,
            "conversion_rate": conversion_rate,
            "avg_order_value": round(affiliate.revenue_generated / affiliate.conversions, 2) if affiliate.conversions > 0 else 0.0
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/payments/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhook events
    In production, verify webhook signature
    """
    try:
        payload = await request.body()
        event = await request.json()
        
        
        event_type = event.get("type")
        
        if event_type == "customer.subscription.created":
            pass
        elif event_type == "customer.subscription.updated":
            pass
        elif event_type == "customer.subscription.deleted":
            pass
        elif event_type == "payment_intent.succeeded":
            pass
        elif event_type == "payment_intent.payment_failed":
            pass
        
        return {"success": True, "event_type": event_type}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/ai/history")
@limiter.limit("5/minute")
async def generate_ai_history(
    request: Request,
    history_request: AIHistoryGenerateRequest
):
    """
    AI History Crawler: Generate Black history content from Wikipedia
    """
    try:
        search_results = wikipedia.search(history_request.topic, results=1)
        
        if not search_results:
            raise HTTPException(status_code=404, detail="No Wikipedia articles found for this topic")
        
        page_title = search_results[0]
        page = wikipedia.page(page_title, auto_suggest=False)
        
        content = page.content[:2000]
        
        image_url = None
        if page.images:
            image_url = page.images[0]
        
        ai_history = db.create_ai_history(
            title=page.title,
            content=content,
            source=page.url,
            category=history_request.category or "general",
            image_url=image_url
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            "system",
            "ai_history_generated",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "ai_history": ai_history,
            "message": "AI history content generated successfully (pending admin approval)"
        }
    
    except wikipedia.exceptions.DisambiguationError as e:
        return {
            "success": False,
            "error": "Multiple topics found. Please be more specific.",
            "options": e.options[:5]
        }
    except wikipedia.exceptions.PageError:
        raise HTTPException(status_code=404, detail="Wikipedia page not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/ai/mentor-match")
@limiter.limit("5/minute")
async def generate_mentor_match(
    request: Request,
    match_request: AIMentorMatchRequest
):
    """
    AI Mentor Engine: Match mentees with mentors using skills and interests
    Uses OpenAI embeddings for semantic matching (mock implementation for MVP)
    """
    try:
        
        mentorship = db.create_ai_mentorship(
            mentee_id=match_request.mentee_id,
            mentee_email=match_request.mentee_email,
            mentee_skills=match_request.mentee_skills,
            mentee_interests=match_request.mentee_interests,
            mentee_industry=match_request.mentee_industry
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            match_request.mentee_id,
            "mentor_match_requested",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "mentorship": mentorship,
            "message": "Mentor match request created successfully (pending admin review)"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/ai/content")
@limiter.limit("5/minute")
async def generate_ai_content(
    request: Request,
    content_request: AIContentGenerateRequest
):
    """
    AI Content Curator: Generate weekly Wealth Hub topics and business insights
    Uses OpenAI GPT for content generation (mock implementation for MVP)
    """
    try:
        
        content_templates = {
            "wealth_hub_topic": {
                "title": f"Building Wealth Through {content_request.topic}",
                "summary": f"Explore strategies for building generational wealth through {content_request.topic}. Learn from successful Black entrepreneurs and financial experts.",
                "full_content": f"This week's Wealth Hub topic focuses on {content_request.topic}. We'll explore proven strategies, real-world examples, and actionable steps you can take today to build lasting wealth in your community."
            },
            "business_insight": {
                "title": f"Business Insight: {content_request.topic}",
                "summary": f"Key insights and trends in {content_request.topic} for Black-owned businesses.",
                "full_content": f"In today's rapidly evolving business landscape, {content_request.topic} presents unique opportunities for Black entrepreneurs. This insight explores current trends, challenges, and strategies for success."
            },
            "community_update": {
                "title": f"Community Update: {content_request.topic}",
                "summary": f"Latest updates and developments in {content_request.topic} affecting our community.",
                "full_content": f"Stay informed about {content_request.topic} and its impact on the Black community. This update covers recent developments, community initiatives, and ways you can get involved."
            }
        }
        
        template = content_templates.get(content_request.content_type, content_templates["wealth_hub_topic"])
        
        ai_content = db.create_ai_content(
            content_type=content_request.content_type,
            title=template["title"],
            summary=template["summary"],
            full_content=template["full_content"],
            tags=[content_request.topic, "ai-generated"],
            target_audience=content_request.target_audience or "all"
        )
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        db.log_audit_event(
            "system",
            "ai_content_generated",
            "success",
            ip_address,
            user_agent
        )
        
        return {
            "success": True,
            "ai_content": ai_content,
            "message": "AI content generated successfully (pending admin approval)"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/ai/history/pending")
async def get_pending_history(is_admin: bool = Depends(verify_admin)):
    """Get all pending AI history content for admin approval"""
    try:
        pending_history = db.get_ai_history_by_status("pending")
        return {
            "success": True,
            "count": len(pending_history),
            "history": pending_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/ai/history/{history_id}/approve")
async def approve_ai_history(
    history_id: str,
    approval: AdminApprovalRequest,
    is_admin: bool = Depends(verify_admin)
):
    """Approve or reject AI-generated history content"""
    try:
        updated_history = db.update_ai_history_status(
            history_id,
            approval.status,
            approval.admin_notes
        )
        
        if not updated_history:
            raise HTTPException(status_code=404, detail="AI history not found")
        
        return {
            "success": True,
            "history": updated_history,
            "message": f"AI history {approval.status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/ai/mentorship/pending")
async def get_pending_mentorship(is_admin: bool = Depends(verify_admin)):
    """Get all pending mentorship matches for admin approval"""
    try:
        pending_matches = db.get_ai_mentorship_by_status("pending")
        return {
            "success": True,
            "count": len(pending_matches),
            "matches": pending_matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/ai/mentorship/{match_id}/approve")
async def approve_mentorship_match(
    match_id: str,
    approval: AdminApprovalRequest,
    is_admin: bool = Depends(verify_admin)
):
    """Approve or reject AI mentorship match"""
    try:
        updated_match = db.update_ai_mentorship_status(
            match_id,
            approval.status,
            approval.admin_notes
        )
        
        if not updated_match:
            raise HTTPException(status_code=404, detail="Mentorship match not found")
        
        return {
            "success": True,
            "match": updated_match,
            "message": f"Mentorship match {approval.status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/ai/content/pending")
async def get_pending_content(is_admin: bool = Depends(verify_admin)):
    """Get all pending AI content for admin approval"""
    try:
        pending_content = db.get_ai_content_by_status("pending")
        return {
            "success": True,
            "count": len(pending_content),
            "content": pending_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/ai/content/{content_id}/approve")
async def approve_ai_content(
    content_id: str,
    approval: AdminApprovalRequest,
    is_admin: bool = Depends(verify_admin)
):
    """Approve or reject AI-generated content"""
    try:
        updated_content = db.update_ai_content_status(
            content_id,
            approval.status,
            approval.admin_notes
        )
        
        if not updated_content:
            raise HTTPException(status_code=404, detail="AI content not found")
        
        return {
            "success": True,
            "content": updated_content,
            "message": f"AI content {approval.status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/impact/metrics")
async def get_impact_metrics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Get aggregated impact metrics for dashboard (MVP version)
    Returns subscriptions, vendors, products, mentorship, and AI content stats
    """
    try:
        if not end_date:
            end_date = date.today().isoformat()
        if not start_date:
            start_date = (date.today() - timedelta(days=30)).isoformat()
        
        metrics = db.get_impact_metrics(start_date, end_date)
        
        return {
            "success": True,
            "metrics": {
                **metrics,
                "date_range": {
                    "start": start_date,
                    "end": end_date
                }
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/impact/export")
async def export_impact_metrics(
    format: str = "csv",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_admin: bool = Depends(verify_admin)
):
    """
    Export impact metrics as CSV or PDF (MVP version)
    Admin only
    """
    try:
        if not end_date:
            end_date = date.today().isoformat()
        if not start_date:
            start_date = (date.today() - timedelta(days=30)).isoformat()
        
        metrics = db.get_impact_metrics(start_date, end_date)
        
        if format == "csv":
            csv_content = "Metric,Value\n"
            csv_content += f"Total Subscriptions,{metrics.get('total_subscriptions', 0)}\n"
            csv_content += f"Total Payouts Amount,{metrics.get('total_payouts_amount', 0)}\n"
            csv_content += f"Total Affiliates,{metrics.get('total_affiliates', 0)}\n"
            csv_content += f"Total Affiliate Earnings,{metrics.get('total_affiliate_earnings', 0)}\n"
            csv_content += f"Approved History Count,{metrics.get('approved_history_count', 0)}\n"
            csv_content += f"Approved Content Count,{metrics.get('approved_content_count', 0)}\n"
            csv_content += f"Total Vendors,{metrics.get('total_vendors', 0)}\n"
            csv_content += f"Total Products,{metrics.get('total_products', 0)}\n"
            csv_content += f"Total Orders,{metrics.get('total_orders', 0)}\n"
            csv_content += f"Community Fund Total,{metrics.get('community_fund_total', 0)}\n"
            
            return {
                "success": True,
                "format": "csv",
                "content": csv_content,
                "filename": f"blkxchange_impact_metrics_{start_date}_to_{end_date}.csv"
            }
        
        elif format == "pdf":
            return {
                "success": True,
                "format": "pdf",
                "message": "PDF export not yet implemented. Use CSV export or frontend PDF generation.",
                "metrics": metrics
            }
        
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'pdf'")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/healthcheck")
async def system_healthcheck():
    """
    System health check endpoint
    Returns memory usage, response time, and database status
    """
    try:
        start_time = time.time()
        
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / 1024 / 1024
        
        db_status = "healthy"
        try:
            _ = db.get_all_vendors()
        except Exception:
            db_status = "unhealthy"
        
        response_time_ms = (time.time() - start_time) * 1000
        
        active_connections = 1
        
        health_check = {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "timestamp": datetime.now().isoformat(),
            "memory_usage_mb": round(memory_usage_mb, 2),
            "avg_response_time_ms": round(response_time_ms, 2),
            "active_connections": active_connections,
            "database_status": db_status
        }
        
        return health_check
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
