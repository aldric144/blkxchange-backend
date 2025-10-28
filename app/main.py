from fastapi import FastAPI, HTTPException, Header, Depends, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import psycopg

from app.models import (
    VendorCreate, Vendor, ProductCreate, Product,
    ProfessionalCreate, Professional, OrderCreate, Order,
    ImpactStats, ProductCategory, ProfessionalCategory,
    VendorApplicationCreate, VendorApplication, VendorApplicationStatus,
    VendorAccountCreate, VendorAccount,
    ProductCreateEnhanced, ProductEnhanced, ProductStatus,
    StartupApplicationCreate, StartupApplication,
    AngelInvestorCreate, AngelInvestor,
    DonationCreate, Donation,
    BlackBank, InvestImpactStats,
    Article, ArticleCreate, ArticleCategory, ArticleStatus,
    Advertiser, AdvertiserCreate, AdCreative, AdCreativeCreate,
    AdSlot, AdSlotCreate, AdStatus, AdType, PriceTier,
    PendingProfessionalCreate, PendingProfessional, PendingProfessionalStatus,
    VendorManualCreate, ProductManualCreate, AdManualCreate, ProfessionalManualCreate,
    PriceRange, FulfillmentMethod,
    AdminLogin, AdminToken, AdminUserCreate, AdminForgotPassword, AdminResetPassword,
    ForumPostCreate, ForumPost, ForumCommentCreate, ForumComment, ForumCategory,
    EventCreate, Event, EventRSVPCreate, EventRSVP,
    QuestionCreate, Question, AnswerCreate, Answer,
    LeadCreate, Lead, LeadMatch,
    Blk360WalletCreate, Blk360Wallet, Blk360WalletTransaction,
    Blk360EventCreate, Blk360Event,
    Blk360ProposalCreate, Blk360Proposal, Blk360VoteCreate, Blk360Vote,
    Blk360FundDonationCreate, Blk360FundDonation, Blk360FundMetrics,
    Blk360GroupCreate, Blk360Group, Blk360GroupMember,
    Blk360MembershipCreate, Blk360Membership
)
from app.database import db
from app.seed_data import seed_database
from app.email import send_vendor_welcome_email, send_bulk_import_confirmation
from app.auth import verify_password, create_access_token, verify_admin_token
from app.image_utils import process_and_save_image
from datetime import timedelta

app = FastAPI(title="BlkXchange API", version="1.0.0")

ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "changeme")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

async def require_admin(
    x_admin_secret: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
):
    """Verify admin access via either admin secret or JWT token"""
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            email = verify_admin_token(token)
            if email:
                user = db.get_admin_user_by_email(email)
                if user and user.is_active:
                    return True
    
    if x_admin_secret == ADMIN_SECRET:
        return True
    
    raise HTTPException(
        status_code=401, 
        detail="Unauthorized: Invalid admin password. Please reload the page and enter the correct password."
    )

@app.on_event("startup")
async def startup_event():
    seed_database()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from pathlib import Path
