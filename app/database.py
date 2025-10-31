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
    ProductEnhanced, ProductCreateEnhanced, ProductStatus
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
        self.impact_stats = {
            "total_donations": 0.0,
            "total_orders": 0,
            "hbcu_donations": 0.0,
            "scholarship_donations": 0.0,
            "nonprofit_donations": 0.0
        }
    
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
    
    def update_vendor(self, vendor_id: str, vendor_data: VendorCreate) -> Optional[Vendor]:
        if vendor_id in self.vendors:
            vendor = self.vendors[vendor_id]
            vendor.email = vendor_data.email
            vendor.name = vendor_data.name
            vendor.business_name = vendor_data.business_name
            vendor.business_description = vendor_data.business_description
            vendor.phone = vendor_data.phone
            vendor.stripe_account_id = vendor_data.stripe_account_id
            return vendor
        return None
    
    def delete_vendor(self, vendor_id: str) -> bool:
        if vendor_id in self.vendors:
            del self.vendors[vendor_id]
            return True
        return False
    
    def create_product(self, vendor_id: str, product_data: ProductCreate) -> Product:
        product_id = str(uuid.uuid4())
        product = Product(
            id=product_id,
            vendor_id=vendor_id,
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
            created_at=datetime.now()
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
    
    def update_professional(self, professional_id: str, professional_data: ProfessionalCreate) -> Optional[Professional]:
        if professional_id in self.professionals:
            professional = self.professionals[professional_id]
            professional.email = professional_data.email
            professional.name = professional_data.name
            professional.title = professional_data.title
            professional.category = professional_data.category
            professional.bio = professional_data.bio
            professional.credentials = professional_data.credentials
            professional.hourly_rate = professional_data.hourly_rate
            professional.phone = professional_data.phone
            professional.image_url = professional_data.image_url
            return professional
        return None
    
    def delete_professional(self, professional_id: str) -> bool:
        if professional_id in self.professionals:
            del self.professionals[professional_id]
            return True
        return False
    
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
        
        vendor_amount = total_amount * 0.90
        platform_amount = total_amount * 0.07
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

db = InMemoryDatabase()
