from typing import Dict, List, Optional
from datetime import datetime
import uuid
import hashlib
from app.models import (
    Vendor, VendorCreate, Product, ProductCreate, 
    Professional, ProfessionalCreate, Order, OrderCreate,
    OrderItem, OrderStatus, ImpactStats,
    VendorApplication, VendorApplicationCreate, VendorApplicationStatus,
    VendorAccount, VendorAccountCreate,
    ProductEnhanced, ProductCreateEnhanced, ProductStatus,
    StartupApplication, StartupApplicationCreate,
    AngelInvestor, AngelInvestorCreate,
    Donation, DonationCreate,
    BlackBank, InvestImpactStats,
    Article, ArticleCreate, ArticleStatus, ArticleCategory,
    Advertiser, AdvertiserCreate, AdCreative, AdCreativeCreate, 
    AdSlot, AdSlotCreate, AdStatus,
    VisitorAnalytics,
    PendingProfessional, PendingProfessionalCreate, PendingProfessionalStatus,
    MembershipTier,
    Blk360Wallet, Blk360WalletCreate, Blk360WalletTransaction,
    Blk360Event, Blk360EventCreate,
    Blk360Proposal, Blk360ProposalCreate, Blk360Vote, Blk360VoteCreate,
    Blk360FundDonation, Blk360FundDonationCreate, Blk360FundMetrics,
    Blk360Group, Blk360GroupCreate, Blk360GroupMember,
    Blk360Membership, Blk360MembershipCreate
)