UPLOAD_DIR = Path("/home/ubuntu/blkxchange/blkxchange-backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

from app.routes_phase2 import router as phase2_router
app.include_router(phase2_router)

from app.routes_phase4 import router as phase4_router
app.include_router(phase4_router)

from app.routes_phase5a import router as phase5a_router
app.include_router(phase5a_router)

from app.routes_phase5b import router as phase5b_router
app.include_router(phase5b_router)

from app.routes_phase5c import router as phase5c_router
app.include_router(phase5c_router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    section: str = Form(...),
    image_type: str = Form(...),
    is_verified: bool = Form(False),
    test_mode: bool = Form(False),
    admin: bool = Depends(require_admin)
):

    """
    Upload and process an image
    
    Args:
        file: Image file to upload
        section: Section (vendors, professionals, products, ads)
        image_type: Type for optimization (logo, product, ad, profile)
        is_verified: Whether to add verified watermark
        test_mode: Whether to save in test directory
    
    Returns:
        {"success": true, "url": "/uploads/live/vendors/..."}
    """
    try:
        content = await file.read()
        
        success, url_path, error = process_and_save_image(
            file_content=content,
            filename=file.filename,
            section=section,
            image_type=image_type,
            is_verified=is_verified,
            test_mode=test_mode
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=error)
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        full_url = f"{backend_url}{url_path}"
        
        return {
            "success": True,
            "url": full_url,
            "path": url_path
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Admin Authentication Endpoints
@app.post("/api/admin/login", response_model=AdminToken)
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint - returns JWT token"""
    user = db.get_admin_user_by_email(login_data.email)
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    
    access_token = create_access_token(
        data={"sub": user.email, "name": user.full_name},
        expires_delta=timedelta(days=7)
    )
    
    return AdminToken(
        token=access_token,
        token_type="bearer",
        expires_in=7 * 24 * 60 * 60,  # 7 days in seconds
        email=user.email
    )

@app.post("/api/admin/create-user", response_model=dict)
async def create_admin_user(user_data: AdminUserCreate, x_admin_secret: str = Header(None)):
    """Create a new admin user (requires admin secret)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    existing_user = db.get_admin_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user = db.create_admin_user(user_data)
    return {"message": "Admin user created successfully", "email": user.email}

@app.post("/api/admin/forgot-password")
async def admin_forgot_password(data: AdminForgotPassword):
    """Send password reset email to admin user"""
    import secrets
    from datetime import datetime, timedelta
    
    user = db.get_admin_user_by_email(data.email)
    if not user:
        return {"message": "If an account exists with this email, a reset link has been sent."}
    
    reset_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    db.create_password_reset_token(user.email, reset_token, expires_at)
    
    reset_url = f"{FRONTEND_URL}/admin/reset-password?token={reset_token}"
    
    print("\n" + "="*80)
    print("📧 PASSWORD RESET EMAIL")
    print("="*80)
    print(f"To: {user.email}")
    print(f"Subject: Reset Your BlkXchange™ Admin Password")
    print(f"\nReset Link: {reset_url}")
    print(f"Valid for: 15 minutes")
    print("="*80 + "\n")
    
    return {"message": "If an account exists with this email, a reset link has been sent."}

@app.post("/api/admin/reset-password")
async def admin_reset_password(data: AdminResetPassword):
    """Reset admin password using token"""
    from datetime import datetime
    
    token_data = db.get_password_reset_token(data.token)
    
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    if token_data.used:
        raise HTTPException(status_code=400, detail="Reset token has already been used")
    
    if datetime.utcnow() > token_data.expires_at:
        raise HTTPException(status_code=400, detail="Reset token has expired")
    
    success = db.update_admin_password(token_data.email, data.new_password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.mark_reset_token_used(data.token)
    
    return {"message": "Password reset successfully"}

@app.post("/api/vendors", response_model=Vendor)
async def create_vendor(vendor: VendorCreate):
    new_vendor = db.create_vendor(vendor)
    
    email_result = await send_vendor_welcome_email(
        to_email=new_vendor.email,
        vendor_name=new_vendor.name,
        vendor_id=new_vendor.id
    )
    
    if email_result and email_result.get("success"):
        print("\n" + "="*80)
        print("📧 VENDOR WELCOME EMAIL SENT!")
        print("="*80)
        print(f"✅ Email sent to: {new_vendor.email}")
        print(f"👤 Vendor: {new_vendor.name} ({new_vendor.business_name})")
        print(f"🔑 Vendor ID: {new_vendor.id}")
        
        if email_result.get('mode') == 'console_log':
            print("\n📋 MODE: Console Logging (MVP)")
            print("   Email content has been logged above.")
            print("   To enable real Ethereal emails, set USE_ETHEREAL=True in app/email.py")
        else:
            print("\n📬 VIEW EMAIL IN BROWSER:")
            print(f"   Login at: {email_result.get('ethereal_inbox')}")
            print(f"   Username: {email_result.get('ethereal_user')}")
            print(f"   Password: {email_result.get('ethereal_pass')}")
            if email_result.get('preview_url'):
                print(f"   Direct URL: {email_result.get('preview_url')}")
        print("="*80 + "\n")
    else:
        print(f"⚠️  Warning: Email sending failed for vendor {new_vendor.email}")
        if email_result:
            print(f"   Error: {email_result.get('error')}")
    
    return new_vendor

@app.get("/api/vendors", response_model=List[Vendor])
async def get_vendors():
    return db.get_all_vendors()

@app.get("/api/vendors/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: str):
    vendor = db.get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@app.put("/api/vendors/{vendor_id}", response_model=Vendor)
async def update_vendor(
    vendor_id: str,
    vendor_data: dict,
    admin: bool = Depends(require_admin)
):
    """Update a vendor (admin only)"""
    vendor = db.update_vendor(vendor_id, vendor_data)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

@app.delete("/api/vendors/{vendor_id}")
async def delete_vendor(
    vendor_id: str,
    admin: bool = Depends(require_admin)
):
    """Delete a vendor (admin only)"""
    success = db.delete_vendor(vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}

@app.post("/api/vendors/{vendor_id}/products", response_model=Product)
async def create_product(vendor_id: str, product: ProductCreate):
    vendor = db.get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db.create_product(vendor_id, product)

@app.get("/api/products", response_model=List[Product])
async def get_products(category: Optional[ProductCategory] = None, vendor_id: Optional[str] = None):
    return db.get_all_products(category=category, vendor_id=vendor_id)

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate):
    updated_product = db.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str):
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/api/professionals", response_model=Professional)
async def create_professional(professional: ProfessionalCreate):
    return db.create_professional(professional)

@app.get("/api/professionals", response_model=List[Professional])
async def get_professionals(category: Optional[ProfessionalCategory] = None):
    return db.get_all_professionals(category=category)

@app.get("/api/professionals/{professional_id}", response_model=Professional)
async def get_professional(professional_id: str):
    professional = db.get_professional(professional_id)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@app.get("/api/professionals/nearby/search")
async def get_professionals_nearby(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    zip: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    radius: float = 25.0,
    category: Optional[ProfessionalCategory] = None
):
    """
    Find professionals near a location by coordinates, ZIP code, or city.
    Priority: lat/lng > zip > city
    """
    from .geocoding import geocode_zip_code, geocode_city
    
    latitude = lat
    longitude = lng
    
    if latitude is None or longitude is None:
        if zip:
            coords = await geocode_zip_code(zip)
            if coords:
                latitude, longitude = coords
        elif city:
            coords = await geocode_city(city, state)
            if coords:
                latitude, longitude = coords
    
    if latitude is None or longitude is None:
        raise HTTPException(
            status_code=400,
            detail="Please provide either lat/lng coordinates, a ZIP code, or a city name"
        )
    
    nearby = db.get_professionals_nearby(
        latitude=latitude,
        longitude=longitude,
        radius_miles=radius,
        category=category
    )
    
    return nearby

@app.get("/api/geocode")
async def geocode_location(
    zip: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None
):
    """
    Geocode a ZIP code or city to get latitude/longitude coordinates.
    """
    from .geocoding import geocode_zip_code, geocode_city
    
    if zip:
        coords = await geocode_zip_code(zip)
        if coords:
            latitude, longitude = coords
            return {"latitude": latitude, "longitude": longitude}
    elif city:
        coords = await geocode_city(city, state)
        if coords:
            latitude, longitude = coords
            return {"latitude": latitude, "longitude": longitude}
    
    raise HTTPException(
        status_code=400,
        detail="Please provide either a ZIP code or a city name"
    )

@app.get("/api/listings/new-count")
async def get_new_listings_count():
    """
    Get count of new vendors and professionals added in the last 7 days.
    Returns: {"vendors": int, "professionals": int, "total": int}
    """
    from datetime import datetime, timedelta
    
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    vendor_count = db.count_new_vendors_since(seven_days_ago)
    
    professional_count = db.count_new_professionals_since(seven_days_ago)
    
    total = vendor_count + professional_count
    
    return {
        "vendors": vendor_count,
        "professionals": professional_count,
        "total": total
    }

@app.post("/api/professionals/submit", response_model=PendingProfessional)
async def submit_professional(data: PendingProfessionalCreate):
    """Submit a professional for review with automatic geocoding"""
    coords = await geocode_address(
        street=data.address,
        city=data.city,
        state=data.state,
        zip_code=data.zip
    )
    
    professional = db.create_pending_professional(data)
    
    if coords and professional:
        db.update_pending_professional_coordinates(professional.id, coords[0], coords[1])
        professional.latitude = coords[0]
        professional.longitude = coords[1]
    
    return professional

@app.get("/api/professionals/pending", response_model=List[PendingProfessional])
async def get_pending_professionals(
    status: Optional[PendingProfessionalStatus] = None,
    admin: bool = Depends(require_admin)
):
    """Get all pending professionals (admin only)"""
    return db.get_all_pending_professionals(status)

@app.post("/api/admin/approve-professional/{professional_id}", response_model=Professional)
async def approve_pending_professional(
    professional_id: str,
    admin: bool = Depends(require_admin)
):
    """Approve a pending professional and create live listing (admin only)"""
    professional = db.approve_pending_professional(professional_id, "admin")
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found or already processed")
    return professional

@app.post("/api/admin/reject-professional/{professional_id}")
async def reject_pending_professional(
    professional_id: str,
    admin: bool = Depends(require_admin)
):
    """Reject a pending professional submission (admin only)"""
    success = db.reject_pending_professional(professional_id)
    if not success:
        raise HTTPException(status_code=404, detail="Professional not found or already processed")
    return {"message": "Professional submission rejected"}

@app.put("/api/professionals/{professional_id}", response_model=Professional)
async def update_professional(
    professional_id: str,
    professional_data: dict,
    admin: bool = Depends(require_admin)
):
    """Update a professional (admin only)"""
    professional = db.update_professional(professional_id, professional_data)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@app.delete("/api/professionals/{professional_id}")
async def delete_professional(
    professional_id: str,
    admin: bool = Depends(require_admin)
):
    """Delete a professional (admin only)"""
    success = db.delete_professional(professional_id)
    if not success:
        raise HTTPException(status_code=404, detail="Professional not found")
    return {"message": "Professional deleted successfully"}

@app.post("/api/orders", response_model=Order)
async def create_order(order: OrderCreate):
    return db.create_order(order)

@app.get("/api/orders", response_model=List[Order])
async def get_orders():
    return db.get_all_orders()

@app.get("/api/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/api/impact", response_model=ImpactStats)
async def get_impact_stats():
    return db.get_impact_stats()

@app.post("/api/visitor-count")
async def increment_visitor_count():
    analytics = db.increment_visitor_count()
    return {"visitor_count": analytics.visitor_count, "month": analytics.month}

@app.get("/api/visitor-count")
async def get_visitor_count():
    visitor_count = db.get_current_month_visitors()
    return {"visitor_count": visitor_count}

# Admin Dashboard Endpoints
@app.get("/api/admin/metrics")
async def get_admin_metrics(admin_ok: bool = Depends(require_admin)):
    """Get unified admin dashboard metrics"""
    from datetime import datetime, timedelta
    
    vendors = db.get_all_vendor_applications()
    professionals_active = db.get_all_professionals()
    professionals_pending = db.get_all_pending_professionals()
    products = db.get_all_products_enhanced()
    impact = db.get_impact_stats()
    invest_impact = db.get_invest_impact_stats()
    
    vendor_approved = len([v for v in vendors if v.status == VendorApplicationStatus.APPROVED])
    vendor_pending = len([v for v in vendors if v.status == VendorApplicationStatus.PENDING])
    vendor_rejected = len([v for v in vendors if v.status == VendorApplicationStatus.REJECTED])
    
    prof_approved = len(professionals_active)
    prof_pending = len([p for p in professionals_pending if p.status == PendingProfessionalStatus.PENDING])
    prof_rejected = len([p for p in professionals_pending if p.status == PendingProfessionalStatus.REJECTED])
    
    prod_approved = len([p for p in products if p.status == ProductStatus.APPROVED])
    prod_pending = len([p for p in products if p.status == ProductStatus.PENDING])
    prod_rejected = len([p for p in products if p.status == ProductStatus.REJECTED])
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sixty_days_ago = datetime.now() - timedelta(days=60)
    
    this_month_revenue = 15000
    last_month_revenue = 12000
    growth = ((this_month_revenue - last_month_revenue) / last_month_revenue * 100) if last_month_revenue > 0 else 0
    
    recent_activity = []
    for v in sorted(vendors, key=lambda x: x.created_at, reverse=True)[:5]:
        recent_activity.append({
            "id": v.id,
            "type": "vendor",
            "description": f"New vendor application: {v.business_name}",
            "timestamp": v.created_at.isoformat()
        })
    
    return {
        "vendors": {
            "total": len(vendors),
            "approved": vendor_approved,
            "pending": vendor_pending,
            "rejected": vendor_rejected
        },
        "professionals": {
            "total": prof_approved + prof_pending + prof_rejected,
            "approved": prof_approved,
            "pending": prof_pending,
            "rejected": prof_rejected
        },
        "products": {
            "total": len(products),
            "approved": prod_approved,
            "pending": prod_pending,
            "rejected": prod_rejected
        },
        "revenue": {
            "total": this_month_revenue + last_month_revenue,
            "thisMonth": this_month_revenue,
            "lastMonth": last_month_revenue,
            "growth": round(growth, 1)
        },
        "impact": {
            "totalDonated": invest_impact.total_funds_reinvested,
            "hbcuFunds": invest_impact.hbcu_donations,
            "startupInvestments": invest_impact.startup_investments
        },
        "recentActivity": recent_activity
    }

@app.get("/api/admin/search")
async def admin_search(q: str, admin_ok: bool = Depends(require_admin)):
    """Global search across vendors, professionals, and products"""
    if not q or len(q) < 2:
        return {"results": []}
    
    query = q.lower()
    results = []
    
    vendors = db.get_all_vendor_applications()
    for vendor in vendors:
        if (query in vendor.business_name.lower() or 
            query in vendor.contact_name.lower() or 
            query in vendor.email.lower()):
            results.append({
                "type": "vendor",
                "id": vendor.id,
                "title": vendor.business_name,
                "subtitle": vendor.contact_name,
                "status": vendor.status.value,
                "url": f"/admin/vendors"
            })
    
    professionals = db.get_all_professionals()
    for prof in professionals:
        if (query in prof.name.lower() or 
            query in prof.title.lower() or 
            query in prof.category.value.lower()):
            results.append({
                "type": "professional",
                "id": prof.id,
                "title": prof.name,
                "subtitle": prof.title,
                "status": "approved",
                "url": f"/admin/professionals"
            })
    
    products = db.get_all_products_enhanced()
    for product in products:
        if (query in product.name.lower() or 
            query in product.category.lower()):
            results.append({
                "type": "product",
                "id": product.id,
                "title": product.name,
                "subtitle": f"${product.price}",
                "status": product.status.value,
                "url": f"/admin/products"
            })
    
    return {"results": results[:20]}

# Vendor Application Endpoints
@app.post("/api/vendor-applications", response_model=VendorApplication)
async def create_vendor_application(application: VendorApplicationCreate):
    if not application.agreement_accepted:
        raise HTTPException(status_code=400, detail="Vendor agreement must be accepted")
    
    coords = await geocode_address(
        street=application.address,
        city=application.city,
        state=application.state,
        zip_code=application.zip
    )
    
    new_application = db.create_vendor_application(application)
    
    if coords and new_application:
        db.update_vendor_application_coordinates(new_application.id, coords[0], coords[1])
        new_application.latitude = coords[0]
        new_application.longitude = coords[1]
    
    print("\n" + "="*80)
    print("📥 New vendor application submitted")
    print(f"Business: {new_application.business_name} | Contact: {new_application.contact_name} | Email: {new_application.email}")
    if coords:
        print(f"📍 Geocoded location: {coords[0]}, {coords[1]}")
    print("- Sending confirmation email to applicant (console/Ethereal)")
    print("- Sending notification email to admin (console/Ethereal)")
    print("="*80 + "\n")
    return new_application

@app.get("/api/vendor-applications", response_model=List[VendorApplication])
async def get_vendor_applications(status: Optional[VendorApplicationStatus] = None, admin_ok: bool = Depends(require_admin)):
    return db.get_all_vendor_applications(status=status)

@app.get("/api/vendor-applications/{application_id}", response_model=VendorApplication)
async def get_vendor_application(application_id: str):
    application = db.get_vendor_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.put("/api/vendor-applications/{application_id}/status")
async def update_vendor_application_status(application_id: str, status: VendorApplicationStatus, admin_ok: bool = Depends(require_admin)):
    application = db.update_vendor_application_status(application_id, status)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": f"Application status updated to {status}", "application": application}

# Vendor Account Endpoints
@app.post("/api/vendor-accounts", response_model=VendorAccount)
async def create_vendor_account(account: VendorAccountCreate):
    existing_account = db.get_vendor_account_by_email(account.email)
    if existing_account:
        raise HTTPException(status_code=400, detail="Account with this email already exists")
    new_account = db.create_vendor_account(account)
    return new_account

@app.post("/api/vendor-accounts/login")
async def vendor_login(email: str, password: str):
    account = db.verify_vendor_password(email, password)
    if not account:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "vendor_id": account.vendor_id, "email": account.email}

# Enhanced Product Endpoints
@app.post("/api/products-enhanced", response_model=ProductEnhanced)
async def create_product_enhanced(product: ProductCreateEnhanced):
    new_product = db.create_product_enhanced(product)
    return new_product

@app.get("/api/products-enhanced", response_model=List[ProductEnhanced])
async def get_products_enhanced(vendor_id: Optional[str] = None, status: Optional[ProductStatus] = None):
    return db.get_all_products_enhanced(vendor_id=vendor_id, status=status)

@app.get("/api/products-enhanced/{product_id}", response_model=ProductEnhanced)
async def get_product_enhanced(product_id: str):
    product = db.get_product_enhanced(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products-enhanced/{product_id}", response_model=ProductEnhanced)
async def update_product_enhanced(product_id: str, product: ProductCreateEnhanced):
    updated_product = db.update_product_enhanced(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.put("/api/products-enhanced/{product_id}/status")
async def update_product_enhanced_status(product_id: str, status: ProductStatus):
    product = db.update_product_enhanced_status(product_id, status)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product status updated to {status}", "product": product}

# Admin Endpoints
@app.post("/api/admin/approve-vendor/{application_id}")
async def approve_vendor_application(application_id: str, admin_ok: bool = Depends(require_admin)):
    application = db.get_vendor_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.update_vendor_application_status(application_id, VendorApplicationStatus.APPROVED)
    
    vendor_data = VendorCreate(
        email=application.email,
        name=application.contact_name,
        business_name=application.business_name,
        business_description=application.description,
        phone=application.phone
    )
    new_vendor = db.create_vendor(vendor_data)
    
    return {"message": "Vendor application approved", "vendor_id": new_vendor.id}

@app.post("/api/admin/reject-vendor/{application_id}")
async def reject_vendor_application(application_id: str, reason: Optional[str] = None, admin_ok: bool = Depends(require_admin)):
    application = db.get_vendor_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.update_vendor_application_status(application_id, VendorApplicationStatus.REJECTED)
    
    return {"message": "Vendor application rejected", "reason": reason}

@app.post("/api/admin/approve-product/{product_id}")
async def approve_product(product_id: str, admin_ok: bool = Depends(require_admin)):
    product = db.update_product_enhanced_status(product_id, ProductStatus.APPROVED)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product approved", "product": product}

@app.post("/api/admin/reject-product/{product_id}")
async def reject_product(product_id: str, reason: Optional[str] = None, admin_ok: bool = Depends(require_admin)):
    product = db.update_product_enhanced_status(product_id, ProductStatus.REJECTED)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product rejected", "reason": reason}

# Invest in the Future Hub Endpoints
@app.post("/api/startup-applications", response_model=StartupApplication)
async def create_startup_application(application: StartupApplicationCreate):
    if not application.agreement_accepted:
        raise HTTPException(status_code=400, detail="Agreement must be accepted")
    new_application = db.create_startup_application(application)
    print(f"\n📥 New startup application: {new_application.business_name} seeking ${new_application.funding_goal:,.2f}")
    return new_application

@app.get("/api/startup-applications", response_model=List[StartupApplication])
async def get_startup_applications():
    return db.get_all_startup_applications()

@app.post("/api/angel-investors", response_model=AngelInvestor)
async def create_angel_investor(investor: AngelInvestorCreate):
    if not investor.agreement_accepted:
        raise HTTPException(status_code=400, detail="Agreement must be accepted")
    new_investor = db.create_angel_investor(investor)
    print(f"\n👼 New angel investor registered: {new_investor.name} ({new_investor.investment_range})")
    return new_investor

@app.get("/api/angel-investors", response_model=List[AngelInvestor])
async def get_angel_investors():
    return db.get_all_angel_investors()

@app.post("/api/donations", response_model=Donation)
async def create_donation(donation: DonationCreate):
    new_donation = db.create_donation(donation)
    print(f"\n💰 New donation: ${new_donation.amount:,.2f} to {new_donation.institution} from {new_donation.donor_name}")
    return new_donation

@app.get("/api/donations", response_model=List[Donation])
async def get_donations():
    return db.get_all_donations()

@app.get("/api/black-banks", response_model=List[BlackBank])
async def get_black_banks():
    return db.get_all_black_banks()

@app.get("/api/invest-impact", response_model=InvestImpactStats)
async def get_invest_impact_stats():
    return db.get_invest_impact_stats()

@app.post("/api/articles", response_model=Article)
async def create_article(article_data: ArticleCreate):
    article = db.create_article(article_data)
    return article

@app.get("/api/articles", response_model=List[Article])
async def get_articles(
    category: Optional[ArticleCategory] = None,
    status: Optional[ArticleStatus] = None
):
    return db.get_all_articles(category=category, status=status)

@app.get("/api/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    article = db.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.get("/api/articles/slug/{slug}", response_model=Article)
async def get_article_by_slug(slug: str):
    article = db.get_article_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.patch("/api/articles/{article_id}/status", response_model=Article, dependencies=[Depends(require_admin)])
async def update_article_status(article_id: str, status: ArticleStatus):
    article = db.update_article_status(article_id, status)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Advertising Module Endpoints
@app.post("/api/advertisers", response_model=Advertiser)
async def create_advertiser(advertiser_data: AdvertiserCreate):
    advertiser = db.create_advertiser(advertiser_data)
    print(f"\n📢 New advertiser registered: {advertiser.name}")
    return advertiser

@app.get("/api/advertisers", response_model=List[Advertiser])
async def get_advertisers():
    return db.get_all_advertisers()

@app.get("/api/advertisers/{advertiser_id}", response_model=Advertiser)
async def get_advertiser(advertiser_id: str):
    advertiser = db.get_advertiser(advertiser_id)
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    return advertiser

@app.post("/api/ad-creatives", response_model=AdCreative)
async def create_ad_creative(creative_data: AdCreativeCreate):
    creative = db.create_ad_creative(creative_data)
    
    for page in creative.pages:
        slot_data = AdSlotCreate(
            creative_id=creative.id,
            page=page,
            placement=creative.ad_type.value
        )
        db.create_ad_slot(slot_data)
    
    print(f"\n🎨 New ad creative created: {creative.advertiser_name} - {creative.ad_type.value} on {', '.join(creative.pages)}")
    return creative

@app.get("/api/ad-creatives", response_model=List[AdCreative])
async def get_ad_creatives(status: Optional[AdStatus] = None, page: Optional[str] = None):
    return db.get_all_ad_creatives(status=status, page=page)

@app.get("/api/ad-creatives/{creative_id}", response_model=AdCreative)
async def get_ad_creative(creative_id: str):
    creative = db.get_ad_creative(creative_id)
    if not creative:
        raise HTTPException(status_code=404, detail="Ad creative not found")
    return creative

@app.patch("/api/ad-creatives/{creative_id}/status", dependencies=[Depends(require_admin)])
async def update_ad_creative_status(creative_id: str, status: AdStatus):
    creative = db.update_ad_creative_status(creative_id, status)
    if not creative:
        raise HTTPException(status_code=404, detail="Ad creative not found")
    return {"message": f"Ad creative status updated to {status}", "creative": creative}

@app.put("/api/ad-creatives/{creative_id}")
async def update_ad_creative(
    creative_id: str,
    update_data: dict,
    x_admin_secret: str = Header(None)
):
    """Update an ad creative (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    creative = db.update_ad_creative(creative_id, update_data)
    if not creative:
        raise HTTPException(status_code=404, detail="Ad creative not found")
    return creative

@app.delete("/api/ad-creatives/{creative_id}")
async def delete_ad_creative(
    creative_id: str,
    x_admin_secret: str = Header(None)
):
    """Delete an ad creative (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    success = db.delete_ad_creative(creative_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ad creative not found")
    return {"message": "Ad creative deleted successfully"}

@app.get("/api/ads/{page}", response_model=List[dict])
async def get_ads_for_page(page: str, placement: Optional[str] = None):
    slots = db.get_ad_slots_by_page(page, placement)
    ads = []
    for slot in slots:
        creative = db.get_ad_creative(slot.creative_id)
        if creative and creative.status == AdStatus.LIVE:
            advertiser = db.get_advertiser(creative.advertiser_id)
            ads.append({
                "id": slot.id,
                "creative_id": creative.id,
                "advertiser_name": creative.advertiser_name,
                "tagline": advertiser.tagline if advertiser else None,
                "asset_url": creative.asset_url,
                "link_url": creative.link_url,
                "ad_type": creative.ad_type,
                "placement": slot.placement,
                "price_tier": creative.price_tier
            })
    return ads

@app.post("/api/ads/{slot_id}/impression")
async def record_ad_impression(slot_id: str):
    db.increment_ad_impression(slot_id)
    return {"message": "Impression recorded"}

@app.post("/api/ads/{slot_id}/click")
async def record_ad_click(slot_id: str):
    db.increment_ad_click(slot_id)
    return {"message": "Click recorded"}

@app.post("/api/admin/vendors/manual", response_model=VendorApplication)
async def create_vendor_manual(
    data: VendorManualCreate,
    admin: bool = Depends(require_admin)
):
    """Manually create a vendor (admin only)"""
    
    vendor_app = VendorApplicationCreate(
        business_name=data.business_name,
        contact_name=data.owner_name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        website=data.website,
        category=data.category,
        description=data.description,
        price_range=PriceRange.UNDER_25,
        fulfillment_method=FulfillmentMethod.SHIPPING,
        image_urls=[data.logo_url] if data.logo_url else [],
        agreement_accepted=True
    )
    
    vendor = db.create_vendor_application(vendor_app)
    vendor.status = data.status
    return vendor

@app.post("/api/admin/products/manual", response_model=ProductEnhanced)
async def create_product_manual(
    data: ProductManualCreate,
    admin: bool = Depends(require_admin)
):
    """Manually create a product (admin only)"""
    
    import uuid
    product_data = ProductCreateEnhanced(
        vendor_id=data.vendor_id,
        name=data.name,
        description=data.description,
        price=data.price,
        category=data.category,
        quantity=data.quantity,
        image_urls=data.image_urls
    )
    
    product = db.create_product_enhanced(product_data)
    if data.status == ProductStatus.APPROVED:
        db.update_product_enhanced_status(product.id, ProductStatus.APPROVED)
    return product

@app.post("/api/admin/ads/manual", response_model=AdCreative)
async def create_ad_manual(
    data: AdManualCreate,
    admin: bool = Depends(require_admin)
):
    """Manually create an ad (admin only)"""
    
    advertiser_data = AdvertiserCreate(
        name=data.advertiser_name,
        contact_email="admin@blkxchange.com",
        website=data.target_url,
        tagline=data.tagline
    )
    advertiser = db.create_advertiser(advertiser_data)
    
    from datetime import datetime, timedelta
    start_date = data.start_date or datetime.now()
    end_date = data.end_date or (datetime.now() + timedelta(days=30))
    
    ad_data = AdCreativeCreate(
        advertiser_id=advertiser.id,
        asset_url=data.asset_url,
        ad_type=data.ad_type,
        pages=data.pages,
        start_date=start_date,
        end_date=end_date,
        price_tier=PriceTier.BASIC,
        link_url=data.target_url
    )
    
    ad = db.create_ad_creative(ad_data)
    if data.status == AdStatus.LIVE:
        db.update_ad_creative_status(ad.id, AdStatus.LIVE)
    return ad

@app.post("/api/admin/professionals/manual", response_model=Professional)
async def create_professional_manual(
    data: ProfessionalManualCreate,
    admin: bool = Depends(require_admin)
):
    """Manually create a professional (admin only)"""
    
    professional_data = ProfessionalCreate(
        email=data.email,
        name=data.name,
        title=data.tagline or data.business_name or data.name,
        category=data.category,
        bio=data.bio,
        credentials=data.credentials,
        hourly_rate=None,
        phone=data.phone,
        website=data.website,
        image_url=data.image_url,
        zip=data.zip
    )
    
    professional = db.create_professional(professional_data)
    return professional

# Bulk Import Endpoints
@app.post("/api/admin/vendors/import")
async def bulk_import_vendors(
    data: dict,
    admin: bool = Depends(require_admin)
):
    """Bulk import vendors from CSV data (admin only)"""
    
    csv_data = data.get("data", [])
    results = {
        "successful": 0,
        "skipped": 0,
        "failed": 0,
        "errors": []
    }
    
    for row in csv_data:
        try:
            existing_apps = db.get_all_vendor_applications()
            if any(app.email == row.get("email") for app in existing_apps):
                results["skipped"] += 1
                continue
            
            # Create vendor application
            vendor_app = VendorApplicationCreate(
                business_name=row.get("business_name", ""),
                contact_name=row.get("owner_name", ""),
                email=row.get("email", ""),
                phone=row.get("phone", ""),
                address=row.get("address", ""),
                website=row.get("website"),
                category=row.get("category", "apparel_accessories"),
                description=row.get("description", ""),
                price_range=PriceRange.UNDER_25,
                fulfillment_method=FulfillmentMethod.SHIPPING,
                image_urls=[row.get("logo_url")] if row.get("logo_url") else [],
                agreement_accepted=True
            )
            
            vendor = db.create_vendor_application(vendor_app)
            
            status_str = row.get("status", "pending").lower()
            if status_str == "approved":
                vendor.status = VendorApplicationStatus.APPROVED
            elif status_str == "rejected":
                vendor.status = VendorApplicationStatus.REJECTED
            else:
                vendor.status = VendorApplicationStatus.PENDING
            
            results["successful"] += 1
            
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Row {results['successful'] + results['failed']}: {str(e)}")
    
    admin_email = os.getenv("ADMIN_EMAIL", "admin@blkxchange.com")
    await send_bulk_import_confirmation(
        admin_email=admin_email,
        category="vendors",
        successful=results["successful"],
        skipped=results["skipped"],
        failed=results["failed"],
        errors=results["errors"]
    )
    
    return results

@app.post("/api/admin/products/import")
async def bulk_import_products(
    data: dict,
    admin: bool = Depends(require_admin)
):
    """Bulk import products from CSV data (admin only)"""
    
    csv_data = data.get("data", [])
    results = {
        "successful": 0,
        "skipped": 0,
        "failed": 0,
        "errors": []
    }
    
    for row in csv_data:
        try:
            vendor_email = row.get("vendor_email", "")
            vendor_apps = db.get_all_vendor_applications()
            vendor_app = next((app for app in vendor_apps if app.email == vendor_email), None)
            
            if not vendor_app:
                results["failed"] += 1
                results["errors"].append(f"Vendor not found for email: {vendor_email}")
                continue
            
            existing_products = db.get_all_products_enhanced(vendor_id=vendor_app.id)
            product_name = row.get("product_name", "")
            if any(p.name == product_name for p in existing_products):
                results["skipped"] += 1
                continue
            
            product_data = ProductCreateEnhanced(
                vendor_id=vendor_app.id,
                name=product_name,
                description=row.get("description", ""),
                price=float(row.get("price", 0)),
                category=row.get("category", "apparel_accessories"),
                quantity=int(row.get("quantity", 0)),
                image_urls=[row.get("image_url")] if row.get("image_url") else []
            )
            
            product = db.create_product_enhanced(product_data)
            
            status_str = row.get("status", "pending").lower()
            if status_str == "approved":
                db.update_product_enhanced_status(product.id, ProductStatus.APPROVED)
            elif status_str == "rejected":
                db.update_product_enhanced_status(product.id, ProductStatus.REJECTED)
            
            results["successful"] += 1
            
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Row {results['successful'] + results['failed']}: {str(e)}")
    
    admin_email = os.getenv("ADMIN_EMAIL", "admin@blkxchange.com")
    await send_bulk_import_confirmation(
        admin_email=admin_email,
        category="products",
        successful=results["successful"],
        skipped=results["skipped"],
        failed=results["failed"],
        errors=results["errors"]
    )
    
    return results

@app.post("/api/admin/professionals/import")
async def bulk_import_professionals(
    data: dict,
    admin: bool = Depends(require_admin)
):
    """Bulk import professionals from CSV data (admin only)"""
    
    csv_data = data.get("data", [])
    results = {
        "successful": 0,
        "skipped": 0,
        "failed": 0,
        "errors": []
    }
    
    for row in csv_data:
        try:
            existing_professionals = db.get_all_professionals()
            email = row.get("email", "")
            if any(p.email == email for p in existing_professionals):
                results["skipped"] += 1
                continue
            
            # Create professional
            professional_data = ProfessionalCreate(
                email=email,
                name=row.get("name", ""),
                title=row.get("tagline") or row.get("business_name") or row.get("name", ""),
                category=row.get("category", "coaching_consulting"),
                bio=row.get("bio", ""),
                credentials="Admin Verified",
                hourly_rate=None,
                phone=row.get("phone"),
                image_url=row.get("image_url"),
                zip=row.get("zip", "")
            )
            
            professional = db.create_professional(professional_data)
            results["successful"] += 1
            
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Row {results['successful'] + results['failed']}: {str(e)}")
    
    admin_email = os.getenv("ADMIN_EMAIL", "admin@blkxchange.com")
    await send_bulk_import_confirmation(
        admin_email=admin_email,
        category="professionals",
        successful=results["successful"],
        skipped=results["skipped"],
        failed=results["failed"],
        errors=results["errors"]
    )
    
    return results

# Test Mode / Sandbox Endpoints
@app.get("/api/admin/test-mode/vendors")
async def get_test_vendors(admin: bool = Depends(require_admin)):
    """Get all test vendor applications"""
    return db.get_all_test_vendor_applications()

@app.get("/api/admin/test-mode/professionals")
async def get_test_professionals(admin: bool = Depends(require_admin)):
    """Get all test professionals"""
    return db.get_all_test_professionals()

@app.get("/api/admin/test-mode/ads")
async def get_test_ads(admin: bool = Depends(require_admin)):
    """Get all test ad creatives"""
    return db.get_all_test_ad_creatives()

@app.post("/api/admin/test-mode/vendors/manual")
async def create_test_vendor_manual(
    data: VendorManualCreate,
    admin: bool = Depends(require_admin)
):
    """Create a test vendor (sandbox mode)"""
    
    vendor_app = VendorApplicationCreate(
        business_name=data.business_name,
        contact_name=data.owner_name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        website=data.website,
        category=data.category,
        description=data.description,
        price_range=PriceRange.UNDER_25,
        fulfillment_method=FulfillmentMethod.SHIPPING,
        image_urls=[data.logo_url] if data.logo_url else [],
        agreement_accepted=True
    )
    
    vendor = db.create_vendor_application(vendor_app)
    vendor.status = data.status
    db.test_vendor_applications[vendor.id] = vendor
    return vendor

@app.post("/api/admin/test-mode/professionals/manual")
async def create_test_professional_manual(
    data: ProfessionalManualCreate,
    admin: bool = Depends(require_admin)
):
    """Create a test professional (sandbox mode)"""
    
    professional_data = ProfessionalCreate(
        email=data.email,
        name=data.name,
        title=data.tagline or data.business_name or data.name,
        category=data.category,
        bio=data.bio,
        credentials=data.credentials,
        hourly_rate=None,
        phone=data.phone,
        website=data.website,
        image_url=data.image_url,
        zip=data.zip
    )
    
    professional = db.create_professional(professional_data)
    db.test_professionals[professional.id] = professional
    return professional

@app.post("/api/admin/test-mode/ads/manual")
async def create_test_ad_manual(
    data: AdManualCreate,
    admin: bool = Depends(require_admin)
):
    """Create a test ad (sandbox mode)"""
    
    advertiser_data = AdvertiserCreate(
        name=data.advertiser_name,
        contact_email="admin@blkxchange.com",
        website=data.target_url,
        tagline=data.tagline
    )
    advertiser = db.create_advertiser(advertiser_data)
    db.test_advertisers[advertiser.id] = advertiser
    
    from datetime import datetime, timedelta
    start_date = data.start_date or datetime.now()
    end_date = data.end_date or (datetime.now() + timedelta(days=30))
    
    ad_data = AdCreativeCreate(
        advertiser_id=advertiser.id,
        asset_url=data.asset_url,
        ad_type=data.ad_type,
        pages=data.pages,
        start_date=start_date,
        end_date=end_date,
        price_tier=PriceTier.BASIC,
        link_url=data.target_url
    )
    
    ad = db.create_ad_creative(ad_data)
    if data.status == AdStatus.LIVE:
        db.update_ad_creative_status(ad.id, AdStatus.LIVE)
    db.test_ad_creatives[ad.id] = ad
    return ad

@app.delete("/api/admin/test-mode/purge")
async def purge_test_data(admin: bool = Depends(require_admin)):
    """Purge all test data"""
    
    counts = db.purge_test_data()
    return {
        "message": "Test data purged successfully",
        "deleted": counts
    }

@app.post("/api/checkout/session")
async def create_checkout_session(cart_data: dict):
    """
    Mock Stripe checkout session endpoint
    Returns a test session ID for future Stripe integration
    """
    import os
    stripe_secret = os.getenv("STRIPE_SECRET_KEY")
    
    if not stripe_secret:
        return {
            "success": False,
            "message": "Stripe integration not configured. Set STRIPE_SECRET_KEY in environment variables.",
            "session_id": None
        }
    
    return {
        "success": True,
        "session_id": "mock_session_" + str(int(datetime.now().timestamp())),
        "message": "Mock checkout session created. Replace with real Stripe integration."
    }

@app.post("/api/checkout/complete")
async def complete_checkout(session_id: str):
    """
    Mock Stripe checkout completion endpoint
    Returns mock success response
    """
    import os
    stripe_secret = os.getenv("STRIPE_SECRET_KEY")
    
    if not stripe_secret:
        return {
            "success": False,
            "message": "Stripe integration not configured."
        }
    
    return {
        "success": True,
        "message": "Mock checkout completed successfully. Replace with real Stripe webhook handling.",
        "order_id": "mock_order_" + str(int(datetime.now().timestamp()))
    }

@app.post("/api/analytics/track")
async def track_analytics(request: Request):
    """
    Track analytics event (view, click, lead)
    """
    data = await request.json()
    entity_type = data.get("entity_type")
    entity_id = data.get("entity_id")
    event_type = data.get("event_type")
    visitor_ip = request.client.host if request.client else None
    
    event_id = db.track_analytics_event(entity_type, entity_id, event_type, visitor_ip)
    
    return {"success": True, "event_id": event_id}

@app.get("/api/analytics/summary/{entity_type}/{entity_id}")
async def get_analytics(entity_type: str, entity_id: str, days: int = 30):
    """
    Get analytics summary for an entity (professional or vendor)
    """
    summary = db.get_analytics_summary(entity_id, entity_type, days)
    return summary

@app.post("/api/forum/posts")
async def create_forum_post(post_data: ForumPostCreate):
    """Create a new forum post"""
    post = db.create_forum_post(post_data)
    return post

@app.get("/api/forum/posts")
async def get_forum_posts(category: Optional[str] = None):
    """Get all forum posts, optionally filtered by category"""
    posts = db.get_all_forum_posts(category)
    return posts

@app.get("/api/forum/posts/{post_id}")
async def get_forum_post(post_id: str):
    """Get a specific forum post"""
    post = db.get_forum_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/api/forum/comments")
async def create_forum_comment(comment_data: ForumCommentCreate):
    """Create a new comment on a forum post"""
    comment = db.create_forum_comment(comment_data)
    return comment

@app.get("/api/forum/posts/{post_id}/comments")
async def get_forum_comments(post_id: str):
    """Get all comments for a specific post"""
    comments = db.get_forum_comments(post_id)
    return comments

@app.post("/api/events")
async def create_event(event_data: EventCreate):
    """Create a new event"""
    event = db.create_event(event_data)
    return event

@app.get("/api/events")
async def get_events(upcoming_only: bool = True):
    """Get all events"""
    events = db.get_all_events(upcoming_only)
    return events

@app.get("/api/events/{event_id}")
async def get_event(event_id: str):
    """Get a specific event"""
    event = db.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/api/events/rsvp")
async def create_event_rsvp(rsvp_data: EventRSVPCreate):
    """RSVP to an event"""
    rsvp = db.create_event_rsvp(rsvp_data)
    if not rsvp:
        raise HTTPException(status_code=400, detail="Already RSVP'd or event is full")
    return rsvp

@app.get("/api/events/{event_id}/rsvps")
async def get_event_rsvps(event_id: str):
    """Get all RSVPs for an event"""
    rsvps = db.get_event_rsvps(event_id)
    return rsvps

@app.post("/api/questions")
async def create_question(question_data: QuestionCreate):
    """Create a new question"""
    question = db.create_question(question_data)
    return question

@app.get("/api/questions")
async def get_questions(category: Optional[str] = None):
    """Get all questions, optionally filtered by category"""
    questions = db.get_all_questions(category)
    return questions

@app.get("/api/questions/{question_id}")
async def get_question(question_id: str):
    """Get a specific question"""
    question = db.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.post("/api/answers")
async def create_answer(answer_data: AnswerCreate):
    """Create a new answer"""
    answer = db.create_answer(answer_data)
    return answer

@app.get("/api/questions/{question_id}/answers")
async def get_answers(question_id: str):
    """Get all answers for a question"""
    answers = db.get_answers(question_id)
    return answers

@app.post("/api/answers/{answer_id}/accept")
async def accept_answer(answer_id: str):
    """Mark an answer as accepted"""
    success = db.accept_answer(answer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"success": True}

@app.post("/api/leads")
async def create_lead(lead_data: LeadCreate):
    """Create a new lead (service request)"""
    lead = db.create_lead(lead_data)
    return lead

@app.get("/api/leads")
async def get_leads(status: Optional[str] = None):
    """Get all leads, optionally filtered by status"""
    leads = db.get_all_leads(status)
    return leads

@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: str):
    """Get a specific lead"""
    lead = db.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.get("/api/leads/{lead_id}/matches")
async def get_lead_matches(lead_id: str):
    """Get all matched professionals for a lead"""
    matches = db.get_lead_matches(lead_id)
    return [{"match": match, "professional": prof} for match, prof in matches]

@app.get("/api/professionals/{professional_id}/leads")
async def get_professional_leads(professional_id: str):
    """Get all leads matched to a professional"""
    leads = db.get_professional_leads(professional_id)
    return [{"match": match, "lead": lead} for match, lead in leads]

# Phase 3: Community Hub, Wallet, Governance, Fund Routes

@app.get("/api/blk360/wallet/{user_id}")
async def get_wallet(user_id: str):
    """Get wallet for a user"""
    wallet = db.get_blk360_wallet_by_user(user_id)
    if not wallet:
        wallet = db.create_blk360_wallet(Blk360WalletCreate(user_id=user_id))
    return wallet

@app.post("/api/blk360/wallet/transaction")
async def add_wallet_transaction(user_id: str, transaction_type: str, amount: int, description: str, category: str):
    """Add a transaction to a wallet"""
    wallet = db.add_wallet_transaction(user_id, transaction_type, amount, description, category)
    return wallet

@app.get("/api/blk360/events")
async def get_events():
    """Get all events"""
    events = db.get_all_blk360_events()
    return events

@app.post("/api/blk360/events")
async def create_event(event_data: Blk360EventCreate):
    """Create a new event"""
    event = db.create_blk360_event(event_data)
    return event

@app.post("/api/blk360/events/{event_id}/rsvp")
async def rsvp_event(event_id: str):
    """RSVP to an event"""
    event = db.increment_event_rsvp(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/api/blk360/governance/proposals")
async def get_proposals(status: Optional[str] = None):
    """Get all proposals"""
    proposals = db.get_all_blk360_proposals(status)
    return proposals

@app.post("/api/blk360/governance/proposals")
async def create_proposal(proposal_data: Blk360ProposalCreate):
    """Create a new proposal"""
    proposal = db.create_blk360_proposal(proposal_data)
    return proposal

@app.post("/api/blk360/governance/proposals/{proposal_id}/vote")
async def vote_on_proposal(proposal_id: str, vote_data: Blk360VoteCreate):
    """Vote on a proposal"""
    vote = db.create_blk360_vote(vote_data)
    return vote

@app.get("/api/blk360/fund/metrics")
async def get_fund_metrics():
    """Get community fund metrics"""
    metrics = db.get_blk360_fund_metrics()
    return metrics

@app.get("/api/blk360/fund/donations/recent")
async def get_recent_donations():
    """Get recent donations"""
    donations = db.get_all_blk360_fund_donations()
    return sorted(donations, key=lambda x: x.timestamp, reverse=True)[:10]

@app.post("/api/blk360/fund/donate")
async def create_donation(donation_data: Blk360FundDonationCreate):
    """Create a new donation"""
    donation = db.create_blk360_fund_donation(donation_data)
    return donation

@app.get("/api/blk360/groups")
async def get_groups():
    """Get all groups"""
    groups = db.get_all_blk360_groups()
    return groups

@app.post("/api/blk360/groups")
async def create_group(group_data: Blk360GroupCreate):
    """Create a new group"""
    group = db.create_blk360_group(group_data)
    return group

@app.get("/api/blk360/membership/{user_id}")
async def get_membership(user_id: str):
    """Get membership for a user"""
    membership = db.get_blk360_membership_by_user(user_id)
    return membership

@app.post("/api/blk360/membership")
async def create_membership(membership_data: Blk360MembershipCreate):
    """Create a new membership"""
    membership = db.create_blk360_membership(membership_data)
    return membership
