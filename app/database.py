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
    PendingProfessional, PendingProfessionalCreate, PendingProfessionalStatus
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
        self.impact_stats = {
            "total_donations": 0.0,
            "total_orders": 0,
            "hbcu_donations": 0.0,
            "scholarship_donations": 0.0,
            "nonprofit_donations": 0.0
        }
        self._seed_black_banks()
    
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
            image_url=professional_data.image_url,
            verified=False,
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
        return professionals
    
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
                    "image_url": professional.image_url,
                    "hourly_rate": professional.hourly_rate,
                    "verified": professional.verified,
                    "rating": professional.rating,
                    "latitude": professional.latitude,
                    "longitude": professional.longitude
                })
        
        nearby_professionals.sort(key=lambda x: x["distance_miles"])
        
        return nearby_professionals
    
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
            zip=data.zip,
            email=data.email,
            agreement_accepted=data.agreement_accepted,
            status=PendingProfessionalStatus.PENDING,
            submitted_at=datetime.now(),
            approved_by=None,
            approved_at=None
        )
        self.pending_professionals[professional_id] = pending
        return pending
    
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

db = InMemoryDatabase()