class InMemoryDatabase:
    def __init__(self):
        self.vendors: Dict[str, Vendor] = {}
        self.products: Dict[str, Product] = {}
        self.professionals: Dict[str, Professional] = {}
        self.orders: Dict[str, Order] = {}
        self.vendor_applications: Dict[str, VendorApplication] = {}
        self.vendor_accounts: Dict[str, VendorAccount] = {}
        self.products_enhanced: Dict[str, ProductEnhanced] = {}
        self.password_setup_tokens: Dict[str, dict] = {}
        self.startup_applications: Dict[str, StartupApplication] = {}
        self.angel_investors: Dict[str, AngelInvestor] = {}
        self.donations: Dict[str, Donation] = {}
        self.black_banks: Dict[str, BlackBank] = {}
        self.articles: Dict[str, Article] = {}
        self.advertisers: Dict[str, Advertiser] = {}
        self.ad_creatives: Dict[str, AdCreative] = {}
        self.ad_slots: Dict[str, AdSlot] = {}
        self.visitor_analytics: Dict[str, VisitorAnalytics] = {}
        self.pending_professionals: Dict[str, PendingProfessional] = {}
        
        self.test_vendor_applications: Dict[str, VendorApplication] = {}
        self.test_professionals: Dict[str, Professional] = {}
        self.test_ad_creatives: Dict[str, AdCreative] = {}
        self.test_advertisers: Dict[str, Advertiser] = {}
        
        self.blk360_wallets: Dict[str, 'Blk360Wallet'] = {}
        self.blk360_events: Dict[str, 'Blk360Event'] = {}
        self.blk360_proposals: Dict[str, 'Blk360Proposal'] = {}
        self.blk360_votes: Dict[str, 'Blk360Vote'] = {}
        self.blk360_fund_donations: Dict[str, 'Blk360FundDonation'] = {}
        self.blk360_groups: Dict[str, 'Blk360Group'] = {}
        self.blk360_group_members: Dict[str, 'Blk360GroupMember'] = {}
        self.blk360_memberships: Dict[str, 'Blk360Membership'] = {}
        self.blk360_2fa: Dict[str, 'Blk360TwoFA'] = {}
        self.blk360_audit_logs: Dict[str, 'Blk360AuditLog'] = {}
        self.blk360_affiliates: Dict[str, 'Blk360Affiliate'] = {}
        
        self.subscriptions: Dict[str, dict] = {}
        self.payouts: Dict[str, dict] = {}
        self.affiliates: Dict[str, dict] = {}
        self.ai_history: Dict[str, dict] = {}
        self.ai_mentorships: Dict[str, dict] = {}
        self.ai_content: Dict[str, dict] = {}
        self.payment_metadata: Dict[str, dict] = {}
        
        self.blk360_blkcoin_wallets: Dict[str, dict] = {}
        self.blk360_blkcoin_transactions: Dict[str, dict] = {}
        self.blk360_blkcoin_rewards: Dict[str, dict] = {}
        self.blk360_scholarships: Dict[str, dict] = {}
        self.blk360_scholarship_applications: Dict[str, dict] = {}
        self.blk360_scholarship_donations: Dict[str, dict] = {}
        
        self.blk360_events_enhanced: Dict[str, dict] = {}
        self.blk360_partners: Dict[str, dict] = {}
        self.blk360_nonprofits: Dict[str, dict] = {}
        self.blk360_volunteer_logs: Dict[str, dict] = {}
        self.blk360_donations: Dict[str, dict] = {}
        
        self.impact_stats = {
            "total_donations": 0.0,
            "total_orders": 0,
            "hbcu_donations": 0.0,
            "scholarship_donations": 0.0,
            "nonprofit_donations": 0.0
        }
        self.admin_users: Dict[str, dict] = {}
        self.password_reset_tokens: Dict[str, dict] = {}
        self._seed_black_banks()
        self._seed_admin_users()
        self._seed_blkcoin_rewards()
    
    def create_vendor(self, vendor_data: VendorCreate) -> Vendor:
        vendor_id = str(uuid.uuid4())
        vendor = Vendor(
            id=vendor_id,
            email=vendor_data.email,
            name=vendor_data.name,
            business_name=vendor_data.business_name,
            business_description=vendor_data.business_description,
            phone=vendor_data.phone,
            stripe_account_id=vendor_data.stripe_account_id,
            verified=False,
            verified_documents=None,
            membership_tier=MembershipTier.BASIC,
            subscription_id=None,
            total_sales=0.0,
            community_contribution=0.0,
            created_at=datetime.now()
        )
        self.vendors[vendor_id] = vendor
        return vendor
    
    def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
        return self.vendors.get(vendor_id)
    
    def get_all_vendors(self) -> List[Vendor]:
        return list(self.vendors.values())
    
    def update_vendor_sales(self, vendor_id: str, amount: float, community_amount: float):
        if vendor_id in self.vendors:
            self.vendors[vendor_id].total_sales += amount
            self.vendors[vendor_id].community_contribution += community_amount
    
    def update_vendor(self, vendor_id: str, vendor_data: dict) -> Optional[Vendor]:
        """Update vendor information"""
        if vendor_id not in self.vendors:
            return None
        vendor = self.vendors[vendor_id]
        for key, value in vendor_data.items():
            if hasattr(vendor, key):
                setattr(vendor, key, value)
        return vendor
    
    def delete_vendor(self, vendor_id: str) -> bool:
        """Delete a vendor"""
        if vendor_id in self.vendors:
            del self.vendors[vendor_id]
            return True
        return False
    
    def create_product(self, vendor_id: str, product_data: ProductCreate) -> Product:
        product_id = str(uuid.uuid4())
        vendor = self.get_vendor(vendor_id)
        vendor_name = vendor.name if vendor else None
        product = Product(
            id=product_id,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            image_url=product_data.image_url,
            stock=product_data.stock,
            rating=0.0,
            reviews_count=0,
            created_at=datetime.now()
        )
        self.products[product_id] = product
        return product
    
    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)
    
    def get_all_products(self, category: Optional[str] = None, vendor_id: Optional[str] = None) -> List[Product]:
        products = list(self.products.values())
        if category:
            products = [p for p in products if p.category == category]
        if vendor_id:
            products = [p for p in products if p.vendor_id == vendor_id]
        return products
    
    def update_product(self, product_id: str, product_data: ProductCreate) -> Optional[Product]:
        if product_id in self.products:
            product = self.products[product_id]
            product.name = product_data.name
            product.description = product_data.description
            product.price = product_data.price
            product.category = product_data.category
            product.image_url = product_data.image_url
            product.stock = product_data.stock
            return product
        return None
    
    def delete_product(self, product_id: str) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    def create_professional(self, professional_data: ProfessionalCreate) -> Professional:
        professional_id = str(uuid.uuid4())
        professional = Professional(
            id=professional_id,
            email=professional_data.email,
            name=professional_data.name,
            title=professional_data.title,
            category=professional_data.category,
            bio=professional_data.bio,
            credentials=professional_data.credentials,
            hourly_rate=professional_data.hourly_rate,
            phone=professional_data.phone,
            website=professional_data.website,
            image_url=professional_data.image_url,
            verified=False,
            verified_documents=None,
            membership_tier=MembershipTier.BASIC,
            subscription_id=None,
            rating=0.0,
            reviews_count=0,
            created_at=datetime.now(),
            street=professional_data.street,
            city=professional_data.city,
            state=professional_data.state,
            zip=professional_data.zip,
            country=professional_data.country,
            latitude=professional_data.latitude,
            longitude=professional_data.longitude
        )
        self.professionals[professional_id] = professional
        return professional
    
    def get_professional(self, professional_id: str) -> Optional[Professional]:
        return self.professionals.get(professional_id)
    
    def get_all_professionals(self, category: Optional[str] = None) -> List[Professional]:
        professionals = list(self.professionals.values())
        if category:
            professionals = [p for p in professionals if p.category == category]
        
        tier_order = {MembershipTier.ELITE: 0, MembershipTier.FEATURED: 1, MembershipTier.BASIC: 2}
        professionals.sort(key=lambda p: (tier_order.get(p.membership_tier, 3), -p.rating))
        
        return professionals
    
    def update_professional(self, professional_id: str, update_data: dict) -> Optional[Professional]:
        professional = self.professionals.get(professional_id)
        if not professional:
            return None
        
        for key, value in update_data.items():
            if hasattr(professional, key) and value is not None:
                setattr(professional, key, value)
        
        return professional
    
    def delete_professional(self, professional_id: str) -> bool:
        if professional_id in self.professionals:
            del self.professionals[professional_id]
            return True
        return False
    
    def get_professionals_nearby(self, latitude: float, longitude: float, radius_miles: float = 25.0, category: Optional[str] = None) -> List[dict]:
        """
        Get professionals within a specified radius using Haversine distance formula.
        Returns list of professionals with distance_miles calculated.
        """
        import math
        
        def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            """Calculate distance between two points on Earth in miles."""
            R = 3959  # Earth's radius in miles
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            return R * c
        
        nearby_professionals = []
        
        for professional in self.professionals.values():
            if professional.latitude is None or professional.longitude is None:
                continue
            
            if category and professional.category != category:
                continue
            
            distance = haversine_distance(latitude, longitude, professional.latitude, professional.longitude)
            
            if distance <= radius_miles:
                nearby_professionals.append({
                    "id": professional.id,
                    "name": professional.name,
                    "title": professional.title,
                    "category": professional.category,
                    "city": professional.city,
                    "state": professional.state,
                    "zip": professional.zip,
                    "distance_miles": round(distance, 2),
                    "email": professional.email,
                    "website": professional.website,
                    "image_url": professional.image_url,
                    "hourly_rate": professional.hourly_rate,
                    "verified": professional.verified,
                    "membership_tier": professional.membership_tier,
                    "rating": professional.rating,
                    "latitude": professional.latitude,
                    "longitude": professional.longitude
                })
        
        tier_order = {MembershipTier.ELITE: 0, MembershipTier.FEATURED: 1, MembershipTier.BASIC: 2}
        nearby_professionals.sort(key=lambda x: (tier_order.get(x["membership_tier"], 3), x["distance_miles"]))
        
        return nearby_professionals
    
    def count_new_professionals_since(self, since_date: datetime) -> int:
        count = 0
        for professional in self.professionals.values():
            if professional.created_at and professional.created_at >= since_date:
                count += 1
        return count
    
    def count_new_vendors_since(self, since_date: datetime) -> int:
        count = 0
        for application in self.vendor_applications.values():
            if application.status == "approved" and application.created_at >= since_date:
                count += 1
        return count
    
    def create_order(self, order_data: OrderCreate) -> Order:
        order_id = str(uuid.uuid4())
        
        order_items = []
        total_amount = 0.0
        
        for item_data in order_data.items:
            product = self.get_product(item_data.product_id)
            if product:
                item_total = product.price * item_data.quantity
                total_amount += item_total
                
                order_item = OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item_data.quantity,
                    price=product.price,
                    vendor_id=product.vendor_id
                )
                order_items.append(order_item)
        
        vendor_amount = total_amount * 0.85
        platform_amount = total_amount * 0.12
        community_amount = total_amount * 0.03
        
        order = Order(
            id=order_id,
            customer_email=order_data.customer_email,
            customer_name=order_data.customer_name,
            items=order_items,
            total_amount=total_amount,
            vendor_amount=vendor_amount,
            platform_amount=platform_amount,
            community_amount=community_amount,
            shipping_address=order_data.shipping_address,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.orders[order_id] = order
        
        self.impact_stats["total_donations"] += community_amount
        self.impact_stats["total_orders"] += 1
        self.impact_stats["hbcu_donations"] += community_amount * 0.5
        self.impact_stats["scholarship_donations"] += community_amount * 0.3
        self.impact_stats["nonprofit_donations"] += community_amount * 0.2
        
        for item in order_items:
            self.update_vendor_sales(item.vendor_id, vendor_amount / len(order_items), community_amount / len(order_items))
        
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> List[Order]:
        return list(self.orders.values())
    
    def get_impact_stats(self) -> ImpactStats:
        return ImpactStats(
            total_donations=self.impact_stats["total_donations"],
            total_orders=self.impact_stats["total_orders"],
            total_vendors=len(self.vendors),
            total_professionals=len(self.professionals),
            hbcu_donations=self.impact_stats["hbcu_donations"],
            scholarship_donations=self.impact_stats["scholarship_donations"],
            nonprofit_donations=self.impact_stats["nonprofit_donations"]
        )
    
    def create_vendor_application(self, application_data: VendorApplicationCreate) -> VendorApplication:
        application_id = str(uuid.uuid4())
        application = VendorApplication(
            id=application_id,
            business_name=application_data.business_name,
            contact_name=application_data.contact_name,
            email=application_data.email,
            phone=application_data.phone,
            address=application_data.address,
            city=application_data.city,
            state=application_data.state,
            zip=application_data.zip,
            latitude=None,
            longitude=None,
            website=application_data.website,
            category=application_data.category,
            description=application_data.description,
            price_range=application_data.price_range,
            fulfillment_method=application_data.fulfillment_method,
            image_urls=application_data.image_urls,
            status=VendorApplicationStatus.PENDING,
            agreement_accepted=application_data.agreement_accepted,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.vendor_applications[application_id] = application
        return application
    
    def update_vendor_application_coordinates(self, application_id: str, latitude: float, longitude: float) -> bool:
        """Update the geocoded coordinates for a vendor application"""
        application = self.vendor_applications.get(application_id)
        if application:
            application.latitude = latitude
            application.longitude = longitude
            return True
        return False
    
    def get_vendor_application(self, application_id: str) -> Optional[VendorApplication]:
        return self.vendor_applications.get(application_id)
    
    def get_all_vendor_applications(self, status: Optional[VendorApplicationStatus] = None) -> List[VendorApplication]:
        applications = list(self.vendor_applications.values())
        if status:
            applications = [a for a in applications if a.status == status]
        return applications
    
    def update_vendor_application_status(self, application_id: str, status: VendorApplicationStatus) -> Optional[VendorApplication]:
        if application_id in self.vendor_applications:
            self.vendor_applications[application_id].status = status
            self.vendor_applications[application_id].updated_at = datetime.now()
            return self.vendor_applications[application_id]
        return None
    
    def create_vendor_account(self, account_data: VendorAccountCreate) -> VendorAccount:
        account_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(account_data.password.encode()).hexdigest()
        account = VendorAccount(
            id=account_id,
            vendor_id=account_data.vendor_id,
            email=account_data.email,
            password_hash=password_hash,
            created_at=datetime.now()
        )
        self.vendor_accounts[account_id] = account
        return account
    
    def get_vendor_account_by_email(self, email: str) -> Optional[VendorAccount]:
        for account in self.vendor_accounts.values():
            if account.email == email:
                return account
        return None
    
    def verify_vendor_password(self, email: str, password: str) -> Optional[VendorAccount]:
        account = self.get_vendor_account_by_email(email)
        if account:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if account.password_hash == password_hash:
                return account
        return None
    
    def create_product_enhanced(self, product_data: ProductCreateEnhanced) -> ProductEnhanced:
        product_id = str(uuid.uuid4())
        product = ProductEnhanced(
            id=product_id,
            vendor_id=product_data.vendor_id,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            quantity=product_data.quantity,
            image_urls=product_data.image_urls,
            status=ProductStatus.PENDING,
            rating=0.0,
            reviews_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.products_enhanced[product_id] = product
        return product
    
    def get_product_enhanced(self, product_id: str) -> Optional[ProductEnhanced]:
        return self.products_enhanced.get(product_id)
    
    def get_all_products_enhanced(self, vendor_id: Optional[str] = None, status: Optional[ProductStatus] = None) -> List[ProductEnhanced]:
        products = list(self.products_enhanced.values())
        if vendor_id:
            products = [p for p in products if p.vendor_id == vendor_id]
        if status:
            products = [p for p in products if p.status == status]
        return products
    
    def update_product_enhanced_status(self, product_id: str, status: ProductStatus) -> Optional[ProductEnhanced]:
        if product_id in self.products_enhanced:
            self.products_enhanced[product_id].status = status
            self.products_enhanced[product_id].updated_at = datetime.now()
            return self.products_enhanced[product_id]
        return None
    
    def update_product_enhanced(self, product_id: str, product_data: ProductCreateEnhanced) -> Optional[ProductEnhanced]:
        if product_id in self.products_enhanced:
            product = self.products_enhanced[product_id]
            product.name = product_data.name
            product.description = product_data.description
            product.price = product_data.price
            product.category = product_data.category
            product.quantity = product_data.quantity
            product.image_urls = product_data.image_urls
            product.updated_at = datetime.now()
            return product
        return None

    def create_password_setup_token(self, vendor_id: str, email: str) -> str:
        token = str(uuid.uuid4())
        expires_at = datetime.now().timestamp() + 24 * 60 * 60
        self.password_setup_tokens[token] = {"vendor_id": vendor_id, "email": email, "expires_at": expires_at}
        return token

    def consume_password_setup_token(self, token: str) -> Optional[dict]:
        data = self.password_setup_tokens.get(token)
        if not data:
            return None
        if datetime.now().timestamp() > data.get("expires_at", 0):
            del self.password_setup_tokens[token]
            return None
        del self.password_setup_tokens[token]
        return data
    
    def _seed_black_banks(self):
        banks = [
            {"name": "OneUnited Bank", "description": "Nation's largest Black-owned bank", "location": "Nationwide", "affiliate_link": "https://www.oneunited.com"},
            {"name": "Carver Federal Savings", "description": "Historic NYC institution", "location": "New York", "affiliate_link": "https://www.carverbank.com"},
            {"name": "Liberty Bank", "description": "One of the oldest Black-owned banks", "location": "New Orleans, LA", "affiliate_link": "https://www.liberty-bank.com"},
            {"name": "Citizens Trust Bank", "description": "Atlanta's premier Black-owned bank", "location": "Atlanta, GA", "affiliate_link": "https://www.ctbconnect.com"}
        ]
        for bank_data in banks:
            bank_id = str(uuid.uuid4())
            bank = BlackBank(id=bank_id, **bank_data)
            self.black_banks[bank_id] = bank
    
    def create_startup_application(self, application_data: StartupApplicationCreate) -> StartupApplication:
        application_id = str(uuid.uuid4())
        application = StartupApplication(
            id=application_id,
            name=application_data.name,
            business_name=application_data.business_name,
            email=application_data.email,
            phone=application_data.phone,
            website=application_data.website,
            funding_goal=application_data.funding_goal,
            business_summary=application_data.business_summary,
            pitch_deck_url=application_data.pitch_deck_url,
            agreement_accepted=application_data.agreement_accepted,
            created_at=datetime.now()
        )
        self.startup_applications[application_id] = application
        return application
    
    def get_all_startup_applications(self) -> List[StartupApplication]:
        return list(self.startup_applications.values())
    
    def create_angel_investor(self, investor_data: AngelInvestorCreate) -> AngelInvestor:
        investor_id = str(uuid.uuid4())
        investor = AngelInvestor(
            id=investor_id,
            name=investor_data.name,
            email=investor_data.email,
            company=investor_data.company,
            accreditation_type=investor_data.accreditation_type,
            investment_range=investor_data.investment_range,
            interests=investor_data.interests,
            agreement_accepted=investor_data.agreement_accepted,
            created_at=datetime.now()
        )
        self.angel_investors[investor_id] = investor
        return investor
    
    def get_all_angel_investors(self) -> List[AngelInvestor]:
        return list(self.angel_investors.values())
    
    def create_donation(self, donation_data: DonationCreate) -> Donation:
        donation_id = str(uuid.uuid4())
        donation = Donation(
            id=donation_id,
            donor_name=donation_data.donor_name,
            email=donation_data.email,
            amount=donation_data.amount,
            institution=donation_data.institution,
            created_at=datetime.now()
        )
        self.donations[donation_id] = donation
        self.impact_stats["hbcu_donations"] += donation_data.amount
        self.impact_stats["total_donations"] += donation_data.amount
        return donation
    
    def get_all_donations(self) -> List[Donation]:
        return list(self.donations.values())
    
    def get_all_black_banks(self) -> List[BlackBank]:
        return list(self.black_banks.values())
    
    def get_invest_impact_stats(self) -> InvestImpactStats:
        total_startup_funding = sum(app.funding_goal for app in self.startup_applications.values())
        return InvestImpactStats(
            total_funds_reinvested=self.impact_stats["total_donations"],
            hbcu_donations=self.impact_stats["hbcu_donations"],
            startup_investments=total_startup_funding,
            angel_investors_count=len(self.angel_investors),
            businesses_supported=len(self.startup_applications)
        )
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        slug = title.lower()
        slug = slug.replace(" ", "-")
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return f"{slug}-{str(uuid.uuid4())[:8]}"
    
    def create_article(self, article_data: ArticleCreate) -> Article:
        article_id = str(uuid.uuid4())
        slug = self._generate_slug(article_data.title)
        article = Article(
            id=article_id,
            title=article_data.title,
            author=article_data.author,
            email=article_data.email,
            category=article_data.category,
            excerpt=article_data.excerpt,
            body=article_data.body,
            image_url=article_data.image_url,
            status=ArticleStatus.PENDING,
            slug=slug,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.articles[article_id] = article
        return article
    
    def get_article(self, article_id: str) -> Optional[Article]:
        return self.articles.get(article_id)
    
    def get_article_by_slug(self, slug: str) -> Optional[Article]:
        for article in self.articles.values():
            if article.slug == slug:
                return article
        return None
    
    def get_all_articles(self, category: Optional[ArticleCategory] = None, status: Optional[ArticleStatus] = None) -> List[Article]:
        articles = list(self.articles.values())
        if category:
            articles = [a for a in articles if a.category == category]
        if status:
            articles = [a for a in articles if a.status == status]
        articles.sort(key=lambda x: x.created_at, reverse=True)
        return articles
    
    def update_article_status(self, article_id: str, status: ArticleStatus) -> Optional[Article]:
        if article_id in self.articles:
            self.articles[article_id].status = status
            self.articles[article_id].updated_at = datetime.now()
            return self.articles[article_id]
        return None
    
    def create_advertiser(self, advertiser_data: AdvertiserCreate) -> Advertiser:
        advertiser_id = str(uuid.uuid4())
        advertiser = Advertiser(
            id=advertiser_id,
            name=advertiser_data.name,
            contact_email=advertiser_data.contact_email,
            website=advertiser_data.website,
            tagline=advertiser_data.tagline,
            created_at=datetime.now()
        )
        self.advertisers[advertiser_id] = advertiser
        return advertiser
    
    def get_advertiser(self, advertiser_id: str) -> Optional[Advertiser]:
        return self.advertisers.get(advertiser_id)
    
    def get_all_advertisers(self) -> List[Advertiser]:
        return list(self.advertisers.values())
    
    def create_ad_creative(self, creative_data: AdCreativeCreate) -> AdCreative:
        creative_id = str(uuid.uuid4())
        advertiser = self.get_advertiser(creative_data.advertiser_id)
        advertiser_name = advertiser.name if advertiser else None
        
        creative = AdCreative(
            id=creative_id,
            advertiser_id=creative_data.advertiser_id,
            advertiser_name=advertiser_name,
            asset_url=creative_data.asset_url,
            ad_type=creative_data.ad_type,
            pages=creative_data.pages,
            start_date=creative_data.start_date,
            end_date=creative_data.end_date,
            price_tier=creative_data.price_tier,
            link_url=creative_data.link_url,
            status=AdStatus.LIVE,
            created_at=datetime.now()
        )
        self.ad_creatives[creative_id] = creative
        return creative
    
    def get_ad_creative(self, creative_id: str) -> Optional[AdCreative]:
        return self.ad_creatives.get(creative_id)
    
    def get_all_ad_creatives(self, status: Optional[AdStatus] = None, page: Optional[str] = None) -> List[AdCreative]:
        creatives = list(self.ad_creatives.values())
        if status:
            creatives = [c for c in creatives if c.status == status]
        if page:
            creatives = [c for c in creatives if page in c.pages]
        
        now = datetime.now()
        for creative in creatives:
            if creative.end_date < now and creative.status == AdStatus.LIVE:
                creative.status = AdStatus.EXPIRED
        
        return creatives
    
    def update_ad_creative_status(self, creative_id: str, status: AdStatus) -> Optional[AdCreative]:
        if creative_id in self.ad_creatives:
            self.ad_creatives[creative_id].status = status
            return self.ad_creatives[creative_id]
        return None
    
    def update_ad_creative(self, creative_id: str, update_data: dict) -> Optional[AdCreative]:
        creative = self.ad_creatives.get(creative_id)
        if not creative:
            return None
        
        for key, value in update_data.items():
            if hasattr(creative, key) and value is not None:
                setattr(creative, key, value)
        
        return creative
    
    def delete_ad_creative(self, creative_id: str) -> bool:
        if creative_id in self.ad_creatives:
            del self.ad_creatives[creative_id]
            return True
        return False
    
    def create_ad_slot(self, slot_data: AdSlotCreate) -> AdSlot:
        slot_id = str(uuid.uuid4())
        creative = self.get_ad_creative(slot_data.creative_id)
        status = creative.status if creative else AdStatus.PENDING
        
        slot = AdSlot(
            id=slot_id,
            creative_id=slot_data.creative_id,
            page=slot_data.page,
            placement=slot_data.placement,
            impressions=0,
            clicks=0,
            status=status,
            created_at=datetime.now()
        )
        self.ad_slots[slot_id] = slot
        return slot
    
    def get_ad_slots_by_page(self, page: str, placement: Optional[str] = None) -> List[AdSlot]:
        slots = [s for s in self.ad_slots.values() if s.page == page and s.status == AdStatus.LIVE]
        if placement:
            slots = [s for s in slots if s.placement == placement]
        return slots
    
    def increment_ad_impression(self, slot_id: str):
        if slot_id in self.ad_slots:
            self.ad_slots[slot_id].impressions += 1
    
    def increment_ad_click(self, slot_id: str):
        if slot_id in self.ad_slots:
            self.ad_slots[slot_id].clicks += 1
    
    def increment_visitor_count(self) -> VisitorAnalytics:
        """Increment visitor count for current month"""
        from datetime import datetime
        current_month = datetime.now().strftime("%Y-%m")
        
        if current_month in self.visitor_analytics:
            analytics = self.visitor_analytics[current_month]
            analytics.visitor_count += 1
            analytics.updated_at = datetime.now()
        else:
            analytics_id = str(uuid.uuid4())
            analytics = VisitorAnalytics(
                id=analytics_id,
                month=current_month,
                visitor_count=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.visitor_analytics[current_month] = analytics
        
        return analytics
    
    def get_current_month_visitors(self) -> int:
        """Get visitor count for current month"""
        from datetime import datetime
        current_month = datetime.now().strftime("%Y-%m")
        
        if current_month in self.visitor_analytics:
            return self.visitor_analytics[current_month].visitor_count
        return 0
    
    def create_pending_professional(self, data: PendingProfessionalCreate) -> PendingProfessional:
        """Create a new pending professional submission"""
        professional_id = str(uuid.uuid4())
        pending = PendingProfessional(
            id=professional_id,
            name=data.name,
            category=data.category,
            tagline=data.tagline,
            description=data.description,
            website=data.website,
            logo_url=data.logo_url,
            address=data.address,
            city=data.city,
            state=data.state,
            zip=data.zip,
            latitude=None,
            longitude=None,
            email=data.email,
            agreement_accepted=data.agreement_accepted,
            status=PendingProfessionalStatus.PENDING,
            submitted_at=datetime.now(),
            approved_by=None,
            approved_at=None
        )
        self.pending_professionals[professional_id] = pending
        return pending
    
    def update_pending_professional_coordinates(self, professional_id: str, latitude: float, longitude: float) -> bool:
        """Update the geocoded coordinates for a pending professional"""
        pending = self.pending_professionals.get(professional_id)
        if pending:
            pending.latitude = latitude
            pending.longitude = longitude
            return True
        return False
    
    def get_pending_professional(self, professional_id: str) -> Optional[PendingProfessional]:
        """Get a pending professional by ID"""
        return self.pending_professionals.get(professional_id)
    
    def get_all_pending_professionals(self, status: Optional[PendingProfessionalStatus] = None) -> List[PendingProfessional]:
        """Get all pending professionals, optionally filtered by status"""
        professionals = list(self.pending_professionals.values())
        if status:
            professionals = [p for p in professionals if p.status == status]
        return sorted(professionals, key=lambda x: x.submitted_at, reverse=True)
    
    def approve_pending_professional(self, professional_id: str, approved_by: str) -> Optional[Professional]:
        """Approve a pending professional and create a live professional listing"""
        pending = self.pending_professionals.get(professional_id)
        if not pending or pending.status != PendingProfessionalStatus.PENDING:
            return None
        
        pending.status = PendingProfessionalStatus.APPROVED
        pending.approved_by = approved_by
        pending.approved_at = datetime.now()
        
        # Create live professional
        professional_create = ProfessionalCreate(
            email=pending.email,
            name=pending.name,
            title=pending.tagline or pending.name,
            category=pending.category,
            bio=pending.description,
            credentials="Community Submitted",
            hourly_rate=None,
            phone=None,
            image_url=pending.logo_url,
            zip=pending.zip
        )
        
        professional = self.create_professional(professional_create)
        return professional
    
    def reject_pending_professional(self, professional_id: str) -> bool:
        """Reject a pending professional submission"""
        pending = self.pending_professionals.get(professional_id)
        if not pending or pending.status != PendingProfessionalStatus.PENDING:
            return False
        
        pending.status = PendingProfessionalStatus.REJECTED
        return True
    
    def get_all_test_vendor_applications(self) -> List[VendorApplication]:
        """Get all test vendor applications"""
        return list(self.test_vendor_applications.values())
    
    def get_all_test_professionals(self) -> List[Professional]:
        """Get all test professionals"""
        return list(self.test_professionals.values())
    
    def get_all_test_ad_creatives(self) -> List[AdCreative]:
        """Get all test ad creatives"""
        return list(self.test_ad_creatives.values())
    
    def purge_test_data(self) -> dict:
        """Purge all test data and return counts"""
        counts = {
            "vendors": len(self.test_vendor_applications),
            "professionals": len(self.test_professionals),
            "ads": len(self.test_ad_creatives),
            "advertisers": len(self.test_advertisers)
        }
        
        self.test_vendor_applications.clear()
        self.test_professionals.clear()
        self.test_ad_creatives.clear()
        self.test_advertisers.clear()
        
        return counts
    
    def _seed_admin_users(self):
        """Create default admin users"""
        from app.auth import get_password_hash
        from app.models import AdminUserInDB
        
        # Create primary admin
        admin_id1 = str(uuid.uuid4())
        admin1 = AdminUserInDB(
            id=admin_id1,
            email="aldrictmarshall3@gmail.com",
            full_name="Dr. Aldric Marshall",
            hashed_password=get_password_hash("BlkXchange2025!"),
            is_active=True,
            created_at=datetime.now()
        )
        self.admin_users[admin_id1] = admin1
        
        # Create backup admin
        admin_id2 = str(uuid.uuid4())
        admin2 = AdminUserInDB(
            id=admin_id2,
            email="klove144@bellsouth.net",
            full_name="Backup Admin",
            hashed_password=get_password_hash("BlkXchange2025!"),
            is_active=True,
            created_at=datetime.now()
        )
        self.admin_users[admin_id2] = admin2
        
        admin_id3 = str(uuid.uuid4())
        admin3 = AdminUserInDB(
            id=admin_id3,
            email="admin@blkxchange.com",
            full_name="BlkXchange 360 Admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            created_at=datetime.now()
        )
        self.admin_users[admin_id3] = admin3
    
    def get_admin_user_by_email(self, email: str):
        """Get admin user by email"""
        for user in self.admin_users.values():
            if user.email == email:
                return user
        return None
    
    def create_admin_user(self, user_data):
        """Create a new admin user"""
        from app.auth import get_password_hash
        from app.models import AdminUserInDB
        
        user_id = str(uuid.uuid4())
        user = AdminUserInDB(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            is_active=True,
            created_at=datetime.now()
        )
        self.admin_users[user_id] = user
        return user
    
    def update_admin_password(self, email: str, new_password: str) -> bool:
        """Update admin user password"""
        from app.auth import get_password_hash
        
        user = self.get_admin_user_by_email(email)
        if user:
            user.hashed_password = get_password_hash(new_password)
            return True
        return False
    
    def create_password_reset_token(self, email: str, token: str, expires_at: datetime) -> dict:
        """Create a password reset token"""
        token_id = str(uuid.uuid4())
        token_data = {
            "id": token_id,
            "email": email,
            "token": token,
            "expires_at": expires_at,
            "used": False,
            "created_at": datetime.now()
        }
        self.password_reset_tokens[token] = token_data
        return token_data
    
    def get_password_reset_token(self, token: str) -> Optional[dict]:
        """Get password reset token data"""
        return self.password_reset_tokens.get(token)
    
    def mark_reset_token_used(self, token: str) -> bool:
        """Mark a reset token as used"""
        if token in self.password_reset_tokens:
            self.password_reset_tokens[token]["used"] = True
            return True
        return False
    
    def track_analytics_event(self, entity_type: str, entity_id: str, event_type: str, visitor_ip: Optional[str] = None) -> str:
        """Track an analytics event (view, click, lead)"""
        from app.models import AnalyticsEvent
        
        event_id = str(uuid.uuid4())
        event = AnalyticsEvent(
            id=event_id,
            entity_type=entity_type,
            entity_id=entity_id,
            event_type=event_type,
            visitor_ip=visitor_ip,
            visitor_location=None,
            created_at=datetime.now()
        )
        
        if not hasattr(self, 'analytics_events'):
            self.analytics_events: Dict[str, AnalyticsEvent] = {}
        
        self.analytics_events[event_id] = event
        return event_id
    
    def get_analytics_summary(self, entity_id: str, entity_type: str, days: int = 30) -> dict:
        """Get analytics summary for an entity"""
        if not hasattr(self, 'analytics_events'):
            self.analytics_events: Dict[str, AnalyticsEvent] = {}
        
        period_start = datetime.now() - timedelta(days=days)
        period_end = datetime.now()
        
        events = [e for e in self.analytics_events.values() 
                 if e.entity_id == entity_id 
                 and e.entity_type == entity_type
                 and e.created_at >= period_start]
        
        views = [e for e in events if e.event_type == 'view']
        clicks = [e for e in events if e.event_type == 'click']
        leads = [e for e in events if e.event_type == 'lead']
        
        unique_ips = set(e.visitor_ip for e in events if e.visitor_ip)
        
        location_counts = {}
        for event in events:
            if event.visitor_location and 'city' in event.visitor_location:
                loc = f"{event.visitor_location.get('city', 'Unknown')}, {event.visitor_location.get('state', 'Unknown')}"
                location_counts[loc] = location_counts.get(loc, 0) + 1
        
        top_locations = [{"location": loc, "count": count} 
                        for loc, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]]
        
        return {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "total_views": len(views),
            "total_clicks": len(clicks),
            "total_leads": len(leads),
            "unique_visitors": len(unique_ips),
            "top_locations": top_locations,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat()
        }
    
    def create_forum_post(self, post_data: 'ForumPostCreate') -> 'ForumPost':
        from app.models import ForumPost
        post_id = str(uuid.uuid4())
        post = ForumPost(
            id=post_id,
            title=post_data.title,
            content=post_data.content,
            category=post_data.category,
            author_name=post_data.author_name,
            author_email=post_data.author_email,
            views=0,
            likes=0,
            comment_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        if not hasattr(self, 'forum_posts'):
            self.forum_posts: Dict[str, 'ForumPost'] = {}
        self.forum_posts[post_id] = post
        return post
    
    def get_forum_post(self, post_id: str) -> Optional['ForumPost']:
        if not hasattr(self, 'forum_posts'):
            self.forum_posts: Dict[str, 'ForumPost'] = {}
        post = self.forum_posts.get(post_id)
        if post:
            post.views += 1
        return post
    
    def get_all_forum_posts(self, category: Optional[str] = None) -> List['ForumPost']:
        if not hasattr(self, 'forum_posts'):
            self.forum_posts: Dict[str, 'ForumPost'] = {}
        posts = list(self.forum_posts.values())
        if category and category != 'all':
            posts = [p for p in posts if p.category == category]
        posts.sort(key=lambda x: x.created_at, reverse=True)
        return posts
    
    def create_forum_comment(self, comment_data: 'ForumCommentCreate') -> 'ForumComment':
        from app.models import ForumComment
        comment_id = str(uuid.uuid4())
        comment = ForumComment(
            id=comment_id,
            post_id=comment_data.post_id,
            content=comment_data.content,
            author_name=comment_data.author_name,
            author_email=comment_data.author_email,
            likes=0,
            created_at=datetime.now()
        )
        if not hasattr(self, 'forum_comments'):
            self.forum_comments: Dict[str, 'ForumComment'] = {}
        self.forum_comments[comment_id] = comment
        
        if hasattr(self, 'forum_posts') and comment_data.post_id in self.forum_posts:
            self.forum_posts[comment_data.post_id].comment_count += 1
        
        return comment
    
    def get_forum_comments(self, post_id: str) -> List['ForumComment']:
        if not hasattr(self, 'forum_comments'):
            self.forum_comments: Dict[str, 'ForumComment'] = {}
        comments = [c for c in self.forum_comments.values() if c.post_id == post_id]
        comments.sort(key=lambda x: x.created_at)
        return comments
    
    def create_event(self, event_data: 'EventCreate') -> 'Event':
        from app.models import Event
        event_id = str(uuid.uuid4())
        event = Event(
            id=event_id,
            title=event_data.title,
            description=event_data.description,
            location=event_data.location,
            event_date=event_data.event_date,
            organizer_name=event_data.organizer_name,
            organizer_email=event_data.organizer_email,
            image_url=event_data.image_url,
            max_attendees=event_data.max_attendees,
            rsvp_count=0,
            created_at=datetime.now()
        )
        if not hasattr(self, 'events'):
            self.events: Dict[str, 'Event'] = {}
        self.events[event_id] = event
        return event
    
    def get_event(self, event_id: str) -> Optional['Event']:
        if not hasattr(self, 'events'):
            self.events: Dict[str, 'Event'] = {}
        return self.events.get(event_id)
    
    def get_all_events(self, upcoming_only: bool = True) -> List['Event']:
        if not hasattr(self, 'events'):
            self.events: Dict[str, 'Event'] = {}
        events = list(self.events.values())
        if upcoming_only:
            now = datetime.now()
            events = [e for e in events if e.event_date > now]
        events.sort(key=lambda x: x.event_date)
        return events
    
    def create_event_rsvp(self, rsvp_data: 'EventRSVPCreate') -> Optional['EventRSVP']:
        from app.models import EventRSVP
        
        if not hasattr(self, 'event_rsvps'):
            self.event_rsvps: Dict[str, 'EventRSVP'] = {}
        
        existing_rsvp = next((r for r in self.event_rsvps.values() 
                             if r.event_id == rsvp_data.event_id and r.attendee_email == rsvp_data.attendee_email), None)
        if existing_rsvp:
            return None
        
        if hasattr(self, 'events') and rsvp_data.event_id in self.events:
            event = self.events[rsvp_data.event_id]
            if event.max_attendees and event.rsvp_count >= event.max_attendees:
                return None
        
        rsvp_id = str(uuid.uuid4())
        rsvp = EventRSVP(
            id=rsvp_id,
            event_id=rsvp_data.event_id,
            attendee_name=rsvp_data.attendee_name,
            attendee_email=rsvp_data.attendee_email,
            created_at=datetime.now()
        )
        self.event_rsvps[rsvp_id] = rsvp
        
        if hasattr(self, 'events') and rsvp_data.event_id in self.events:
            self.events[rsvp_data.event_id].rsvp_count += 1
        
        return rsvp
    
    def get_event_rsvps(self, event_id: str) -> List['EventRSVP']:
        if not hasattr(self, 'event_rsvps'):
            self.event_rsvps: Dict[str, 'EventRSVP'] = {}
        return [r for r in self.event_rsvps.values() if r.event_id == event_id]
    
    def create_question(self, question_data: 'QuestionCreate') -> 'Question':
        from app.models import Question
        question_id = str(uuid.uuid4())
        question = Question(
            id=question_id,
            title=question_data.title,
            content=question_data.content,
            category=question_data.category,
            author_name=question_data.author_name,
            author_email=question_data.author_email,
            views=0,
            upvotes=0,
            answer_count=0,
            has_accepted_answer=False,
            created_at=datetime.now()
        )
        if not hasattr(self, 'questions'):
            self.questions: Dict[str, 'Question'] = {}
        self.questions[question_id] = question
        return question
    
    def get_question(self, question_id: str) -> Optional['Question']:
        if not hasattr(self, 'questions'):
            self.questions: Dict[str, 'Question'] = {}
        question = self.questions.get(question_id)
        if question:
            question.views += 1
        return question
    
    def get_all_questions(self, category: Optional[str] = None) -> List['Question']:
        if not hasattr(self, 'questions'):
            self.questions: Dict[str, 'Question'] = {}
        questions = list(self.questions.values())
        if category and category != 'all':
            questions = [q for q in questions if q.category == category]
        questions.sort(key=lambda x: x.created_at, reverse=True)
        return questions
    
    def create_answer(self, answer_data: 'AnswerCreate') -> 'Answer':
        from app.models import Answer
        answer_id = str(uuid.uuid4())
        answer = Answer(
            id=answer_id,
            question_id=answer_data.question_id,
            content=answer_data.content,
            author_name=answer_data.author_name,
            author_email=answer_data.author_email,
            upvotes=0,
            is_accepted=False,
            created_at=datetime.now()
        )
        if not hasattr(self, 'answers'):
            self.answers: Dict[str, 'Answer'] = {}
        self.answers[answer_id] = answer
        
        if hasattr(self, 'questions') and answer_data.question_id in self.questions:
            self.questions[answer_data.question_id].answer_count += 1
        
        return answer
    
    def get_answers(self, question_id: str) -> List['Answer']:
        if not hasattr(self, 'answers'):
            self.answers: Dict[str, 'Answer'] = {}
        answers = [a for a in self.answers.values() if a.question_id == question_id]
        answers.sort(key=lambda x: (not x.is_accepted, -x.upvotes, x.created_at))
        return answers
    
    def accept_answer(self, answer_id: str) -> bool:
        if not hasattr(self, 'answers'):
            self.answers: Dict[str, 'Answer'] = {}
        answer = self.answers.get(answer_id)
        if not answer:
            return False
        
        answer.is_accepted = True
        
        if hasattr(self, 'questions') and answer.question_id in self.questions:
            self.questions[answer.question_id].has_accepted_answer = True
        
        return True
    
    def create_lead(self, lead_data: 'LeadCreate') -> 'Lead':
        from app.models import Lead
        lead_id = str(uuid.uuid4())
        lead = Lead(
            id=lead_id,
            title=lead_data.title,
            description=lead_data.description,
            category=lead_data.category,
            budget_range=lead_data.budget_range,
            location=lead_data.location,
            city=lead_data.city,
            state=lead_data.state,
            latitude=lead_data.latitude,
            longitude=lead_data.longitude,
            contact_name=lead_data.contact_name,
            contact_email=lead_data.contact_email,
            contact_phone=lead_data.contact_phone,
            deadline=lead_data.deadline,
            status="open",
            match_count=0,
            created_at=datetime.now()
        )
        if not hasattr(self, 'leads'):
            self.leads: Dict[str, 'Lead'] = {}
        self.leads[lead_id] = lead
        
        self._match_lead_to_professionals(lead)
        
        return lead
    
    def _match_lead_to_professionals(self, lead: 'Lead'):
        from app.models import LeadMatch
        import math
        
        if not hasattr(self, 'lead_matches'):
            self.lead_matches: Dict[str, 'LeadMatch'] = {}
        
        professionals = [p for p in self.professionals.values() if p.category == lead.category]
        
        for prof in professionals:
            match_score = 100.0
            
            if lead.latitude and lead.longitude and prof.latitude and prof.longitude:
                def haversine_distance(lat1, lon1, lat2, lon2):
                    R = 3959
                    phi1, phi2 = math.radians(lat1), math.radians(lat2)
                    delta_phi = math.radians(lat2 - lat1)
                    delta_lambda = math.radians(lon2 - lon1)
                    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                    return R * c
                
                distance = haversine_distance(lead.latitude, lead.longitude, prof.latitude, prof.longitude)
                
                if distance > 100:
                    match_score -= 50
                elif distance > 50:
                    match_score -= 30
                elif distance > 25:
                    match_score -= 15
            
            if prof.verified:
                match_score += 10
            
            if prof.membership_tier == MembershipTier.ELITE:
                match_score += 15
            elif prof.membership_tier == MembershipTier.FEATURED:
                match_score += 10
            
            if prof.rating >= 4.5:
                match_score += 10
            elif prof.rating >= 4.0:
                match_score += 5
            
            if match_score >= 50:
                match_id = str(uuid.uuid4())
                match = LeadMatch(
                    id=match_id,
                    lead_id=lead.id,
                    professional_id=prof.id,
                    match_score=match_score,
                    notified=False,
                    responded=False,
                    created_at=datetime.now()
                )
                self.lead_matches[match_id] = match
                lead.match_count += 1
    
    def get_lead(self, lead_id: str) -> Optional['Lead']:
        if not hasattr(self, 'leads'):
            self.leads: Dict[str, 'Lead'] = {}
        return self.leads.get(lead_id)
    
    def get_all_leads(self, status: Optional[str] = None) -> List['Lead']:
        if not hasattr(self, 'leads'):
            self.leads: Dict[str, 'Lead'] = {}
        leads = list(self.leads.values())
        if status:
            leads = [l for l in leads if l.status == status]
        leads.sort(key=lambda x: x.created_at, reverse=True)
        return leads
    
    def get_lead_matches(self, lead_id: str) -> List[tuple['LeadMatch', 'Professional']]:
        if not hasattr(self, 'lead_matches'):
            self.lead_matches: Dict[str, 'LeadMatch'] = {}
        
        matches = [m for m in self.lead_matches.values() if m.lead_id == lead_id]
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        result = []
        for match in matches:
            prof = self.professionals.get(match.professional_id)
            if prof:
                result.append((match, prof))
        
        return result
    
    def get_professional_leads(self, professional_id: str) -> List[tuple['LeadMatch', 'Lead']]:
        if not hasattr(self, 'lead_matches'):
            self.lead_matches: Dict[str, 'LeadMatch'] = {}
        if not hasattr(self, 'leads'):
            self.leads: Dict[str, 'Lead'] = {}
        
        matches = [m for m in self.lead_matches.values() if m.professional_id == professional_id]
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        result = []
        for match in matches:
            lead = self.leads.get(match.lead_id)
            if lead and lead.status == "open":
                result.append((match, lead))
        
        return result
    
    def mark_lead_match_notified(self, match_id: str):
        if not hasattr(self, 'lead_matches'):
            self.lead_matches: Dict[str, 'LeadMatch'] = {}
        if match_id in self.lead_matches:
            self.lead_matches[match_id].notified = True
    
    def create_blk360_subscription(self, subscription_data: 'Blk360SubscriptionCreate') -> 'Blk360Subscription':
        if not hasattr(self, 'blk360_subscriptions'):
            self.blk360_subscriptions: Dict[str, 'Blk360Subscription'] = {}
        
        from app.models import Blk360Subscription, SubscriptionStatus
        subscription_id = str(uuid.uuid4())
        subscription = Blk360Subscription(
            id=subscription_id,
            user_email=subscription_data.user_email,
            tier=subscription_data.tier,
            status=SubscriptionStatus.ACTIVE,
            stripe_customer_id=subscription_data.stripe_customer_id,
            stripe_subscription_id=subscription_data.stripe_subscription_id,
            current_period_start=datetime.now(),
            current_period_end=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_subscriptions[subscription_id] = subscription
        return subscription
    
    def get_blk360_subscription_by_email(self, email: str) -> Optional['Blk360Subscription']:
        if not hasattr(self, 'blk360_subscriptions'):
            self.blk360_subscriptions: Dict[str, 'Blk360Subscription'] = {}
        for sub in self.blk360_subscriptions.values():
            if sub.user_email == email:
                return sub
        return None
    
    def get_all_blk360_subscriptions(self) -> List['Blk360Subscription']:
        if not hasattr(self, 'blk360_subscriptions'):
            self.blk360_subscriptions: Dict[str, 'Blk360Subscription'] = {}
        return list(self.blk360_subscriptions.values())
    
    def create_blk360_wealth_module(self, module_data: 'Blk360WealthModuleCreate') -> 'Blk360WealthModule':
        if not hasattr(self, 'blk360_wealth_modules'):
            self.blk360_wealth_modules: Dict[str, 'Blk360WealthModule'] = {}
        
        from app.models import Blk360WealthModule
        module_id = str(uuid.uuid4())
        module = Blk360WealthModule(
            id=module_id,
            title=module_data.title,
            category=module_data.category,
            description=module_data.description,
            video_url=module_data.video_url,
            article_url=module_data.article_url,
            pdf_url=module_data.pdf_url,
            thumbnail_url=module_data.thumbnail_url,
            access_level=module_data.access_level,
            published=module_data.published,
            views=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_wealth_modules[module_id] = module
        return module
    
    def get_all_blk360_wealth_modules(self, published_only: bool = True) -> List['Blk360WealthModule']:
        if not hasattr(self, 'blk360_wealth_modules'):
            self.blk360_wealth_modules: Dict[str, 'Blk360WealthModule'] = {}
        modules = list(self.blk360_wealth_modules.values())
        if published_only:
            modules = [m for m in modules if m.published]
        return modules
    
    def update_blk360_wealth_module(self, module_id: str, module_data: 'Blk360WealthModuleCreate') -> Optional['Blk360WealthModule']:
        if not hasattr(self, 'blk360_wealth_modules'):
            self.blk360_wealth_modules: Dict[str, 'Blk360WealthModule'] = {}
        if module_id in self.blk360_wealth_modules:
            module = self.blk360_wealth_modules[module_id]
            module.title = module_data.title
            module.category = module_data.category
            module.description = module_data.description
            module.video_url = module_data.video_url
            module.article_url = module_data.article_url
            module.pdf_url = module_data.pdf_url
            module.thumbnail_url = module_data.thumbnail_url
            module.access_level = module_data.access_level
            module.published = module_data.published
            module.updated_at = datetime.now()
            return module
        return None
    
    def delete_blk360_wealth_module(self, module_id: str) -> bool:
        if not hasattr(self, 'blk360_wealth_modules'):
            self.blk360_wealth_modules: Dict[str, 'Blk360WealthModule'] = {}
        if module_id in self.blk360_wealth_modules:
            del self.blk360_wealth_modules[module_id]
            return True
        return False
    
    def create_blk360_legacy_entry(self, entry_data: 'Blk360LegacyEntryCreate') -> 'Blk360LegacyEntry':
        if not hasattr(self, 'blk360_legacy_entries'):
            self.blk360_legacy_entries: Dict[str, 'Blk360LegacyEntry'] = {}
        
        from app.models import Blk360LegacyEntry, LegacyEntryStatus
        entry_id = str(uuid.uuid4())
        entry = Blk360LegacyEntry(
            id=entry_id,
            user_email=entry_data.user_email,
            title=entry_data.title,
            honoree_name=entry_data.honoree_name,
            photo_url=entry_data.photo_url,
            story=entry_data.story,
            category=entry_data.category,
            status=LegacyEntryStatus.PENDING,
            featured=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_legacy_entries[entry_id] = entry
        return entry
    
    def get_all_blk360_legacy_entries(self, status: Optional['LegacyEntryStatus'] = None) -> List['Blk360LegacyEntry']:
        if not hasattr(self, 'blk360_legacy_entries'):
            self.blk360_legacy_entries: Dict[str, 'Blk360LegacyEntry'] = {}
        entries = list(self.blk360_legacy_entries.values())
        if status:
            entries = [e for e in entries if e.status == status]
        return entries
    
    def update_blk360_legacy_entry_status(self, entry_id: str, status: 'LegacyEntryStatus', featured: bool = False) -> Optional['Blk360LegacyEntry']:
        if not hasattr(self, 'blk360_legacy_entries'):
            self.blk360_legacy_entries: Dict[str, 'Blk360LegacyEntry'] = {}
        if entry_id in self.blk360_legacy_entries:
            self.blk360_legacy_entries[entry_id].status = status
            self.blk360_legacy_entries[entry_id].featured = featured
            self.blk360_legacy_entries[entry_id].updated_at = datetime.now()
            return self.blk360_legacy_entries[entry_id]
        return None
    
    def create_blk360_history_entry(self, entry_data: 'Blk360HistoryEntryCreate') -> 'Blk360HistoryEntry':
        if not hasattr(self, 'blk360_history_entries'):
            self.blk360_history_entries: Dict[str, 'Blk360HistoryEntry'] = {}
        
        from app.models import Blk360HistoryEntry, HistoryEntryStatus
        entry_id = str(uuid.uuid4())
        entry = Blk360HistoryEntry(
            id=entry_id,
            name=entry_data.name,
            field=entry_data.field,
            decade=entry_data.decade,
            biography=entry_data.biography,
            photo_url=entry_data.photo_url,
            source_url=entry_data.source_url,
            source_type=entry_data.source_type,
            status=HistoryEntryStatus.APPROVED,
            approved=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_history_entries[entry_id] = entry
        return entry
    
    def get_all_blk360_history_entries(self, approved_only: bool = True) -> List['Blk360HistoryEntry']:
        if not hasattr(self, 'blk360_history_entries'):
            self.blk360_history_entries: Dict[str, 'Blk360HistoryEntry'] = {}
        entries = list(self.blk360_history_entries.values())
        if approved_only:
            entries = [e for e in entries if e.approved]
        return entries
    
    def create_blk360_forum_post(self, post_data: 'Blk360ForumPostCreate') -> 'Blk360ForumPost':
        if not hasattr(self, 'blk360_forum_posts'):
            self.blk360_forum_posts: Dict[str, 'Blk360ForumPost'] = {}
        
        from app.models import Blk360ForumPost, Forum360PostStatus
        post_id = str(uuid.uuid4())
        post = Blk360ForumPost(
            id=post_id,
            title=post_data.title,
            content=post_data.content,
            category=post_data.category,
            author_name=post_data.author_name,
            author_email=post_data.author_email,
            status=Forum360PostStatus.ACTIVE,
            pinned=False,
            views=0,
            reply_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_forum_posts[post_id] = post
        return post
    
    def get_all_blk360_forum_posts(self, category: Optional['Forum360Category'] = None) -> List['Blk360ForumPost']:
        if not hasattr(self, 'blk360_forum_posts'):
            self.blk360_forum_posts: Dict[str, 'Blk360ForumPost'] = {}
        posts = list(self.blk360_forum_posts.values())
        if category:
            posts = [p for p in posts if p.category == category]
        posts.sort(key=lambda x: x.created_at, reverse=True)
        return posts
    
    def get_blk360_forum_post(self, post_id: str) -> Optional['Blk360ForumPost']:
        if not hasattr(self, 'blk360_forum_posts'):
            self.blk360_forum_posts: Dict[str, 'Blk360ForumPost'] = {}
        return self.blk360_forum_posts.get(post_id)
    
    def create_blk360_forum_reply(self, reply_data: 'Blk360ForumReplyCreate') -> 'Blk360ForumReply':
        if not hasattr(self, 'blk360_forum_replies'):
            self.blk360_forum_replies: Dict[str, 'Blk360ForumReply'] = {}
        
        from app.models import Blk360ForumReply
        reply_id = str(uuid.uuid4())
        reply = Blk360ForumReply(
            id=reply_id,
            post_id=reply_data.post_id,
            content=reply_data.content,
            author_name=reply_data.author_name,
            author_email=reply_data.author_email,
            created_at=datetime.now()
        )
        self.blk360_forum_replies[reply_id] = reply
        
        if reply_data.post_id in self.blk360_forum_posts:
            self.blk360_forum_posts[reply_data.post_id].reply_count += 1
        
        return reply
    
    def get_blk360_forum_replies(self, post_id: str) -> List['Blk360ForumReply']:
        if not hasattr(self, 'blk360_forum_replies'):
            self.blk360_forum_replies: Dict[str, 'Blk360ForumReply'] = {}
        replies = [r for r in self.blk360_forum_replies.values() if r.post_id == post_id]
        replies.sort(key=lambda x: x.created_at)
        return replies
    
    def get_blk360_analytics_metrics(self) -> 'Blk360AnalyticsMetrics':
        if not hasattr(self, 'blk360_subscriptions'):
            self.blk360_subscriptions: Dict[str, 'Blk360Subscription'] = {}
        if not hasattr(self, 'blk360_wealth_modules'):
            self.blk360_wealth_modules: Dict[str, 'Blk360WealthModule'] = {}
        if not hasattr(self, 'blk360_legacy_entries'):
            self.blk360_legacy_entries: Dict[str, 'Blk360LegacyEntry'] = {}
        if not hasattr(self, 'blk360_history_entries'):
            self.blk360_history_entries: Dict[str, 'Blk360HistoryEntry'] = {}
        if not hasattr(self, 'blk360_forum_posts'):
            self.blk360_forum_posts: Dict[str, 'Blk360ForumPost'] = {}
        if not hasattr(self, 'blk360_forum_replies'):
            self.blk360_forum_replies: Dict[str, 'Blk360ForumReply'] = {}
        
        from app.models import Blk360AnalyticsMetrics, SubscriptionTier, LegacyEntryStatus
        
        total_subs = len(self.blk360_subscriptions)
        premium_subs = len([s for s in self.blk360_subscriptions.values() if s.tier == SubscriptionTier.PREMIUM])
        elite_subs = len([s for s in self.blk360_subscriptions.values() if s.tier == SubscriptionTier.ELITE])
        monthly_revenue = (premium_subs * 9.99) + (elite_subs * 99.0)
        
        legacy_pending = len([e for e in self.blk360_legacy_entries.values() if e.status == LegacyEntryStatus.PENDING])
        legacy_approved = len([e for e in self.blk360_legacy_entries.values() if e.status == LegacyEntryStatus.APPROVED])
        
        return Blk360AnalyticsMetrics(
            total_subscriptions=total_subs,
            premium_subscribers=premium_subs,
            elite_subscribers=elite_subs,
            monthly_revenue=monthly_revenue,
            wealth_modules_count=len(self.blk360_wealth_modules),
            legacy_entries_pending=legacy_pending,
            legacy_entries_approved=legacy_approved,
            history_entries_count=len(self.blk360_history_entries),
            forum_posts_count=len(self.blk360_forum_posts),
            forum_replies_count=len(self.blk360_forum_replies)
        )

    
    # Phase 3: Community Hub, Wallet, Governance, Fund Methods
    
    def create_blk360_wallet(self, wallet_data: Blk360WalletCreate) -> Blk360Wallet:
        wallet_id = str(uuid.uuid4())
        wallet = Blk360Wallet(
            id=wallet_id,
            user_id=wallet_data.user_id,
            balance=0,
            lifetime_earned=0,
            lifetime_spent=0,
            transactions=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_wallets[wallet_id] = wallet
        return wallet
    
    def get_blk360_wallet_by_user(self, user_id: str) -> Optional[Blk360Wallet]:
        for wallet in self.blk360_wallets.values():
            if wallet.user_id == user_id:
                return wallet
        return None
    
    def add_wallet_transaction(self, user_id: str, transaction_type: str, amount: int, description: str, category: str) -> Optional[Blk360Wallet]:
        wallet = self.get_blk360_wallet_by_user(user_id)
        if not wallet:
            wallet = self.create_blk360_wallet(Blk360WalletCreate(user_id=user_id))
        
        transaction = Blk360WalletTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=transaction_type,
            amount=amount,
            description=description,
            category=category,
            timestamp=datetime.now()
        )
        
        wallet.transactions.append(transaction)
        if transaction_type == 'earned':
            wallet.balance += amount
            wallet.lifetime_earned += amount
        elif transaction_type == 'spent':
            wallet.balance -= amount
            wallet.lifetime_spent += amount
        wallet.updated_at = datetime.now()
        
        return wallet
    
    def create_blk360_event(self, event_data: Blk360EventCreate) -> Blk360Event:
        event_id = str(uuid.uuid4())
        event = Blk360Event(
            id=event_id,
            title=event_data.title,
            description=event_data.description,
            date=event_data.date,
            time=event_data.time,
            location=event_data.location,
            category=event_data.category,
            image_url=event_data.image_url,
            rsvp_count=0,
            status='upcoming',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.blk360_events[event_id] = event
        return event
    
    def get_all_blk360_events(self) -> List[Blk360Event]:
        return list(self.blk360_events.values())
    
    def increment_event_rsvp(self, event_id: str) -> Optional[Blk360Event]:
        if event_id in self.blk360_events:
            self.blk360_events[event_id].rsvp_count += 1
            return self.blk360_events[event_id]
        return None
    
    def create_blk360_proposal(self, proposal_data: Blk360ProposalCreate) -> Blk360Proposal:
        from datetime import timedelta
        proposal_id = str(uuid.uuid4())
        deadline = (datetime.now() + timedelta(days=14)).isoformat()
        proposal = Blk360Proposal(
            id=proposal_id,
            title=proposal_data.title,
            summary=proposal_data.summary,
            description=proposal_data.description,
            category=proposal_data.category,
            status='active',
            created_by=proposal_data.created_by,
            created_at=datetime.now(),
            deadline=deadline,
            votes_for=0,
            votes_against=0,
            votes_abstain=0,
            total_votes=0,
            quorum_required=100
        )
        self.blk360_proposals[proposal_id] = proposal
        return proposal
    
    def get_all_blk360_proposals(self, status: Optional[str] = None) -> List[Blk360Proposal]:
        proposals = list(self.blk360_proposals.values())
        if status:
            proposals = [p for p in proposals if p.status == status]
        return proposals
    
    def create_blk360_vote(self, vote_data: Blk360VoteCreate) -> Blk360Vote:
        vote_id = str(uuid.uuid4())
        vote = Blk360Vote(
            id=vote_id,
            proposal_id=vote_data.proposal_id,
            user_id=vote_data.user_id,
            vote=vote_data.vote,
            timestamp=datetime.now()
        )
        self.blk360_votes[vote_id] = vote
        
        if vote_data.proposal_id in self.blk360_proposals:
            proposal = self.blk360_proposals[vote_data.proposal_id]
            if vote_data.vote == 'for':
                proposal.votes_for += 1
            elif vote_data.vote == 'against':
                proposal.votes_against += 1
            elif vote_data.vote == 'abstain':
                proposal.votes_abstain += 1
            proposal.total_votes += 1
        
        return vote
    
    def create_blk360_fund_donation(self, donation_data: Blk360FundDonationCreate) -> Blk360FundDonation:
        donation_id = str(uuid.uuid4())
        donation = Blk360FundDonation(
            id=donation_id,
            donor_name=donation_data.donor_name,
            email=donation_data.email,
            amount=donation_data.amount,
            category=donation_data.category,
            anonymous=donation_data.anonymous,
            timestamp=datetime.now()
        )
        self.blk360_fund_donations[donation_id] = donation
        return donation
    
    def get_all_blk360_fund_donations(self) -> List[Blk360FundDonation]:
        return list(self.blk360_fund_donations.values())
    
    def get_blk360_fund_metrics(self) -> Blk360FundMetrics:
        total_raised = sum(d.amount for d in self.blk360_fund_donations.values())
        vendor_allocation = total_raised * 0.85
        operations_allocation = total_raised * 0.12
        hbcu_allocation = total_raised * 0.03
        
        return Blk360FundMetrics(
            total_raised=total_raised,
            vendor_allocation=vendor_allocation,
            operations_allocation=operations_allocation,
            hbcu_allocation=hbcu_allocation,
            total_vendors_supported=len(self.vendors),
            total_hbcus_supported=5,
            monthly_growth=12.5
        )
    
    def create_blk360_group(self, group_data: Blk360GroupCreate) -> Blk360Group:
        group_id = str(uuid.uuid4())
        group = Blk360Group(
            id=group_id,
            name=group_data.name,
            description=group_data.description,
            visibility=group_data.visibility,
            created_by=group_data.created_by,
            member_count=1,
            created_at=datetime.now()
        )
        self.blk360_groups[group_id] = group
        return group
    
    def get_all_blk360_groups(self) -> List[Blk360Group]:
        return list(self.blk360_groups.values())
    
    def create_blk360_membership(self, membership_data: Blk360MembershipCreate) -> Blk360Membership:
        membership_id = str(uuid.uuid4())
        membership = Blk360Membership(
            id=membership_id,
            user_id=membership_data.user_id,
            tier=membership_data.tier,
            consent_timestamp=datetime.now(),
            terms_accepted=membership_data.terms_accepted,
            agreement_date=datetime.now()
        )
        self.blk360_memberships[membership_id] = membership
        return membership
    
    def get_blk360_membership_by_user(self, user_id: str) -> Optional[Blk360Membership]:
        for membership in self.blk360_memberships.values():
            if membership.user_id == user_id:
                return membership
        return None
    
    def setup_2fa(self, user_id: str, method: str, secret_hash: str, recovery_codes: List[str]) -> 'Blk360TwoFA':
        from app.models import Blk360TwoFA
        from datetime import timedelta
        
        twofa = Blk360TwoFA(
            user_id=user_id,
            method=method,
            secret_hash=secret_hash,
            recovery_codes=recovery_codes,
            enabled=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            grace_period_expires=datetime.now() + timedelta(days=30),
            device_id=None
        )
        self.blk360_2fa[user_id] = twofa
        return twofa
    
    def get_2fa_by_user(self, user_id: str) -> Optional['Blk360TwoFA']:
        return self.blk360_2fa.get(user_id)
    
    def disable_2fa(self, user_id: str) -> bool:
        if user_id in self.blk360_2fa:
            del self.blk360_2fa[user_id]
            return True
        return False
    
    def log_audit_event(self, user_id: str, event: str, status: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        from app.models import Blk360AuditLog
        
        log_id = str(uuid.uuid4())
        audit_log = Blk360AuditLog(
            id=log_id,
            user_id=user_id,
            event=event,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now()
        )
        self.blk360_audit_logs[log_id] = audit_log
        return audit_log
    
    def get_audit_logs_by_user(self, user_id: str) -> List['Blk360AuditLog']:
        return [log for log in self.blk360_audit_logs.values() if log.user_id == user_id]
    
    
    def create_subscription(self, subscription_data: dict) -> dict:
        """Create a new subscription"""
        subscription_id = str(uuid.uuid4())
        subscription = {
            "id": subscription_id,
            "user_id": subscription_data["user_id"],
            "plan_type": subscription_data["plan_type"],
            "stripe_subscription_id": subscription_data.get("stripe_subscription_id", f"sub_test_{subscription_id[:8]}"),
            "status": subscription_data.get("status", "active"),
            "current_period_start": datetime.now(),
            "current_period_end": datetime.now(),
            "cancel_at_period_end": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        if not hasattr(self, 'subscriptions'):
            self.subscriptions = {}
        self.subscriptions[subscription_id] = subscription
        return subscription
    
    def get_subscription(self, subscription_id: str) -> Optional[dict]:
        """Get subscription by ID"""
        if not hasattr(self, 'subscriptions'):
            self.subscriptions = {}
        return self.subscriptions.get(subscription_id)
    
    def get_subscription_by_user(self, user_id: str) -> Optional[dict]:
        """Get active subscription for a user"""
        if not hasattr(self, 'subscriptions'):
            self.subscriptions = {}
        for sub in self.subscriptions.values():
            if sub["user_id"] == user_id and sub["status"] == "active":
                return sub
        return None
    
    def update_subscription_status(self, subscription_id: str, status: str) -> bool:
        """Update subscription status"""
        if not hasattr(self, 'subscriptions'):
            self.subscriptions = {}
        if subscription_id in self.subscriptions:
            self.subscriptions[subscription_id]["status"] = status
            self.subscriptions[subscription_id]["updated_at"] = datetime.now()
            return True
        return False
    
    def create_payout(self, payout_data: dict) -> dict:
        """Create a vendor payout"""
        payout_id = str(uuid.uuid4())
        payout = {
            "id": payout_id,
            "vendor_id": payout_data["vendor_id"],
            "amount": payout_data["amount"],
            "stripe_payout_id": payout_data.get("stripe_payout_id", f"po_test_{payout_id[:8]}"),
            "status": payout_data.get("status", "pending"),
            "scheduled_date": payout_data.get("scheduled_date", datetime.now()),
            "completed_date": None,
            "created_at": datetime.now()
        }
        if not hasattr(self, 'payouts'):
            self.payouts = {}
        self.payouts[payout_id] = payout
        return payout
    
    def get_payout(self, payout_id: str) -> Optional[dict]:
        """Get payout by ID"""
        if not hasattr(self, 'payouts'):
            self.payouts = {}
        return self.payouts.get(payout_id)
    
    def get_payouts_by_vendor(self, vendor_id: str) -> List[dict]:
        """Get all payouts for a vendor"""
        if not hasattr(self, 'payouts'):
            self.payouts = {}
        return [p for p in self.payouts.values() if p["vendor_id"] == vendor_id]
    
    def update_payout_status(self, payout_id: str, status: str) -> bool:
        """Update payout status"""
        if not hasattr(self, 'payouts'):
            self.payouts = {}
        if payout_id in self.payouts:
            self.payouts[payout_id]["status"] = status
            if status == "completed":
                self.payouts[payout_id]["completed_date"] = datetime.now()
            return True
        return False
    
    def create_affiliate(self, affiliate_data: dict) -> dict:
        """Create affiliate account"""
        affiliate_id = str(uuid.uuid4())
        affiliate = {
            "id": affiliate_id,
            "user_id": affiliate_data["user_id"],
            "referral_code": affiliate_data["referral_code"],
            "total_clicks": 0,
            "total_conversions": 0,
            "total_earnings": 0.0,
            "status": "active",
            "created_at": datetime.now()
        }
        if not hasattr(self, 'affiliates'):
            self.affiliates = {}
        self.affiliates[affiliate_id] = affiliate
        return affiliate
    
    def get_affiliate_by_user(self, user_id: str) -> Optional[dict]:
        """Get affiliate by user ID"""
        if not hasattr(self, 'affiliates'):
            self.affiliates = {}
        for aff in self.affiliates.values():
            if aff["user_id"] == user_id:
                return aff
        return None
    
    def get_affiliate_by_code(self, referral_code: str) -> Optional[dict]:
        """Get affiliate by referral code"""
        if not hasattr(self, 'affiliates'):
            self.affiliates = {}
        for aff in self.affiliates.values():
            if aff["referral_code"] == referral_code:
                return aff
        return None
    
    def track_affiliate_click(self, referral_code: str) -> bool:
        """Track affiliate click"""
        affiliate = self.get_affiliate_by_code(referral_code)
        if affiliate:
            affiliate["total_clicks"] += 1
            return True
        return False
    
    def track_affiliate_conversion(self, referral_code: str, earnings: float) -> bool:
        """Track affiliate conversion"""
        affiliate = self.get_affiliate_by_code(referral_code)
        if affiliate:
            affiliate["total_conversions"] += 1
            affiliate["total_earnings"] += earnings
            return True
        return False
    
    def create_ai_history(self, history_data: dict) -> dict:
        """Create AI-generated history content"""
        history_id = str(uuid.uuid4())
        history = {
            "id": history_id,
            "title": history_data["title"],
            "content": history_data["content"],
            "source_url": history_data.get("source_url"),
            "status": "pending",
            "created_at": datetime.now(),
            "approved_at": None,
            "approved_by": None
        }
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        self.ai_history[history_id] = history
        return history
    
    def get_ai_history(self, history_id: str) -> Optional[dict]:
        """Get AI history by ID"""
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        return self.ai_history.get(history_id)
    
    def get_all_ai_history(self, status: Optional[str] = None) -> List[dict]:
        """Get all AI history, optionally filtered by status"""
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        if status:
            return [h for h in self.ai_history.values() if h["status"] == status]
        return list(self.ai_history.values())
    
    def approve_ai_history(self, history_id: str, admin_id: str) -> bool:
        """Approve AI history content"""
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        if history_id in self.ai_history:
            self.ai_history[history_id]["status"] = "approved"
            self.ai_history[history_id]["approved_at"] = datetime.now()
            self.ai_history[history_id]["approved_by"] = admin_id
            return True
        return False
    
    def reject_ai_history(self, history_id: str) -> bool:
        """Reject AI history content"""
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        if history_id in self.ai_history:
            self.ai_history[history_id]["status"] = "rejected"
            return True
        return False
    
    def create_ai_mentorship(self, mentorship_data: dict) -> dict:
        """Create AI mentor match"""
        match_id = str(uuid.uuid4())
        mentorship = {
            "id": match_id,
            "mentee_id": mentorship_data["mentee_id"],
            "mentor_id": mentorship_data["mentor_id"],
            "match_score": mentorship_data["match_score"],
            "status": "pending",
            "created_at": datetime.now(),
            "approved_at": None
        }
        if not hasattr(self, 'ai_mentorships'):
            self.ai_mentorships = {}
        self.ai_mentorships[match_id] = mentorship
        return mentorship
    
    def get_ai_mentorship(self, match_id: str) -> Optional[dict]:
        """Get AI mentorship by ID"""
        if not hasattr(self, 'ai_mentorships'):
            self.ai_mentorships = {}
        return self.ai_mentorships.get(match_id)
    
    def get_all_ai_mentorships(self, status: Optional[str] = None) -> List[dict]:
        """Get all AI mentorships, optionally filtered by status"""
        if not hasattr(self, 'ai_mentorships'):
            self.ai_mentorships = {}
        if status:
            return [m for m in self.ai_mentorships.values() if m["status"] == status]
        return list(self.ai_mentorships.values())
    
    def approve_ai_mentorship(self, match_id: str) -> bool:
        """Approve AI mentorship match"""
        if not hasattr(self, 'ai_mentorships'):
            self.ai_mentorships = {}
        if match_id in self.ai_mentorships:
            self.ai_mentorships[match_id]["status"] = "approved"
            self.ai_mentorships[match_id]["approved_at"] = datetime.now()
            return True
        return False
    
    def reject_ai_mentorship(self, match_id: str) -> bool:
        """Reject AI mentorship match"""
        if not hasattr(self, 'ai_mentorships'):
            self.ai_mentorships = {}
        if match_id in self.ai_mentorships:
            self.ai_mentorships[match_id]["status"] = "rejected"
            return True
        return False
    
    def create_ai_content(self, content_data: dict) -> dict:
        """Create AI-generated content"""
        content_id = str(uuid.uuid4())
        content = {
            "id": content_id,
            "content_type": content_data["content_type"],
            "title": content_data["title"],
            "body": content_data["body"],
            "status": "pending",
            "created_at": datetime.now(),
            "approved_at": None,
            "approved_by": None
        }
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        self.ai_content[content_id] = content
        return content
    
    def get_ai_content(self, content_id: str) -> Optional[dict]:
        """Get AI content by ID"""
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        return self.ai_content.get(content_id)
    
    def get_all_ai_content(self, status: Optional[str] = None, content_type: Optional[str] = None) -> List[dict]:
        """Get all AI content, optionally filtered"""
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        results = list(self.ai_content.values())
        if status:
            results = [c for c in results if c["status"] == status]
        if content_type:
            results = [c for c in results if c["content_type"] == content_type]
        return results
    
    def approve_ai_content(self, content_id: str, admin_id: str) -> bool:
        """Approve AI content"""
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        if content_id in self.ai_content:
            self.ai_content[content_id]["status"] = "approved"
            self.ai_content[content_id]["approved_at"] = datetime.now()
            self.ai_content[content_id]["approved_by"] = admin_id
            return True
        return False
    
    def reject_ai_content(self, content_id: str) -> bool:
        """Reject AI content"""
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        if content_id in self.ai_content:
            self.ai_content[content_id]["status"] = "rejected"
            return True
        return False
    
    def get_impact_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
        """Get platform impact metrics (start_date and end_date are placeholders for MVP)"""
        if not hasattr(self, 'subscriptions'):
            self.subscriptions = {}
        if not hasattr(self, 'payouts'):
            self.payouts = {}
        if not hasattr(self, 'affiliates'):
            self.affiliates = {}
        if not hasattr(self, 'ai_history'):
            self.ai_history = {}
        if not hasattr(self, 'ai_content'):
            self.ai_content = {}
        
        total_subscriptions = len([s for s in self.subscriptions.values() if s["status"] == "active"])
        total_payouts = sum(p["amount"] for p in self.payouts.values() if p["status"] == "completed")
        total_affiliates = len(self.affiliates)
        total_affiliate_earnings = sum(a["total_earnings"] for a in self.affiliates.values())
        approved_history = len([h for h in self.ai_history.values() if h["status"] == "approved"])
        approved_content = len([c for c in self.ai_content.values() if c["status"] == "approved"])
        
        return {
            "total_subscriptions": total_subscriptions,
            "total_payouts_amount": total_payouts,
            "total_affiliates": total_affiliates,
            "total_affiliate_earnings": total_affiliate_earnings,
            "approved_history_count": approved_history,
            "approved_content_count": approved_content,
            "total_vendors": len(self.vendors),
            "total_products": len(self.products),
            "total_orders": len(self.orders),
            "community_fund_total": self.impact_stats.get("total_donations", 0.0)
        }
    
    def track_payment_metadata(self, metadata: dict) -> dict:
        """Track payment metadata for audit"""
        payment_id = str(uuid.uuid4())
        payment = {
            "id": payment_id,
            "payment_type": metadata["payment_type"],
            "stripe_payment_id": metadata.get("stripe_payment_id"),
            "amount": metadata["amount"],
            "status": metadata.get("status", "pending"),
            "user_id": metadata.get("user_id"),
            "vendor_id": metadata.get("vendor_id"),
            "metadata": metadata.get("metadata", {}),
            "created_at": datetime.now()
        }
        if not hasattr(self, 'payment_metadata'):
            self.payment_metadata = {}
        self.payment_metadata[payment_id] = payment
        return payment
    
    def _seed_blkcoin_rewards(self):
        """Seed default BlkCoin reward amounts"""
        rewards = [
            {"activity_type": "wealth_module_complete", "amount": 50.0, "description": "Complete a Wealth Hub module"},
            {"activity_type": "event_rsvp", "amount": 10.0, "description": "RSVP to a community event"},
            {"activity_type": "event_attend", "amount": 25.0, "description": "Attend a community event"},
            {"activity_type": "vendor_referral", "amount": 100.0, "description": "Refer a new vendor"},
            {"activity_type": "partner_referral", "amount": 75.0, "description": "Refer a new partner"},
            {"activity_type": "donation", "amount": 20.0, "description": "Make a donation (per $10 donated)"},
            {"activity_type": "forum_post", "amount": 5.0, "description": "Create a forum post"},
            {"activity_type": "forum_comment", "amount": 2.0, "description": "Comment on a forum post"},
            {"activity_type": "scholarship_application", "amount": 15.0, "description": "Submit a scholarship application"},
        ]
        for reward in rewards:
            self.create_blkcoin_reward(reward["activity_type"], reward["amount"], reward["description"])
    
    def create_blkcoin_wallet(self, user_id: str, email: str):
        """Create a new BlkCoin wallet for a user"""
        wallet_id = str(uuid.uuid4())
        wallet = {
            "id": wallet_id,
            "user_id": user_id,
            "email": email,
            "balance": 0.0,
            "lifetime_earned": 0.0,
            "lifetime_redeemed": 0.0,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        self.blk360_blkcoin_wallets[wallet_id] = wallet
        return wallet
    
    def get_blkcoin_wallet(self, user_id: str):
        """Get BlkCoin wallet by user_id"""
        for wallet in self.blk360_blkcoin_wallets.values():
            if wallet["user_id"] == user_id:
                return wallet
        return None
    
    def update_blkcoin_balance(self, user_id: str, amount: float, transaction_type: str, activity_type: str, reason: str, metadata: dict = None):
        """Update BlkCoin balance and create transaction record"""
        wallet = self.get_blkcoin_wallet(user_id)
        if not wallet:
            return None
        
        if transaction_type == "earn":
            wallet["balance"] += amount
            wallet["lifetime_earned"] += amount
        elif transaction_type == "redeem":
            if wallet["balance"] < amount:
                return None
            wallet["balance"] -= amount
            wallet["lifetime_redeemed"] += amount
        
        wallet["last_updated"] = datetime.now().isoformat()
        
        tx_id = str(uuid.uuid4())
        transaction = {
            "id": tx_id,
            "user_id": user_id,
            "transaction_type": transaction_type,
            "activity_type": activity_type,
            "amount": amount,
            "balance_after": wallet["balance"],
            "reason": reason,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        self.blk360_blkcoin_transactions[tx_id] = transaction
        
        return wallet
    
    def get_blkcoin_transactions(self, user_id: str, limit: int = 50):
        """Get transaction history for a user"""
        transactions = [
            tx for tx in self.blk360_blkcoin_transactions.values()
            if tx["user_id"] == user_id
        ]
        transactions.sort(key=lambda x: x["created_at"], reverse=True)
        return transactions[:limit]
    
    def get_blkcoin_reward_amount(self, activity_type: str):
        """Get reward amount for an activity type"""
        for reward in self.blk360_blkcoin_rewards.values():
            if reward["activity_type"] == activity_type and reward["is_active"]:
                return reward["amount"]
        return 0.0
    
    def create_blkcoin_reward(self, activity_type: str, amount: float, description: str):
        """Create a new BlkCoin reward rule"""
        reward_id = str(uuid.uuid4())
        reward = {
            "id": reward_id,
            "activity_type": activity_type,
            "amount": amount,
            "description": description,
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        self.blk360_blkcoin_rewards[reward_id] = reward
        return reward
    
    def create_scholarship(self, title: str, description: str, amount: float, deadline: str, goal_category: str, requirements: str, eligibility_criteria: str):
        """Create a new scholarship"""
        scholarship_id = str(uuid.uuid4())
        scholarship = {
            "id": scholarship_id,
            "title": title,
            "description": description,
            "amount": amount,
            "deadline": deadline,
            "goal_category": goal_category,
            "requirements": requirements,
            "eligibility_criteria": eligibility_criteria,
            "status": "open",
            "total_raised": 0.0,
            "applications_count": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.blk360_scholarships[scholarship_id] = scholarship
        return scholarship
    
    def get_scholarship(self, scholarship_id: str):
        """Get scholarship by ID"""
        return self.blk360_scholarships.get(scholarship_id)
    
    def get_scholarships(self, status: str = None):
        """Get all scholarships, optionally filtered by status"""
        scholarships = list(self.blk360_scholarships.values())
        if status:
            scholarships = [s for s in scholarships if s["status"] == status]
        scholarships.sort(key=lambda x: x["created_at"], reverse=True)
        return scholarships
    
    def update_scholarship(self, scholarship_id: str, updates: dict):
        """Update scholarship"""
        scholarship = self.blk360_scholarships.get(scholarship_id)
        if not scholarship:
            return None
        scholarship.update(updates)
        scholarship["updated_at"] = datetime.now().isoformat()
        return scholarship
    
    def create_scholarship_application(self, user_id: str, scholarship_id: str, applicant_name: str, email: str, phone: str, essay: str, goal_category: str, amount_requested: float, additional_info: str = None):
        """Create a scholarship application"""
        application_id = str(uuid.uuid4())
        scholarship = self.get_scholarship(scholarship_id)
        
        application = {
            "id": application_id,
            "user_id": user_id,
            "scholarship_id": scholarship_id,
            "scholarship_title": scholarship["title"] if scholarship else None,
            "applicant_name": applicant_name,
            "email": email,
            "phone": phone,
            "essay": essay,
            "goal_category": goal_category,
            "amount_requested": amount_requested,
            "additional_info": additional_info,
            "status": "pending",
            "admin_notes": None,
            "reviewed_by": None,
            "reviewed_at": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.blk360_scholarship_applications[application_id] = application
        
        if scholarship:
            scholarship["applications_count"] += 1
        
        return application
    
    def get_scholarship_application(self, application_id: str):
        """Get scholarship application by ID"""
        return self.blk360_scholarship_applications.get(application_id)
    
    def get_scholarship_applications(self, scholarship_id: str = None, status: str = None):
        """Get scholarship applications, optionally filtered"""
        applications = list(self.blk360_scholarship_applications.values())
        if scholarship_id:
            applications = [a for a in applications if a["scholarship_id"] == scholarship_id]
        if status:
            applications = [a for a in applications if a["status"] == status]
        applications.sort(key=lambda x: x["created_at"], reverse=True)
        return applications
    
    def update_scholarship_application(self, application_id: str, status: str, admin_notes: str = None, reviewed_by: str = None, award_amount: float = None):
        """Update scholarship application status"""
        application = self.blk360_scholarship_applications.get(application_id)
        if not application:
            return None
        
        application["status"] = status
        application["admin_notes"] = admin_notes
        application["reviewed_by"] = reviewed_by
        application["reviewed_at"] = datetime.now().isoformat()
        application["updated_at"] = datetime.now().isoformat()
        
        if award_amount:
            application["award_amount"] = award_amount
        
        return application
    
    def create_scholarship_donation(self, user_id: str, scholarship_id: str, donor_name: str, email: str, amount: float, is_anonymous: bool = False):
        """Create a scholarship donation"""
        donation_id = str(uuid.uuid4())
        scholarship = self.get_scholarship(scholarship_id)
        
        donation = {
            "id": donation_id,
            "user_id": user_id,
            "scholarship_id": scholarship_id,
            "scholarship_title": scholarship["title"] if scholarship else None,
            "donor_name": donor_name,
            "email": email,
            "amount": amount,
            "is_anonymous": is_anonymous,
            "created_at": datetime.now().isoformat()
        }
        self.blk360_scholarship_donations[donation_id] = donation
        
        if scholarship:
            scholarship["total_raised"] += amount
        
        return donation
    
    def get_scholarship_donations(self, scholarship_id: str = None):
        """Get scholarship donations"""
        donations = list(self.blk360_scholarship_donations.values())
        if scholarship_id:
            donations = [d for d in donations if d["scholarship_id"] == scholarship_id]
        donations.sort(key=lambda x: x["created_at"], reverse=True)
        return donations
    
    def get_impact_metrics_v2(self, start_date: str, end_date: str):
        """Get comprehensive impact metrics including Phase 5B data"""
        base_metrics = self.get_impact_metrics(start_date, end_date)
        
        total_blkcoin_circulating = sum(w["balance"] for w in self.blk360_blkcoin_wallets.values())
        total_blkcoin_earned = sum(w["lifetime_earned"] for w in self.blk360_blkcoin_wallets.values())
        total_blkcoin_redeemed = sum(w["lifetime_redeemed"] for w in self.blk360_blkcoin_wallets.values())
        active_wallets = len([w for w in self.blk360_blkcoin_wallets.values() if w["balance"] > 0])
        
        total_scholarships = len(self.blk360_scholarships)
        open_scholarships = len([s for s in self.blk360_scholarships.values() if s["status"] == "open"])
        total_scholarship_funds = sum(s["total_raised"] for s in self.blk360_scholarships.values())
        total_applications = len(self.blk360_scholarship_applications)
        approved_applications = len([a for a in self.blk360_scholarship_applications.values() if a["status"] == "approved"])
        
        return {
            **base_metrics,
            "blkcoin": {
                "total_circulating": total_blkcoin_circulating,
                "total_earned": total_blkcoin_earned,
                "total_redeemed": total_blkcoin_redeemed,
                "active_wallets": active_wallets,
                "total_wallets": len(self.blk360_blkcoin_wallets)
            },
            "scholarships": {
                "total_scholarships": total_scholarships,
                "open_scholarships": open_scholarships,
                "total_funds_raised": total_scholarship_funds,
                "total_applications": total_applications,
                "approved_applications": approved_applications,
                "pending_applications": len([a for a in self.blk360_scholarship_applications.values() if a["status"] == "pending"])
            }
        }
    
    def create_event_enhanced(self, title: str, description: str, category: str, location: str, 
                             start_time: str, end_time: str, rsvp_limit: int = None, 
                             ticket_price: float = 0.0, image_url: str = None, 
                             is_volunteer_event: bool = False, blkcoin_reward: float = None):
        event_id = str(uuid.uuid4())
        event = {
            "id": event_id,
            "title": title,
            "description": description,
            "category": category,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
            "rsvp_count": 0,
            "rsvp_limit": rsvp_limit,
            "ticket_price": ticket_price,
            "image_url": image_url,
            "is_volunteer_event": is_volunteer_event,
            "blkcoin_reward": blkcoin_reward or (25.0 if is_volunteer_event else 10.0),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.blk360_events_enhanced[event_id] = event
        return event
    
    def get_event_enhanced(self, event_id: str):
        return self.blk360_events_enhanced.get(event_id)
    
    def get_all_events_enhanced(self, category: str = None, upcoming_only: bool = False):
        events = list(self.blk360_events_enhanced.values())
        if category:
            events = [e for e in events if e["category"] == category]
        if upcoming_only:
            now = datetime.now().isoformat()
            events = [e for e in events if e["start_time"] > now]
        events.sort(key=lambda x: x["start_time"])
        return events
    
    def update_event_enhanced(self, event_id: str, updates: dict):
        event = self.blk360_events_enhanced.get(event_id)
        if not event:
            return None
        event.update(updates)
        event["updated_at"] = datetime.now().isoformat()
        return event
    
    def delete_event_enhanced(self, event_id: str):
        if event_id in self.blk360_events_enhanced:
            del self.blk360_events_enhanced[event_id]
            return True
        return False
    
    def create_partner(self, name: str, category: str, mission: str, website: str, 
                      contact_name: str, contact_email: str, contact_phone: str, 
                      logo_url: str, description: str):
        partner_id = str(uuid.uuid4())
        partner = {
            "id": partner_id,
            "name": name,
            "category": category,
            "mission": mission,
            "website": website,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "logo_url": logo_url,
            "description": description,
            "status": "pending",
            "badge_level": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.blk360_partners[partner_id] = partner
        return partner
    
    def get_partner(self, partner_id: str):
        return self.blk360_partners.get(partner_id)
    
    def get_all_partners(self, status: str = None, category: str = None):
        partners = list(self.blk360_partners.values())
        if status:
            partners = [p for p in partners if p["status"] == status]
        if category:
            partners = [p for p in partners if p["category"] == category]
        partners.sort(key=lambda x: x["created_at"], reverse=True)
        return partners
    
    def update_partner(self, partner_id: str, updates: dict):
        partner = self.blk360_partners.get(partner_id)
        if not partner:
            return None
        partner.update(updates)
        partner["updated_at"] = datetime.now().isoformat()
        return partner
    
    def create_nonprofit(self, name: str, ein: str, focus_area: str, mission: str, 
                        website: str, contact_name: str, contact_email: str, 
                        contact_phone: str, logo_url: str, description: str, 
                        address: str, city: str, state: str, zip_code: str):
        nonprofit_id = str(uuid.uuid4())
        nonprofit = {
            "id": nonprofit_id,
            "name": name,
            "ein": ein,
            "focus_area": focus_area,
            "mission": mission,
            "website": website,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "logo_url": logo_url,
            "description": description,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_code,
            "status": "pending",
            "total_donations": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.blk360_nonprofits[nonprofit_id] = nonprofit
        return nonprofit
    
    def get_nonprofit(self, nonprofit_id: str):
        return self.blk360_nonprofits.get(nonprofit_id)
    
    def get_all_nonprofits(self, status: str = None, focus_area: str = None):
        nonprofits = list(self.blk360_nonprofits.values())
        if status:
            nonprofits = [n for n in nonprofits if n["status"] == status]
        if focus_area:
            nonprofits = [n for n in nonprofits if n["focus_area"] == focus_area]
        nonprofits.sort(key=lambda x: x["created_at"], reverse=True)
        return nonprofits
    
    def update_nonprofit(self, nonprofit_id: str, updates: dict):
        nonprofit = self.blk360_nonprofits.get(nonprofit_id)
        if not nonprofit:
            return None
        nonprofit.update(updates)
        nonprofit["updated_at"] = datetime.now().isoformat()
        return nonprofit
    
    def create_volunteer_log(self, user_id: str, event_id: str, hours: float, notes: str = None):
        log_id = str(uuid.uuid4())
        event = self.get_event_enhanced(event_id)
        blkcoin_earned = hours * 10.0
        
        log = {
            "id": log_id,
            "user_id": user_id,
            "event_id": event_id,
            "event_title": event["title"] if event else None,
            "hours": hours,
            "notes": notes,
            "blkcoin_earned": blkcoin_earned,
            "created_at": datetime.now().isoformat()
        }
        self.blk360_volunteer_logs[log_id] = log
        
        wallet = self.get_blkcoin_wallet(user_id)
        if wallet:
            self.update_blkcoin_balance(
                user_id=user_id,
                amount=blkcoin_earned,
                transaction_type="earn",
                activity_type="volunteer",
                reason=f"Volunteered {hours} hours at {event['title'] if event else 'event'}",
                metadata={"event_id": event_id, "hours": hours}
            )
        
        return log
    
    def get_volunteer_logs(self, user_id: str = None, event_id: str = None):
        logs = list(self.blk360_volunteer_logs.values())
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        if event_id:
            logs = [l for l in logs if l["event_id"] == event_id]
        logs.sort(key=lambda x: x["created_at"], reverse=True)
        return logs
    
    def create_donation_enhanced(self, user_id: str, recipient_type: str, recipient_id: str, 
                                donor_name: str, email: str, amount: float, 
                                is_anonymous: bool = False, message: str = None):
        donation_id = str(uuid.uuid4())
        
        recipient_name = None
        if recipient_type == "partner":
            partner = self.get_partner(recipient_id)
            recipient_name = partner["name"] if partner else None
        elif recipient_type == "nonprofit":
            nonprofit = self.get_nonprofit(recipient_id)
            recipient_name = nonprofit["name"] if nonprofit else None
            if nonprofit:
                nonprofit["total_donations"] += amount
        elif recipient_type == "event":
            event = self.get_event_enhanced(recipient_id)
            recipient_name = event["title"] if event else None
        elif recipient_type == "scholarship":
            scholarship = self.get_scholarship(recipient_id)
            recipient_name = scholarship["title"] if scholarship else None
        
        blkcoin_earned = (amount // 10) * 20
        
        donation = {
            "id": donation_id,
            "user_id": user_id,
            "recipient_type": recipient_type,
            "recipient_id": recipient_id,
            "recipient_name": recipient_name,
            "donor_name": donor_name,
            "email": email,
            "amount": amount,
            "is_anonymous": is_anonymous,
            "message": message,
            "blkcoin_earned": blkcoin_earned,
            "created_at": datetime.now().isoformat()
        }
        self.blk360_donations[donation_id] = donation
        
        wallet = self.get_blkcoin_wallet(user_id)
        if wallet and blkcoin_earned > 0:
            self.update_blkcoin_balance(
                user_id=user_id,
                amount=blkcoin_earned,
                transaction_type="earn",
                activity_type="donation",
                reason=f"Donated ${amount} to {recipient_name or recipient_type}",
                metadata={"recipient_type": recipient_type, "recipient_id": recipient_id, "amount": amount}
            )
        
        return donation
    
    def get_donations_enhanced(self, recipient_type: str = None, recipient_id: str = None, user_id: str = None):
        donations = list(self.blk360_donations.values())
        if recipient_type:
            donations = [d for d in donations if d["recipient_type"] == recipient_type]
        if recipient_id:
            donations = [d for d in donations if d["recipient_id"] == recipient_id]
        if user_id:
            donations = [d for d in donations if d["user_id"] == user_id]
        donations.sort(key=lambda x: x["created_at"], reverse=True)
        return donations
    
    def get_impact_metrics_v3(self, start_date: str, end_date: str):
        v2_metrics = self.get_impact_metrics_v2(start_date, end_date)
        
        total_events = len(self.blk360_events_enhanced)
        upcoming_events = len([e for e in self.blk360_events_enhanced.values() if e["start_time"] > datetime.now().isoformat()])
        total_rsvps = sum(e["rsvp_count"] for e in self.blk360_events_enhanced.values())
        
        active_partners = len([p for p in self.blk360_partners.values() if p["status"] == "active"])
        total_partners = len(self.blk360_partners)
        
        active_nonprofits = len([n for n in self.blk360_nonprofits.values() if n["status"] == "active"])
        total_nonprofits = len(self.blk360_nonprofits)
        
        total_volunteer_hours = sum(l["hours"] for l in self.blk360_volunteer_logs.values())
        total_volunteers = len(set(l["user_id"] for l in self.blk360_volunteer_logs.values()))
        
        total_donations_amount = sum(d["amount"] for d in self.blk360_donations.values())
        total_donations_count = len(self.blk360_donations)
        
        return {
            **v2_metrics,
            "events": {
                "total_events": total_events,
                "upcoming_events": upcoming_events,
                "total_rsvps": total_rsvps,
                "past_events": total_events - upcoming_events
            },
            "partners": {
                "total_partners": total_partners,
                "active_partners": active_partners,
                "pending_partners": len([p for p in self.blk360_partners.values() if p["status"] == "pending"])
            },
            "nonprofits": {
                "total_nonprofits": total_nonprofits,
                "active_nonprofits": active_nonprofits,
                "pending_nonprofits": len([n for n in self.blk360_nonprofits.values() if n["status"] == "pending"])
            },
            "volunteers": {
                "total_hours": total_volunteer_hours,
                "total_volunteers": total_volunteers,
                "total_logs": len(self.blk360_volunteer_logs)
            },
            "donations": {
                "total_amount": total_donations_amount,
                "total_count": total_donations_count,
                "average_donation": total_donations_amount / total_donations_count if total_donations_count > 0 else 0
            }
        }

db = InMemoryDatabase()
