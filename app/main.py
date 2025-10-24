from fastapi import FastAPI, HTTPException, Header, Depends, UploadFile, File, Form
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
    AdminLogin, AdminToken, AdminUserCreate, AdminForgotPassword, AdminResetPassword
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
    x_admin_secret: str = Header(None)
):
    """Get all pending professionals (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.get_all_pending_professionals(status)

@app.post("/api/admin/approve-professional/{professional_id}", response_model=Professional)
async def approve_pending_professional(
    professional_id: str,
    x_admin_secret: str = Header(None)
):
    """Approve a pending professional and create live listing (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    professional = db.approve_pending_professional(professional_id, "admin")
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found or already processed")
    return professional

@app.post("/api/admin/reject-professional/{professional_id}")
async def reject_pending_professional(
    professional_id: str,
    x_admin_secret: str = Header(None)
):
    """Reject a pending professional submission (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    success = db.reject_pending_professional(professional_id)
    if not success:
        raise HTTPException(status_code=404, detail="Professional not found or already processed")
    return {"message": "Professional submission rejected"}

@app.put("/api/professionals/{professional_id}", response_model=Professional)
async def update_professional(
    professional_id: str,
    professional_data: dict,
    x_admin_secret: str = Header(None)
):
    """Update a professional (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    professional = db.update_professional(professional_id, professional_data)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@app.delete("/api/professionals/{professional_id}")
async def delete_professional(
    professional_id: str,
    x_admin_secret: str = Header(None)
):
    """Delete a professional (admin only)"""
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
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
