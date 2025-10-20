from app.database import db
from app.models import (
    VendorCreate, ProductCreate, ProfessionalCreate,
    ProductCategory, ProfessionalCategory
)

def seed_database():
    vendor1 = db.create_vendor(VendorCreate(
        email="maya@soulfulthreads.com",
        name="Maya Johnson",
        business_name="Soulful Threads",
        business_description="Authentic African-inspired apparel and accessories celebrating Black culture and heritage.",
        phone="555-0101"
    ))
    
    vendor2 = db.create_vendor(VendorCreate(
        email="james@naturalglow.com",
        name="James Williams",
        business_name="Natural Glow Beauty",
        business_description="Premium natural beauty products formulated for melanin-rich skin.",
        phone="555-0102"
    ))
    
    vendor3 = db.create_vendor(VendorCreate(
        email="aisha@blackbookshelf.com",
        name="Aisha Davis",
        business_name="The Black Bookshelf",
        business_description="Curated collection of books by Black authors across all genres.",
        phone="555-0103"
    ))
    
    vendor4 = db.create_vendor(VendorCreate(
        email="marcus@afroart.com",
        name="Marcus Brown",
        business_name="AfroArt Gallery",
        business_description="Contemporary African and African-American art pieces.",
        phone="555-0104"
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Ankara Print Dress",
        description="Beautiful handmade dress featuring vibrant Ankara print fabric. Perfect for any occasion.",
        price=89.99,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500",
        stock=15
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Kente Cloth Scarf",
        description="Authentic Kente cloth scarf handwoven in Ghana. A timeless accessory.",
        price=45.00,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=500",
        stock=25
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Dashiki Shirt",
        description="Classic dashiki shirt in bold colors. Comfortable and stylish.",
        price=39.99,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500",
        stock=30
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Shea Butter Body Cream",
        description="Rich, moisturizing body cream made with pure African shea butter.",
        price=24.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500",
        stock=50
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Natural Hair Growth Oil",
        description="Nourishing oil blend to promote healthy hair growth and shine.",
        price=18.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=500",
        stock=40
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Melanin Glow Serum",
        description="Vitamin C serum designed to enhance and protect melanin-rich skin.",
        price=32.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500",
        stock=35
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="The Bluest Eye by Toni Morrison",
        description="Classic novel exploring themes of beauty, race, and identity.",
        price=16.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
        stock=20
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="Between the World and Me",
        description="Ta-Nehisi Coates' powerful meditation on race in America.",
        price=14.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        stock=18
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="Homegoing by Yaa Gyasi",
        description="Epic novel tracing two branches of a family through generations.",
        price=17.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500",
        stock=22
    ))
    
    db.create_product(vendor4.id, ProductCreate(
        name="African Mask Wall Art",
        description="Handcrafted wooden African mask, perfect for home decor.",
        price=125.00,
        category=ProductCategory.ART,
        image_url="https://images.unsplash.com/photo-1577083552431-6e5fd01988ec?w=500",
        stock=8
    ))
    
    db.create_product(vendor4.id, ProductCreate(
        name="Abstract Canvas Print",
        description="Contemporary abstract art celebrating Black excellence.",
        price=89.00,
        category=ProductCategory.ART,
        image_url="https://images.unsplash.com/photo-1549887534-1541e9326642?w=500",
        stock=12
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.thompson@healthclinic.com",
        name="Dr. Sarah Thompson",
        title="Family Medicine Physician",
        category=ProfessionalCategory.HEALTH,
        bio="Board-certified family medicine physician with 15 years of experience providing comprehensive care to diverse communities.",
        credentials="MD, Board Certified in Family Medicine",
        hourly_rate=200.00,
        phone="555-0201",
        image_url="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.jackson@lawfirm.com",
        name="Attorney Michael Jackson",
        title="Civil Rights Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Dedicated civil rights attorney fighting for justice and equality. Specializing in employment discrimination and police misconduct cases.",
        credentials="JD, Licensed to practice in NY, NJ, and Federal Courts",
        hourly_rate=350.00,
        phone="555-0202",
        image_url="https://images.unsplash.com/photo-1556157382-97eda2d62296?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="lisa@financialfreedom.com",
        name="Lisa Anderson",
        title="Financial Advisor",
        category=ProfessionalCategory.FINANCE,
        bio="Certified financial planner helping families build generational wealth through smart investing and financial planning.",
        credentials="CFP, MBA in Finance",
        hourly_rate=175.00,
        phone="555-0203",
        image_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.roberts@empowerment.com",
        name="Coach David Roberts",
        title="Life & Business Coach",
        category=ProfessionalCategory.COACHING,
        bio="Empowering Black entrepreneurs to achieve their dreams through strategic coaching and mentorship.",
        credentials="ICF Certified Coach, 20+ years business experience",
        hourly_rate=150.00,
        phone="555-0204",
        image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.williams@consulting.com",
        name="Dr. Patricia Williams",
        title="Diversity & Inclusion Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="PhD in Organizational Psychology. Helping companies build inclusive cultures and equitable practices.",
        credentials="PhD in Organizational Psychology, SHRM-SCP",
        hourly_rate=300.00,
        phone="555-0205",
        image_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=500"
    ))
    
    print("Database seeded successfully!")
    print(f"Created {len(db.vendors)} vendors")
    print(f"Created {len(db.products)} products")
    print(f"Created {len(db.professionals)} professionals")
