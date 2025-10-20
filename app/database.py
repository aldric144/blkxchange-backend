from typing import Dict, List, Optional
from datetime import datetime
import uuid
from app.models import (
    Vendor, VendorCreate, Product, ProductCreate, 
    Professional, ProfessionalCreate, Order, OrderCreate,
    OrderItem, OrderStatus, ImpactStats
)

class InMemoryDatabase:
    def __init__(self):
        self.vendors: Dict[str, Vendor] = {}
        self.products: Dict[str, Product] = {}
        self.professionals: Dict[str, Professional] = {}
        self.orders: Dict[str, Order] = {}
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

db = InMemoryDatabase()
