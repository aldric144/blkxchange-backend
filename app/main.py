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
    BlackBank, InvestImpactStats
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
