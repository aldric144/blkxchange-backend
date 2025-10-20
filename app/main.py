from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import psycopg

from app.models import (
    VendorCreate, Vendor, ProductCreate, Product,
    ProfessionalCreate, Professional, OrderCreate, Order,
    ImpactStats, ProductCategory, ProfessionalCategory
)
from app.database import db
from app.seed_data import seed_database
from app.email import send_vendor_welcome_email

app = FastAPI(title="BlkXchange API", version="1.0.0")

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
