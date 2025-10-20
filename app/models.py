from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    PROFESSIONAL = "professional"
    ADMIN = "admin"

class ProductCategory(str, Enum):
    APPAREL = "apparel"
    BEAUTY = "beauty"
    BOOKS = "books"
    ART = "art"
    TECH = "tech"
    FOOD = "food"
    WELLNESS = "wellness"
    HOME = "home"
    JEWELRY = "jewelry"
    OTHER = "other"

class ProfessionalCategory(str, Enum):
    HEALTH = "health"
    LEGAL = "legal"
    FINANCE = "finance"
    COACHING = "coaching"
    CONSULTING = "consulting"
    EDUCATION = "education"
    OTHER = "other"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: UserRole
    created_at: datetime

class VendorCreate(BaseModel):
    email: EmailStr
    name: str
    business_name: str
    business_description: str
    phone: Optional[str] = None
    stripe_account_id: Optional[str] = None

class Vendor(BaseModel):
    id: str
    email: EmailStr
    name: str
    business_name: str
    business_description: str
    phone: Optional[str] = None
    stripe_account_id: Optional[str] = None
    verified: bool = False
    total_sales: float = 0.0
    community_contribution: float = 0.0
    created_at: datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory
    image_url: Optional[str] = None
    stock: int = 0

class Product(BaseModel):
    id: str
    vendor_id: str
    name: str
    description: str
    price: float
    category: ProductCategory
    image_url: Optional[str] = None
    stock: int
    rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime

class ProfessionalCreate(BaseModel):
    email: EmailStr
    name: str
    title: str
    category: ProfessionalCategory
    bio: str
    credentials: str
    hourly_rate: Optional[float] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None

class Professional(BaseModel):
    id: str
    email: EmailStr
    name: str
    title: str
    category: ProfessionalCategory
    bio: str
    credentials: str
    hourly_rate: Optional[float] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    verified: bool = False
    rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    customer_email: EmailStr
    customer_name: str
    items: List[OrderItemCreate]
    shipping_address: str

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    vendor_id: str

class Order(BaseModel):
    id: str
    customer_email: EmailStr
    customer_name: str
    items: List[OrderItem]
    total_amount: float
    vendor_amount: float
    platform_amount: float
    community_amount: float
    shipping_address: str
    status: OrderStatus
    created_at: datetime

class ImpactStats(BaseModel):
    total_donations: float
    total_orders: int
    total_vendors: int
    total_professionals: int
    hbcu_donations: float
    scholarship_donations: float
    nonprofit_donations: float
