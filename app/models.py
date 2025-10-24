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
    APPAREL_ACCESSORIES = "apparel_accessories"
    ART_COLLECTIBLES = "art_collectibles"
    AUTOMOTIVE_TRANSPORTATION = "automotive_transportation"
    BEAUTY_WELLNESS = "beauty_wellness"
    BOOKS_STATIONERY = "books_stationery"
    FOOD_BEVERAGE = "food_beverage"
    HEALTH_PHARMACY = "health_pharmacy"
    HOME_LIVING = "home_living"
    MANUFACTURING_TRADES = "manufacturing_trades"
    TECHNOLOGY_GADGETS = "technology_gadgets"
    OTHER = "other"

class ProfessionalCategory(str, Enum):
    COACHING_CONSULTING = "coaching_consulting"
    EDUCATION_TUTORING = "education_tutoring"
    EVENT_HOSPITALITY = "event_hospitality"
    FINANCE_INSURANCE = "finance_insurance"
    HEALTH_MEDICAL = "health_medical"
    LEGAL_ADVOCACY = "legal_advocacy"
    MEDIA_MARKETING = "media_marketing"
    NONPROFITS_COMMUNITY = "nonprofits_community"
    REAL_ESTATE_WEALTH = "real_estate_wealth"
    TECHNOLOGY_INNOVATION = "technology_innovation"
    TRADES_HOME = "trades_home"
    TRANSPORTATION_LOGISTICS = "transportation_logistics"
    ARTS_CULTURE = "arts_culture"
    BLACK_MEDIA = "black_media"
    FAITH_RESILIENCE = "faith_resilience"
    HBCUS_EDUCATION = "hbcus_education"
    TRAVEL_HERITAGE = "travel_heritage"
    OTHER = "other"

class CulturalCategory(str, Enum):
    ARTS_CULTURE = "arts_culture"
    BLACK_MEDIA = "black_media"
    FAITH_RESILIENCE = "faith_resilience"
    HBCUS_EDUCATION = "hbcus_education"
    TRAVEL_HERITAGE = "travel_heritage"
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
    vendor_name: Optional[str] = None
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
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

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
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ProfessionalNearby(BaseModel):
    id: str
    name: str
    title: str
    category: ProfessionalCategory
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    distance_miles: float
    image_url: Optional[str] = None
    hourly_rate: Optional[float] = None
    verified: bool = False
    rating: float = 0.0
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PendingProfessionalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PendingProfessionalCreate(BaseModel):
    name: str
    category: ProfessionalCategory
    tagline: Optional[str] = None
    description: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    zip: str
    email: EmailStr
    agreement_accepted: bool

class PendingProfessional(BaseModel):
    id: str
    name: str
    category: ProfessionalCategory
    tagline: Optional[str] = None
    description: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    zip: str
    email: EmailStr
    agreement_accepted: bool
    status: PendingProfessionalStatus
    submitted_at: datetime
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

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

class ArticleCategory(str, Enum):
    LATEST_NEWS = "latest_news"
    BLACK_ACHIEVEMENTS = "black_achievements"
    ENTREPRENEUR_SPOTLIGHT = "entrepreneur_spotlight"
    EDUCATION_CULTURE = "education_culture"
    FAITH_RESILIENCE = "faith_resilience"

class ArticleStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PUBLISHED = "published"

class ArticleCreate(BaseModel):
    title: str
    author: str
    email: EmailStr
    category: ArticleCategory
    excerpt: str
    body: str
    image_url: Optional[str] = None

class Article(BaseModel):
    id: str
    title: str
    author: str
    email: EmailStr
    category: ArticleCategory
    excerpt: str
    body: str
    image_url: Optional[str] = None
    status: ArticleStatus
    slug: str
    created_at: datetime
    updated_at: datetime

class AdType(str, Enum):
    BANNER = "banner"
    SIDEBAR = "sidebar"
    CAROUSEL = "carousel"
    SPOTLIGHT = "spotlight"

class AdStatus(str, Enum):
    PENDING = "pending"
    LIVE = "live"
    EXPIRED = "expired"

