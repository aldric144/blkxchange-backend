"""
Phase 5C API Routes
BlkXchange 360™ Community & Events Dashboard
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
from datetime import datetime
from app.database import db
from app.models import (
    Blk360EventCreateEnhanced,
    Blk360PartnerCreate,
    Blk360NonprofitCreate,
    Blk360VolunteerLogCreate,
    Blk360DonationEnhanced
)

router = APIRouter()

ADMIN_SECRET = "changeme"

def verify_admin(x_admin_secret: Optional[str] = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Admin access required")

@router.post("/api/events/create")
async def create_event(event: Blk360EventCreateEnhanced, x_admin_secret: Optional[str] = Header(None)):
    verify_admin(x_admin_secret)
    try:
        new_event = db.create_event_enhanced(
            title=event.title,
            description=event.description,
            category=event.category,
            location=event.location,
            start_time=event.start_time.isoformat(),
            end_time=event.end_time.isoformat(),
            rsvp_limit=event.rsvp_limit,
            ticket_price=event.ticket_price,
            image_url=event.image_url,
            is_volunteer_event=event.is_volunteer_event,
            blkcoin_reward=event.blkcoin_reward
        )
        return {"message": "Event created successfully", "event": new_event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/events")
async def get_events(category: Optional[str] = None, upcoming_only: bool = False):
    try:
        events = db.get_all_events_enhanced(category=category, upcoming_only=upcoming_only)
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/events/{event_id}")
async def get_event(event_id: str):
    event = db.get_event_enhanced(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"event": event}

@router.put("/api/events/{event_id}")
async def update_event(event_id: str, updates: dict, x_admin_secret: Optional[str] = Header(None)):
    verify_admin(x_admin_secret)
    event = db.update_event_enhanced(event_id, updates)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event updated successfully", "event": event}

@router.delete("/api/events/{event_id}")
async def delete_event(event_id: str, x_admin_secret: Optional[str] = Header(None)):
    verify_admin(x_admin_secret)
    success = db.delete_event_enhanced(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}

@router.post("/api/partners/create")
async def create_partner(partner: Blk360PartnerCreate):
    try:
        new_partner = db.create_partner(
            name=partner.name,
            category=partner.category,
            mission=partner.mission,
            website=partner.website,
            contact_name=partner.contact_name,
            contact_email=partner.contact_email,
            contact_phone=partner.contact_phone,
            logo_url=partner.logo_url,
            description=partner.description
        )
        return {"message": "Partner application submitted successfully", "partner": new_partner}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/partners")
async def get_partners(status: Optional[str] = None, category: Optional[str] = None):
    try:
        partners = db.get_all_partners(status=status, category=category)
        return {"partners": partners}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/partners/{partner_id}")
async def get_partner(partner_id: str):
    partner = db.get_partner(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"partner": partner}

@router.put("/api/partners/{partner_id}")
async def update_partner(partner_id: str, updates: dict, x_admin_secret: Optional[str] = Header(None)):
    verify_admin(x_admin_secret)
    partner = db.update_partner(partner_id, updates)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner updated successfully", "partner": partner}

@router.post("/api/nonprofits/create")
async def create_nonprofit(nonprofit: Blk360NonprofitCreate):
    try:
        new_nonprofit = db.create_nonprofit(
            name=nonprofit.name,
            ein=nonprofit.ein,
            focus_area=nonprofit.focus_area,
            mission=nonprofit.mission,
            website=nonprofit.website,
            contact_name=nonprofit.contact_name,
            contact_email=nonprofit.contact_email,
            contact_phone=nonprofit.contact_phone,
            logo_url=nonprofit.logo_url,
            description=nonprofit.description,
            address=nonprofit.address,
            city=nonprofit.city,
            state=nonprofit.state,
            zip_code=nonprofit.zip
        )
        return {"message": "Nonprofit application submitted successfully", "nonprofit": new_nonprofit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/nonprofits")
async def get_nonprofits(status: Optional[str] = None, focus_area: Optional[str] = None):
    try:
        nonprofits = db.get_all_nonprofits(status=status, focus_area=focus_area)
        return {"nonprofits": nonprofits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/nonprofits/{nonprofit_id}")
async def get_nonprofit(nonprofit_id: str):
    nonprofit = db.get_nonprofit(nonprofit_id)
    if not nonprofit:
        raise HTTPException(status_code=404, detail="Nonprofit not found")
    return {"nonprofit": nonprofit}

@router.put("/api/nonprofits/{nonprofit_id}")
async def update_nonprofit(nonprofit_id: str, updates: dict, x_admin_secret: Optional[str] = Header(None)):
    verify_admin(x_admin_secret)
    nonprofit = db.update_nonprofit(nonprofit_id, updates)
    if not nonprofit:
        raise HTTPException(status_code=404, detail="Nonprofit not found")
    return {"message": "Nonprofit updated successfully", "nonprofit": nonprofit}

@router.post("/api/volunteers/log")
async def create_volunteer_log(log: Blk360VolunteerLogCreate):
    try:
        new_log = db.create_volunteer_log(
            user_id=log.user_id,
            event_id=log.event_id,
            hours=log.hours,
            notes=log.notes
        )
        return {"message": "Volunteer hours logged successfully", "log": new_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/volunteers/logs")
async def get_volunteer_logs(user_id: Optional[str] = None, event_id: Optional[str] = None):
    try:
        logs = db.get_volunteer_logs(user_id=user_id, event_id=event_id)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/donations/create")
async def create_donation(donation: Blk360DonationEnhanced):
    try:
        new_donation = db.create_donation_enhanced(
            user_id=donation.user_id,
            recipient_type=donation.recipient_type,
            recipient_id=donation.recipient_id,
            donor_name=donation.donor_name,
            email=donation.email,
            amount=donation.amount,
            is_anonymous=donation.is_anonymous,
            message=donation.message
        )
        return {"message": "Donation processed successfully", "donation": new_donation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/donations")
async def get_donations(recipient_type: Optional[str] = None, recipient_id: Optional[str] = None, user_id: Optional[str] = None):
    try:
        donations = db.get_donations_enhanced(recipient_type=recipient_type, recipient_id=recipient_id, user_id=user_id)
        return {"donations": donations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/impact/metrics/v3")
async def get_impact_metrics_v3(start_date: Optional[str] = None, end_date: Optional[str] = None):
    try:
        if not start_date:
            start_date = "2024-01-01"
        if not end_date:
            end_date = datetime.now().isoformat()
        
        metrics = db.get_impact_metrics_v3(start_date, end_date)
        return {"metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
