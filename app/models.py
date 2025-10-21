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
    REAL_ESTATE = "real_estate"
    BARBERS_BEAUTY = "barbers_beauty"
    PHOTOGRAPHY_DESIGN = "photography_design"
    AUTOMOTIVE_HOUSING = "automotive_housing"
    MEDIA_MARKETING = "media_marketing"
    NONPROFITS = "nonprofits"
    OTHER = "other"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class VendorApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ProductStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class FulfillmentMethod(str, Enum):
    SHIPPING = "shipping"
    LOCAL = "local"

class PriceRange(str, Enum):
    UNDER_25 = "<$25"
    RANGE_25_50 = "$25-$50"
    RANGE_50_100 = "$50-$100"
    OVER_100 = ">$100"

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

class VendorApplicationCreate(BaseModel):
    business_name: str
    contact_name: str
    email: EmailStr
    phone: str
    address: str
    website: Optional[str] = None
    category: ProductCategory
    description: str
    price_range: PriceRange
    fulfillment_method: FulfillmentMethod
    image_urls: List[str] = []
    agreement_accepted: bool

class VendorApplication(BaseModel):
    id: str
    business_name: str
    contact_name: str
    email: EmailStr
    phone: str
    address: str
    website: Optional[str] = None
    category: ProductCategory
    description: str
    price_range: PriceRange
    fulfillment_method: FulfillmentMethod
    image_urls: List[str]
    status: VendorApplicationStatus
    agreement_accepted: bool
    created_at: datetime
    updated_at: datetime

class VendorAccountCreate(BaseModel):
    vendor_id: str
    email: EmailStr
    password: str

class VendorAccount(BaseModel):
    id: str
    vendor_id: str
    email: EmailStr
    password_hash: str
    role: UserRole = UserRole.VENDOR
    created_at: datetime

class ProductCreateEnhanced(BaseModel):
    vendor_id: str
    name: str
    description: str
    price: float
    category: ProductCategory
    quantity: int
    image_urls: List[str] = []

class ProductEnhanced(BaseModel):
    id: str
    vendor_id: str
    name: str
    description: str
    price: float
    category: ProductCategory
    quantity: int
    image_urls: List[str]
    status: ProductStatus
    rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime
    updated_at: datetime

class StartupApplicationCreate(BaseModel):
    name: str
    business_name: str
    email: EmailStr
    phone: str
    website: Optional[str] = None
    funding_goal: float
    business_summary: str
    pitch_deck_url: Optional[str] = None
    agreement_accepted: bool

class StartupApplication(BaseModel):
    id: str
    name: str
    business_name: str
    email: EmailStr
    phone: str
    website: Optional[str] = None
    funding_goal: float
    business_summary: str
    pitch_deck_url: Optional[str] = None
    agreement_accepted: bool
    created_at: datetime

class AngelInvestorCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    accreditation_type: str
    investment_range: str
    interests: List[str]
    agreement_accepted: bool

class AngelInvestor(BaseModel):
    id: str
    name: str
    email: EmailStr
    company: Optional[str] = None
    accreditation_type: str
    investment_range: str
    interests: List[str]
    agreement_accepted: bool
    created_at: datetime

class DonationCreate(BaseModel):
    donor_name: str
    email: EmailStr
    amount: float
    institution: str

class Donation(BaseModel):
    id: str
    donor_name: str
    email: EmailStr
    amount: float
    institution: str
    created_at: datetime

class BlackBank(BaseModel):
    id: str
    name: str
    description: str
    location: str
    affiliate_link: str

class InvestImpactStats(BaseModel):
    total_funds_reinvested: float
    hbcu_donations: float
    startup_investments: float
    angel_investors_count: int
    businesses_supported: int