class PriceTier(str, Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    SPOTLIGHT = "Spotlight"

class AdvertiserCreate(BaseModel):
    name: str
    contact_email: EmailStr
    website: Optional[str] = None
    tagline: Optional[str] = None

class Advertiser(BaseModel):
    id: str
    name: str
    contact_email: EmailStr
    website: Optional[str] = None
    tagline: Optional[str] = None
    created_at: datetime

class AdCreativeCreate(BaseModel):
    advertiser_id: str
    asset_url: str
    ad_type: AdType
    pages: List[str]
    start_date: datetime
    end_date: datetime
    price_tier: PriceTier
    link_url: Optional[str] = None

class AdCreative(BaseModel):
    id: str
    advertiser_id: str
    advertiser_name: Optional[str] = None
    asset_url: str
    ad_type: AdType
    pages: List[str]
    start_date: datetime
    end_date: datetime
    price_tier: PriceTier
    link_url: Optional[str] = None
    status: AdStatus
    created_at: datetime

class AdSlotCreate(BaseModel):
    creative_id: str
    page: str
    placement: str

class AdSlot(BaseModel):
    id: str
    creative_id: str
    page: str
    placement: str
    impressions: int = 0
    clicks: int = 0
    status: AdStatus
    created_at: datetime

class VisitorAnalytics(BaseModel):
    id: str
    month: str  # Format: "YYYY-MM"
    visitor_count: int
    created_at: datetime
    updated_at: datetime

class VendorManualCreate(BaseModel):
    business_name: str
    owner_name: str
    email: EmailStr
    phone: str
    description: str
    category: ProductCategory
    website: Optional[str] = None
    logo_url: Optional[str] = None
    address: str
    zip: str
    status: VendorApplicationStatus = VendorApplicationStatus.APPROVED

class ProductManualCreate(BaseModel):
    vendor_id: str
    name: str
    category: ProductCategory
    price: float
    description: str
    sku: Optional[str] = None
    image_urls: List[str] = []
    quantity: int = 0
    status: ProductStatus = ProductStatus.APPROVED

class AdManualCreate(BaseModel):
    advertiser_name: str
    tagline: Optional[str] = None
    asset_url: str
    target_url: str
    ad_type: AdType
    pages: List[str] = ["marketplace"]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: AdStatus = AdStatus.LIVE

class ProfessionalManualCreate(BaseModel):
    name: str
    category: ProfessionalCategory
    business_name: Optional[str] = None
    tagline: Optional[str] = None
    bio: str
    email: EmailStr
    website: Optional[str] = None
    phone: Optional[str] = None
    zip: str
    image_url: Optional[str] = None
    credentials: str = "Admin Verified"
    status: str = "approved"

# Admin User Authentication Models
class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class AdminUser(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool = True
    created_at: datetime

class AdminUserInDB(AdminUser):
    hashed_password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminToken(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    email: str

class AdminForgotPassword(BaseModel):
    email: EmailStr

class AdminResetPassword(BaseModel):
    token: str
    new_password: str

class PasswordResetToken(BaseModel):
    id: str
    email: EmailStr
    token: str
    expires_at: datetime
    used: bool = False
    created_at: datetime

class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    EDITOR = "editor"
    REVIEWER = "reviewer"
    VENDOR = "vendor"
    PROFESSIONAL = "professional"

class EntityType(str, Enum):
    VENDOR = "vendor"
    PROFESSIONAL = "professional"
    PRODUCT = "product"
    AD = "ad"

class VersionHistory(BaseModel):
    id: str
    entity_type: EntityType
    entity_id: str
    version_number: int
    data_snapshot: dict
    edited_by: str
    edited_by_email: str
    edited_at: datetime
    change_description: Optional[str] = None

class VersionHistoryCreate(BaseModel):
    entity_type: EntityType
    entity_id: str
    data_snapshot: dict
    edited_by: str
    edited_by_email: str
    change_description: Optional[str] = None

class AdminMetrics(BaseModel):
    total_vendors: int
    total_professionals: int
    total_products: int
    total_ads: int
    total_visitors: int
    pending_vendors: int
    pending_professionals: int
    pending_products: int
    last_updated: datetime

class SearchResult(BaseModel):
    id: str
    type: EntityType
    name: str
    email: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
