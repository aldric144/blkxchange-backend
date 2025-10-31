#!/usr/bin/env python3
"""
Phase 14B Data Seeding Script
Seeds 18 categories with 3-5 products each (54-90 products)
Seeds 24 professionals across all categories
"""
from app.db_models import SessionLocal
from app.db_models.models import Category, Product, Professional, Vendor
from datetime import datetime
import uuid

def seed_categories():
    """Seed 18 Pillars of Black Commerce"""
    print("\n" + "="*80)
    print("Seeding 18 Categories (Pillars of Black Commerce)")
    print("="*80)
    
    db = SessionLocal()
    
    categories = [
        {
            "name": "Apparel & Accessories",
            "slug": "apparel-accessories",
            "description": "Fashion, clothing, jewelry, and accessories celebrating Black culture and style",
            "color_theme": "#FF6B6B",
            "image_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800",
            "icon": "👔"
        },
        {
            "name": "Health & Wellness",
            "slug": "health-wellness",
            "description": "Products and services promoting physical and mental well-being",
            "color_theme": "#4ECDC4",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
            "icon": "💪"
        },
        {
            "name": "Beauty & Grooming",
            "slug": "beauty-grooming",
            "description": "Skincare, haircare, and beauty products for melanin-rich skin",
            "color_theme": "#FFE66D",
            "image_url": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800",
            "icon": "💄"
        },
        {
            "name": "Food & Beverages",
            "slug": "food-beverages",
            "description": "Soul food, specialty foods, beverages, and culinary experiences",
            "color_theme": "#FF8C42",
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",
            "icon": "🍽️"
        },
        {
            "name": "Home & Lifestyle",
            "slug": "home-lifestyle",
            "description": "Home decor, furniture, and lifestyle products",
            "color_theme": "#95E1D3",
            "image_url": "https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=800",
            "icon": "🏠"
        },
        {
            "name": "Art & Culture",
            "slug": "art-culture",
            "description": "Fine art, cultural artifacts, and creative expressions",
            "color_theme": "#F38181",
            "image_url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800",
            "icon": "🎨"
        },
        {
            "name": "Books & Publishing",
            "slug": "books-publishing",
            "description": "Books, magazines, and published works by Black authors",
            "color_theme": "#AA96DA",
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800",
            "icon": "📚"
        },
        {
            "name": "Technology & Innovation",
            "slug": "technology-innovation",
            "description": "Tech products, software, and innovative solutions",
            "color_theme": "#6C5CE7",
            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800",
            "icon": "💻"
        },
        {
            "name": "Finance & Investing",
            "slug": "finance-investing",
            "description": "Financial services, investment opportunities, and wealth building",
            "color_theme": "#00B894",
            "image_url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800",
            "icon": "💰"
        },
        {
            "name": "Education & Training",
            "slug": "education-training",
            "description": "Educational resources, courses, and professional development",
            "color_theme": "#FDCB6E",
            "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
            "icon": "🎓"
        },
        {
            "name": "Faith & Inspiration",
            "slug": "faith-inspiration",
            "description": "Spiritual products, inspirational content, and faith-based resources",
            "color_theme": "#A29BFE",
            "image_url": "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=800",
            "icon": "🙏"
        },
        {
            "name": "Community & Nonprofits",
            "slug": "community-nonprofits",
            "description": "Community organizations and nonprofit initiatives",
            "color_theme": "#74B9FF",
            "image_url": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800",
            "icon": "🤝"
        },
        {
            "name": "Real Estate & Development",
            "slug": "real-estate-development",
            "description": "Property services, real estate, and community development",
            "color_theme": "#FD79A8",
            "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800",
            "icon": "🏢"
        },
        {
            "name": "Media & Entertainment",
            "slug": "media-entertainment",
            "description": "Film, music, entertainment, and media production",
            "color_theme": "#E17055",
            "image_url": "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=800",
            "icon": "🎬"
        },
        {
            "name": "Law & Justice",
            "slug": "law-justice",
            "description": "Legal services, advocacy, and justice initiatives",
            "color_theme": "#636E72",
            "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800",
            "icon": "⚖️"
        },
        {
            "name": "Travel & Leisure",
            "slug": "travel-leisure",
            "description": "Travel services, tourism, and leisure activities",
            "color_theme": "#00CEC9",
            "image_url": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800",
            "icon": "✈️"
        },
        {
            "name": "Sports & Fitness",
            "slug": "sports-fitness",
            "description": "Athletic gear, fitness services, and sports programs",
            "color_theme": "#FF7675",
            "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800",
            "icon": "⚽"
        },
        {
            "name": "Green Tech & Sustainability",
            "slug": "green-tech-sustainability",
            "description": "Eco-friendly products and sustainable solutions",
            "color_theme": "#55EFC4",
            "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800",
            "icon": "🌱"
        }
    ]
    
    try:
        for cat_data in categories:
            existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                print(f"  ✅ Added category: {cat_data['name']}")
            else:
                print(f"  ⏭️  Category already exists: {cat_data['name']}")
        
        db.commit()
        print(f"\n✅ Categories seeding complete!")
        return True
    except Exception as e:
        print(f"\n❌ Error seeding categories: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def seed_products():
    """Seed 3-5 products for each category (54-90 total)"""
    print("\n" + "="*80)
    print("Seeding Products (3-5 per category)")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        vendor = db.query(Vendor).first()
        if not vendor:
            vendor = Vendor(
                id=str(uuid.uuid4()),
                email="marketplace@blkxchange.com",
                name="BlkXchange Marketplace",
                business_name="BlkXchange Marketplace",
                business_description="Official BlkXchange marketplace vendor",
                verified=True
            )
            db.add(vendor)
            db.commit()
            db.refresh(vendor)
        
        categories = db.query(Category).all()
        product_count = 0
        
        for category in categories:
            existing_products = db.query(Product).filter(Product.category == category.name).count()
            if existing_products >= 3:
                print(f"  ⏭️  {category.name}: Already has {existing_products} products")
                continue
            
            products_to_add = 4 - existing_products
            for i in range(products_to_add):
                product = Product(
                    id=str(uuid.uuid4()),
                    vendor_id=vendor.id,
                    name=f"{category.name} Product {i+1}",
                    description=f"Premium {category.name.lower()} product from Black-owned business",
                    price=round(29.99 + (i * 10), 2),
                    category=category.name,
                    image_url=category.image_url,
                    stock=100,
                    rating=4.5 + (i * 0.1),
                    reviews_count=10 + (i * 5)
                )
                db.add(product)
                product_count += 1
            
            print(f"  ✅ {category.name}: Added {products_to_add} products")
        
        db.commit()
        print(f"\n✅ Products seeding complete! Total products added: {product_count}")
        return True
    except Exception as e:
        print(f"\n❌ Error seeding products: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def seed_professionals():
    """Seed 24 professionals across all categories"""
    print("\n" + "="*80)
    print("Seeding 24 Professionals")
    print("="*80)
    
    db = SessionLocal()
    
    professionals_data = [
        {"name": "Dr. Marcus Johnson", "title": "Financial Advisor", "category": "Finance & Investing", "bio": "20+ years helping Black families build generational wealth through strategic investing", "hourly_rate": 250.00, "verified": True, "featured": True},
        {"name": "Jasmine Clarke", "title": "Business Consultant", "category": "Finance & Investing", "bio": "Specializing in startup funding and business development for minority entrepreneurs", "hourly_rate": 200.00, "verified": True, "featured": False},
        {"name": "Kevin Thompson", "title": "Software Engineer", "category": "Technology & Innovation", "bio": "Full-stack developer with expertise in AI and machine learning applications", "hourly_rate": 180.00, "verified": True, "featured": True},
        {"name": "Angela Williams", "title": "EdTech Specialist", "category": "Education & Training", "bio": "Creating innovative educational technology solutions for underserved communities", "hourly_rate": 150.00, "verified": True, "featured": False},
        {"name": "Dr. Patricia Brown", "title": "Healthcare Consultant", "category": "Health & Wellness", "bio": "Public health expert focused on healthcare equity and community wellness programs", "hourly_rate": 220.00, "verified": True, "featured": True},
        {"name": "Michael Davis", "title": "Real Estate Developer", "category": "Real Estate & Development", "bio": "Developing affordable housing and commercial spaces in Black communities", "hourly_rate": 275.00, "verified": True, "featured": False},
        {"name": "Tamika Robinson", "title": "Fashion Designer", "category": "Apparel & Accessories", "bio": "Award-winning designer celebrating African heritage through contemporary fashion", "hourly_rate": 195.00, "verified": True, "featured": True},
        {"name": "James Mitchell", "title": "Marketing Strategist", "category": "Media & Entertainment", "bio": "Digital marketing expert helping Black businesses amplify their brand presence", "hourly_rate": 165.00, "verified": True, "featured": False},
        {"name": "Dr. Aisha Carter", "title": "Clinical Psychologist", "category": "Health & Wellness", "bio": "Mental health advocate specializing in trauma-informed care for BIPOC communities", "hourly_rate": 200.00, "verified": True, "featured": True},
        {"name": "Brandon Lee", "title": "Fitness Coach", "category": "Sports & Fitness", "bio": "Certified personal trainer and nutrition specialist for holistic wellness", "hourly_rate": 120.00, "verified": True, "featured": False},
        {"name": "Monique Harris", "title": "Beauty Expert", "category": "Beauty & Grooming", "bio": "Licensed esthetician specializing in skincare for melanin-rich skin", "hourly_rate": 135.00, "verified": True, "featured": True},
        {"name": "Terrence Washington", "title": "Attorney", "category": "Law & Justice", "bio": "Civil rights attorney fighting for justice and equality in the legal system", "hourly_rate": 300.00, "verified": True, "featured": True},
        {"name": "Nia Anderson", "title": "Interior Designer", "category": "Home & Lifestyle", "bio": "Creating beautiful, culturally-inspired living spaces that tell your story", "hourly_rate": 175.00, "verified": True, "featured": False},
        {"name": "Derek Foster", "title": "Chef & Culinary Consultant", "category": "Food & Beverages", "bio": "Celebrating soul food traditions while innovating modern culinary experiences", "hourly_rate": 160.00, "verified": True, "featured": True},
        {"name": "Simone Jackson", "title": "Author & Publisher", "category": "Books & Publishing", "bio": "Award-winning author and founder of independent Black publishing house", "hourly_rate": 185.00, "verified": True, "featured": False},
        {"name": "Isaiah Moore", "title": "Visual Artist", "category": "Art & Culture", "bio": "Contemporary artist exploring Black identity through mixed media installations", "hourly_rate": 145.00, "verified": True, "featured": True},
        {"name": "Rev. Dr. Grace Taylor", "title": "Spiritual Counselor", "category": "Faith & Inspiration", "bio": "Providing faith-based guidance and spiritual wellness coaching", "hourly_rate": 125.00, "verified": True, "featured": False},
        {"name": "Cameron White", "title": "Travel Consultant", "category": "Travel & Leisure", "bio": "Curating culturally immersive travel experiences across the African diaspora", "hourly_rate": 140.00, "verified": True, "featured": True},
        {"name": "Destiny Green", "title": "Environmental Scientist", "category": "Green Tech & Sustainability", "bio": "Leading sustainable development initiatives in urban Black communities", "hourly_rate": 190.00, "verified": True, "featured": False},
        {"name": "Marcus Thompson", "title": "Community Organizer", "category": "Community & Nonprofits", "bio": "Building grassroots movements for social justice and community empowerment", "hourly_rate": 110.00, "verified": True, "featured": True},
        {"name": "Alicia Martinez", "title": "Film Producer", "category": "Media & Entertainment", "bio": "Independent filmmaker telling authentic Black stories for global audiences", "hourly_rate": 210.00, "verified": True, "featured": False},
        {"name": "Jordan Scott", "title": "Data Scientist", "category": "Technology & Innovation", "bio": "Using data analytics to drive equity and inclusion in tech industry", "hourly_rate": 195.00, "verified": True, "featured": True},
        {"name": "Dr. Kimberly Adams", "title": "Education Director", "category": "Education & Training", "bio": "Developing culturally responsive curriculum for K-12 and higher education", "hourly_rate": 170.00, "verified": True, "featured": False},
        {"name": "Xavier Brooks", "title": "Investment Banker", "category": "Finance & Investing", "bio": "Connecting Black entrepreneurs with capital and investment opportunities", "hourly_rate": 285.00, "verified": True, "featured": True}
    ]
    
    try:
        existing_count = db.query(Professional).count()
        if existing_count >= 24:
            print(f"  ⏭️  Already have {existing_count} professionals in database")
            return True
        
        for prof_data in professionals_data:
            existing = db.query(Professional).filter(Professional.email == f"{prof_data['name'].lower().replace(' ', '.')}@blkxchange.com").first()
            if not existing:
                professional = Professional(
                    id=str(uuid.uuid4()),
                    email=f"{prof_data['name'].lower().replace(' ', '.')}@blkxchange.com",
                    name=prof_data["name"],
                    title=prof_data["title"],
                    category=prof_data["category"],
                    bio=prof_data["bio"],
                    hourly_rate=prof_data["hourly_rate"],
                    verified=prof_data["verified"],
                    image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
                    rating=4.8,
                    reviews_count=25
                )
                db.add(professional)
                print(f"  ✅ Added professional: {prof_data['name']} - {prof_data['title']}")
            else:
                print(f"  ⏭️  Professional already exists: {prof_data['name']}")
        
        db.commit()
        print(f"\n✅ Professionals seeding complete!")
        return True
    except Exception as e:
        print(f"\n❌ Error seeding professionals: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("Phase 14B Data Seeding Script")
    print("="*80)
    
    results = {
        "Categories": seed_categories(),
        "Products": seed_products(),
        "Professionals": seed_professionals()
    }
    
    print("\n" + "="*80)
    print("SEEDING RESULTS")
    print("="*80)
    
    for module, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{module}: {status}")
    
    if all(results.values()):
        print("\n✅ Phase 14B data seeding completed successfully!")
    else:
        print("\n❌ Some seeding operations failed - review errors above")
