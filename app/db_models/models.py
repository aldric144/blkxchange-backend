from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_models import Base

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    business_name = Column(String, nullable=False)
    business_description = Column(Text)
    phone = Column(String)
    stripe_account_id = Column(String)
    verified = Column(Boolean, default=False)
    total_sales = Column(Float, default=0.0)
    community_contribution = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="vendor", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String)
    image_url = Column(String)
    stock = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="products")

class Professional(Base):
    __tablename__ = "professionals"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String)
    bio = Column(Text)
    credentials = Column(String)
    hourly_rate = Column(Float, default=0.0)
    phone = Column(String)
    image_url = Column(String)
    verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    customer_email = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    items = Column(JSON)
    total_amount = Column(Float, nullable=False)
    vendor_amount = Column(Float)
    platform_amount = Column(Float)
    community_amount = Column(Float)
    shipping_address = Column(JSON)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class VendorApplication(Base):
    __tablename__ = "vendor_applications"
    
    id = Column(String, primary_key=True)
    business_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(Text)
    website = Column(String)
    category = Column(String)
    description = Column(Text)
    price_range = Column(String)
    fulfillment_method = Column(String)
    image_urls = Column(JSON)
    status = Column(String, default="pending")
    agreement_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VendorAccount(Base):
    __tablename__ = "vendor_accounts"
    
    id = Column(String, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductEnhanced(Base):
    __tablename__ = "products_enhanced"
    
    id = Column(String, primary_key=True)
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String)
    quantity = Column(Integer, default=0)
    image_urls = Column(JSON)
    status = Column(String, default="pending")
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(String)
    body = Column(Text)
    author = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    category = Column(String)
    description = Column(Text)
    video_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Legacy(Base):
    __tablename__ = "legacy"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    relation = Column(String)
    biography = Column(Text)
    photo_url = Column(String)
    era = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    description = Column(Text)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ForumTopic(Base):
    __tablename__ = "forum_topics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    title = Column(String, nullable=False)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    replies = relationship("ForumReply", back_populates="topic", cascade="all, delete-orphan")

class ForumReply(Base):
    __tablename__ = "forum_replies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("forum_topics.id"), nullable=False)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    topic = relationship("ForumTopic", back_populates="replies")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    date = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ImpactStat(Base):
    __tablename__ = "impact_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_donations = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    total_vendors = Column(Integer, default=0)
    total_professionals = Column(Integer, default=0)
    hbcu_donations = Column(Float, default=0.0)
    scholarship_donations = Column(Float, default=0.0)
    nonprofit_donations = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    description = Column(Text)
    color_theme = Column(String)
    image_url = Column(String)
    icon = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    membership_tier = Column(String, default="Free")
    join_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Partner(Base):
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    org_name = Column(String, nullable=False)
    logo_url = Column(String)
    website = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Testimonial(Base):
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    photo_url = Column(String)
    quote = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)

class Scholarship(Base):
    __tablename__ = "scholarships"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(String)
    apply_url = Column(String)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class BusinessMatchmaker(Base):
    __tablename__ = "business_matchmaker"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    interest = Column(String)
    preferred_category = Column(String)
    match_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
