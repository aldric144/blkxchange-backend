"""
Migrate Phase 14B data from SQLite to PostgreSQL on Render
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models
from app.db_models.models import Base, Category, Product, Professional

# SQLite source
sqlite_url = "sqlite:///./blkxchange.db"
sqlite_engine = create_engine(sqlite_url)
SQLiteSession = sessionmaker(bind=sqlite_engine)

# PostgreSQL target (from environment)
postgres_url = os.getenv("DATABASE_URL")
if not postgres_url:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)

postgres_engine = create_engine(postgres_url)
PostgresSession = sessionmaker(bind=postgres_engine)

def migrate_data():
    print("="*80)
    print("MIGRATING PHASE 14B DATA TO POSTGRESQL")
    print("="*80)
    
    sqlite_db = SQLiteSession()
    postgres_db = PostgresSession()
    
    try:
        # Migrate Categories
        categories = sqlite_db.query(Category).all()
        print(f"\nMigrating {len(categories)} categories...")
        for cat in categories:
            # Check if exists
            existing = postgres_db.query(Category).filter(Category.slug == cat.slug).first()
            if not existing:
                new_cat = Category(
                    name=cat.name,
                    slug=cat.slug,
                    description=cat.description,
                    color_theme=cat.color_theme,
                    image_url=cat.image_url,
                    icon=cat.icon
                )
                postgres_db.add(new_cat)
        postgres_db.commit()
        print(f"✅ Categories migrated")
        
        # Migrate Products
        products = sqlite_db.query(Product).all()
        print(f"\nMigrating {len(products)} products...")
        for prod in products:
            existing = postgres_db.query(Product).filter(Product.name == prod.name).first()
            if not existing:
                new_prod = Product(
                    name=prod.name,
                    description=prod.description,
                    price=prod.price,
                    image_url=prod.image_url,
                    vendor_id=prod.vendor_id,
                    category=prod.category
                )
                postgres_db.add(new_prod)
        postgres_db.commit()
        print(f"✅ Products migrated")
        
        # Migrate Professionals
        professionals = sqlite_db.query(Professional).all()
        print(f"\nMigrating {len(professionals)} professionals...")
        for prof in professionals:
            existing = postgres_db.query(Professional).filter(Professional.email == prof.email).first()
            if not existing:
                new_prof = Professional(
                    name=prof.name,
                    title=prof.title,
                    bio=prof.bio,
                    image_url=prof.image_url,
                    email=prof.email,
                    phone=prof.phone,
                    category=prof.category,
                    expertise=prof.expertise
                )
                postgres_db.add(new_prof)
        postgres_db.commit()
        print(f"✅ Professionals migrated")
        
        print("\n" + "="*80)
        print("MIGRATION COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"ERROR: {e}")
        postgres_db.rollback()
        sys.exit(1)
    finally:
        sqlite_db.close()
        postgres_db.close()

if __name__ == "__main__":
    migrate_data()
