from fastapi import FastAPI, HTTPException, Header, Depends
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
    AdSlot, AdSlotCreate, AdStatus
)
from app.database import db
from app.seed_data import seed_database
from app.email import send_vendor_welcome_email

app = FastAPI(title="BlkXchange API", version="1.0.0")

ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "changeme")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

async def require_admin(x_admin_secret: Optional[str] = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

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

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

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

# Vendor Application Endpoints
@app.post("/api/vendor-applications", response_model=VendorApplication)
async def create_vendor_application(application: VendorApplicationCreate):
    if not application.agreement_accepted:
        raise HTTPException(status_code=400, detail="Vendor agreement must be accepted")
    new_application = db.create_vendor_application(application)
    print("\n" + "="*80)
    print("📥 New vendor application submitted")
    print(f"Business: {new_application.business_name} | Contact: {new_application.contact_name} | Email: {new_application.email}")
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
