from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.utils.security import verify_admin_credentials, create_access_token, require_admin_token
from app.database import db
from app.models import VendorApplicationStatus, ProductStatus

router = APIRouter()

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: str

class AdminMetrics(BaseModel):
    vendors: int
    products: int
    professionals: int
    orders: int
    impact_score: float

@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(credentials: AdminLogin):
    if not verify_admin_credentials(credentials.email, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": credentials.email, "role": "admin"})
    
    return AdminLoginResponse(
        access_token=access_token,
        token_type="bearer",
        message="Login successful"
    )

@router.get("/metrics", response_model=AdminMetrics)
async def get_admin_metrics(admin=Depends(require_admin_token)):
    vendors = db.get_all_vendors()
    products = db.get_all_products()
    professionals = db.get_all_professionals()
    orders = db.get_all_orders()
    impact_stats = db.get_impact_stats()
    
    return AdminMetrics(
        vendors=len(vendors),
        products=len(products),
        professionals=len(professionals),
        orders=len(orders),
        impact_score=impact_stats.total_donations
    )

@router.get("/vendors")
async def get_admin_vendors(admin=Depends(require_admin_token)):
    return db.get_all_vendors()

@router.get("/products")
async def get_admin_products(admin=Depends(require_admin_token)):
    return db.get_all_products()

@router.post("/approve-vendor/{application_id}")
async def approve_vendor_admin(application_id: str, admin=Depends(require_admin_token)):
    from app.models import VendorCreate
    
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

@router.post("/reject-vendor/{application_id}")
async def reject_vendor_admin(application_id: str, reason: Optional[str] = None, admin=Depends(require_admin_token)):
    application = db.get_vendor_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.update_vendor_application_status(application_id, VendorApplicationStatus.REJECTED)
    
    return {"message": "Vendor application rejected", "reason": reason}

@router.post("/approve-product/{product_id}")
async def approve_product_admin(product_id: str, admin=Depends(require_admin_token)):
    product = db.update_product_enhanced_status(product_id, ProductStatus.APPROVED)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product approved", "product": product}

@router.post("/reject-product/{product_id}")
async def reject_product_admin(product_id: str, reason: Optional[str] = None, admin=Depends(require_admin_token)):
    product = db.update_product_enhanced_status(product_id, ProductStatus.REJECTED)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product rejected", "reason": reason}
