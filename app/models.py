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

class MembershipTier(str, Enum):
    BASIC = "basic"
    FEATURED = "featured"
    ELITE = "elite"

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
    verified_documents: Optional[str] = None
    membership_tier: MembershipTier = MembershipTier.BASIC
    subscription_id: Optional[str] = None
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
    website: Optional[str] = None
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
    website: Optional[str] = None
    image_url: Optional[str] = None
    verified: bool = False
    verified_documents: Optional[str] = None
    membership_tier: MembershipTier = MembershipTier.BASIC
    subscription_id: Optional[str] = None
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
    email: Optional[str] = None
    website: Optional[str] = None
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
    address: str
    city: str
    state: str
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
    address: str
    city: str
    state: str
    zip: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
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
    city: str
    state: str
    zip: str
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
    city: str
    state: str
    zip: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
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

class AnalyticsEvent(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    event_type: str
    visitor_ip: Optional[str] = None
    visitor_location: Optional[dict] = None
    created_at: datetime

class AnalyticsSummary(BaseModel):
    entity_id: str
    entity_type: str
    total_views: int
    total_clicks: int
    total_leads: int
    unique_visitors: int
    top_locations: List[dict]
    period_start: datetime
    period_end: datetime


class ForumCategory(str, Enum):
    BUSINESS = "business"
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    CULTURE = "culture"
    HEALTH = "health"
    EDUCATION = "education"
    GENERAL = "general"

class ForumPostCreate(BaseModel):
    title: str
    content: str
    category: ForumCategory
    author_name: str
    author_email: EmailStr

class ForumPost(BaseModel):
    id: str
    title: str
    content: str
    category: ForumCategory
    author_name: str
    author_email: str
    views: int = 0
    likes: int = 0
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime

class ForumCommentCreate(BaseModel):
    post_id: str
    content: str
    author_name: str
    author_email: EmailStr

class ForumComment(BaseModel):
    id: str
    post_id: str
    content: str
    author_name: str
    author_email: str
    likes: int = 0
    created_at: datetime

class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    event_date: datetime
    organizer_name: str
    organizer_email: EmailStr
    image_url: Optional[str] = None
    max_attendees: Optional[int] = None

class Event(BaseModel):
    id: str
    title: str
    description: str
    location: str
    event_date: datetime
    organizer_name: str
    organizer_email: str
    image_url: Optional[str] = None
    max_attendees: Optional[int] = None
    rsvp_count: int = 0
    created_at: datetime

class EventRSVPCreate(BaseModel):
    event_id: str
    attendee_name: str
    attendee_email: EmailStr

class EventRSVP(BaseModel):
    id: str
    event_id: str
    attendee_name: str
    attendee_email: str
    created_at: datetime

class QuestionCreate(BaseModel):
    title: str
    content: str
    category: ForumCategory
    author_name: str
    author_email: EmailStr

class Question(BaseModel):
    id: str
    title: str
    content: str
    category: ForumCategory
    author_name: str
    author_email: str
    views: int = 0
    upvotes: int = 0
    answer_count: int = 0
    has_accepted_answer: bool = False
    created_at: datetime

class AnswerCreate(BaseModel):
    question_id: str
    content: str
    author_name: str
    author_email: EmailStr

class Answer(BaseModel):
    id: str
    question_id: str
    content: str
    author_name: str
    author_email: str
    upvotes: int = 0
    is_accepted: bool = False
    created_at: datetime

class LeadCreate(BaseModel):
    title: str
    description: str
    category: ProfessionalCategory
    budget_range: str
    location: str
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    deadline: Optional[datetime] = None

class Lead(BaseModel):
    id: str
    title: str
    description: str
    category: ProfessionalCategory
    budget_range: str
    location: str
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: str
    contact_email: str
    contact_phone: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "open"
    match_count: int = 0
    created_at: datetime

class LeadMatch(BaseModel):
    id: str
    lead_id: str
    professional_id: str
    match_score: float
    notified: bool = False
    responded: bool = False
    created_at: datetime



# Membership Subscription Models
class SubscriptionTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ELITE = "elite"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"

class Blk360SubscriptionCreate(BaseModel):
    user_email: EmailStr
    tier: SubscriptionTier
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

class Blk360Subscription(BaseModel):
    id: str
    user_email: EmailStr
    tier: SubscriptionTier
    status: SubscriptionStatus
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class WealthModuleCategory(str, Enum):
    ENTREPRENEURSHIP = "entrepreneurship"
    INVESTING = "investing"
    LEADERSHIP = "leadership"
    FINANCIAL_LITERACY = "financial_literacy"
    MINDSET = "mindset"

class WealthModuleAccessLevel(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ELITE = "elite"

class Blk360WealthModuleCreate(BaseModel):
    title: str
    category: WealthModuleCategory
    description: str
    video_url: Optional[str] = None
    article_url: Optional[str] = None
    pdf_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    access_level: WealthModuleAccessLevel
    published: bool = True

class Blk360WealthModule(BaseModel):
    id: str
    title: str
    category: WealthModuleCategory
    description: str
    video_url: Optional[str] = None
    article_url: Optional[str] = None
    pdf_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    access_level: WealthModuleAccessLevel
    published: bool
    views: int = 0
    created_at: datetime
    updated_at: datetime

class LegacyEntryStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LegacyEntryCategory(str, Enum):
    FAMILY = "family"
    COMMUNITY = "community"
    BUSINESS = "business"
    EDUCATION = "education"
    FAITH = "faith"
    OTHER = "other"

class Blk360LegacyEntryCreate(BaseModel):
    user_email: EmailStr
    title: str
    honoree_name: str
    photo_url: Optional[str] = None
    story: str
    category: LegacyEntryCategory

class Blk360LegacyEntry(BaseModel):
    id: str
    user_email: EmailStr
    title: str
    honoree_name: str
    photo_url: Optional[str] = None
    story: str
    category: LegacyEntryCategory
    status: LegacyEntryStatus
    featured: bool = False
    created_at: datetime
    updated_at: datetime

class HistorySourceType(str, Enum):
    MANUAL = "manual"
    AI_CRAWLER = "ai_crawler"
    COMMUNITY = "community"

class HistoryEntryStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class HistoryDecade(str, Enum):
    PRE_1900 = "pre_1900"
    DECADE_1900_1950 = "1900_1950"
    DECADE_1950_2000 = "1950_2000"
    DECADE_2000_TODAY = "2000_today"

class Blk360HistoryEntryCreate(BaseModel):
    name: str
    field: str
    decade: HistoryDecade
    biography: str
    photo_url: Optional[str] = None
    source_url: Optional[str] = None
    source_type: HistorySourceType = HistorySourceType.MANUAL

class Blk360HistoryEntry(BaseModel):
    id: str
    name: str
    field: str
    decade: HistoryDecade
    biography: str
    photo_url: Optional[str] = None
    source_url: Optional[str] = None
    source_type: HistorySourceType
    status: HistoryEntryStatus
    approved: bool = False
    created_at: datetime
    updated_at: datetime

class Forum360Category(str, Enum):
    BUSINESS = "business"
    HEALTH = "health"
    FAITH = "faith"
    CULTURE = "culture"
    TECH = "tech"
    LEADERSHIP = "leadership"
    ELITE_LOUNGE = "elite_lounge"

class Forum360PostStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    DELETED = "deleted"

class Blk360ForumPostCreate(BaseModel):
    title: str
    content: str
    category: Forum360Category
    author_name: str
    author_email: EmailStr

class Blk360ForumPost(BaseModel):
    id: str
    title: str
    content: str
    category: Forum360Category
    author_name: str
    author_email: str
    status: Forum360PostStatus
    pinned: bool = False
    views: int = 0
    reply_count: int = 0
    created_at: datetime
    updated_at: datetime

class Blk360ForumReplyCreate(BaseModel):
    post_id: str
    content: str
    author_name: str
    author_email: EmailStr

class Blk360ForumReply(BaseModel):
    id: str
    post_id: str
    content: str
    author_name: str
    author_email: str
    created_at: datetime

class Blk360AnalyticsMetrics(BaseModel):
    total_subscriptions: int
    premium_subscribers: int
    elite_subscribers: int
    monthly_revenue: float
    wealth_modules_count: int
    legacy_entries_pending: int
    legacy_entries_approved: int
    history_entries_count: int
    forum_posts_count: int
    forum_replies_count: int

# Phase 3: Community Hub, Wallet, Governance, Fund Models

class Blk360WalletTransaction(BaseModel):
    id: str
    user_id: str
    type: str  # 'earned' | 'spent' | 'bonus'
    amount: int
    description: str
    category: str
    timestamp: datetime

class Blk360Wallet(BaseModel):
    id: str
    user_id: str
    balance: int
    lifetime_earned: int
    lifetime_spent: int
    transactions: List[Blk360WalletTransaction]
    created_at: datetime
    updated_at: datetime

class Blk360WalletCreate(BaseModel):
    user_id: str

class Blk360Event(BaseModel):
    id: str
    title: str
    description: str
    date: str
    time: str
    location: str
    category: str
    image_url: Optional[str] = None
    rsvp_count: int = 0
    status: str  # 'upcoming' | 'ongoing' | 'past'
    created_at: datetime
    updated_at: datetime

class Blk360EventCreate(BaseModel):
    title: str
    description: str
    date: str
    time: str
    location: str
    category: str
    image_url: Optional[str] = None

class Blk360Proposal(BaseModel):
    id: str
    title: str
    summary: str
    description: str
    category: str
    status: str  # 'active' | 'passed' | 'rejected' | 'pending'
    created_by: str
    created_at: datetime
    deadline: str
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    total_votes: int = 0
    quorum_required: int = 100

class Blk360ProposalCreate(BaseModel):
    title: str
    summary: str
    description: str
    category: str
    created_by: str

class Blk360Vote(BaseModel):
    id: str
    proposal_id: str
    user_id: str
    vote: str  # 'for' | 'against' | 'abstain'
    timestamp: datetime

class Blk360VoteCreate(BaseModel):
    proposal_id: str
    user_id: str
    vote: str

class Blk360FundDonation(BaseModel):
    id: str
    donor_name: str
    email: str
    amount: float
    category: str
    anonymous: bool = False
    timestamp: datetime

class Blk360FundDonationCreate(BaseModel):
    donor_name: str
    email: str
    amount: float
    category: str
    anonymous: bool = False

class Blk360FundMetrics(BaseModel):
    total_raised: float
    vendor_allocation: float
    operations_allocation: float
    hbcu_allocation: float
    total_vendors_supported: int
    total_hbcus_supported: int
    monthly_growth: float

class Blk360Group(BaseModel):
    id: str
    name: str
    description: str
    visibility: str  # 'public' | 'private'
    created_by: str
    member_count: int = 0
    created_at: datetime

class Blk360GroupCreate(BaseModel):
    name: str
    description: str
    visibility: str
    created_by: str

class Blk360GroupMember(BaseModel):
    id: str
    group_id: str
    user_id: str
    role: str  # 'admin' | 'member'
    joined_at: datetime

class Blk360Membership(BaseModel):
    id: str
    user_id: str
    tier: str  # 'free' | 'premium' | 'elite'
    consent_timestamp: datetime
    terms_accepted: bool
    agreement_date: datetime

class Blk360MembershipCreate(BaseModel):
    user_id: str
    tier: str
    terms_accepted: bool
