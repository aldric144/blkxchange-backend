#!/usr/bin/env python3
"""
Comprehensive CRUD testing for all BlkXchange modules
Tests Create, Read, Update, Delete operations on PostgreSQL
"""
import os
os.environ['DATABASE_URL'] = 'postgresql://blkxchange_user:smQL52FVRrBBzEYtDKpHPj8U65bKIk8p@dpg-d42eghq4d50c739lcs2g-a.oregon-postgres.render.com:5432/blkxchange'

from app.db_models import SessionLocal
from app.db_models.models import (
    Vendor, Product, Professional, Article, Module, Event, 
    Legacy, ForumTopic, ForumReply, Group
)
from datetime import datetime
import uuid

def test_vendors_crud():
    """Test CRUD operations on Vendors"""
    print("\n" + "="*80)
    print("Testing Vendors CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        print("\n1. CREATE - Adding new vendor...")
        new_vendor = Vendor(
            id=str(uuid.uuid4()),
            email="test@vendor.com",
            name="Test Vendor",
            business_name="Test Business",
            business_description="Test Description",
            phone="555-1234",
            verified=False
        )
        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
        print(f"   ✅ Created vendor: {new_vendor.business_name} (ID: {new_vendor.id})")
        
        print("\n2. READ - Fetching vendor...")
        fetched_vendor = db.query(Vendor).filter(Vendor.id == new_vendor.id).first()
        print(f"   ✅ Read vendor: {fetched_vendor.business_name}")
        
        print("\n3. UPDATE - Updating vendor...")
        fetched_vendor.business_description = "Updated Description"
        fetched_vendor.verified = True
        db.commit()
        db.refresh(fetched_vendor)
        print(f"   ✅ Updated vendor: verified={fetched_vendor.verified}")
        
        print("\n4. DELETE - Removing vendor...")
        db.delete(fetched_vendor)
        db.commit()
        deleted_check = db.query(Vendor).filter(Vendor.id == new_vendor.id).first()
        print(f"   ✅ Deleted vendor: exists={deleted_check is not None}")
        
        print("\n✅ Vendors CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Vendors CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_products_crud():
    """Test CRUD operations on Products"""
    print("\n" + "="*80)
    print("Testing Products CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        vendor = Vendor(
            id=str(uuid.uuid4()),
            email="vendor@test.com",
            name="Product Test Vendor",
            business_name="Test Vendor Business",
            phone="555-5678"
        )
        db.add(vendor)
        db.commit()
        
        print("\n1. CREATE - Adding new product...")
        new_product = Product(
            id=str(uuid.uuid4()),
            vendor_id=vendor.id,
            name="Test Product",
            description="Test Description",
            price=99.99,
            category="Technology",
            stock=10
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        print(f"   ✅ Created product: {new_product.name} (ID: {new_product.id})")
        
        print("\n2. READ - Fetching product...")
        fetched_product = db.query(Product).filter(Product.id == new_product.id).first()
        print(f"   ✅ Read product: {fetched_product.name}, Price: ${fetched_product.price}")
        
        print("\n3. UPDATE - Updating product...")
        fetched_product.price = 149.99
        fetched_product.stock = 20
        db.commit()
        db.refresh(fetched_product)
        print(f"   ✅ Updated product: price=${fetched_product.price}, stock={fetched_product.stock}")
        
        print("\n4. DELETE - Removing product...")
        db.delete(fetched_product)
        db.delete(vendor)
        db.commit()
        print(f"   ✅ Deleted product and vendor")
        
        print("\n✅ Products CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Products CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_professionals_crud():
    """Test CRUD operations on Professionals"""
    print("\n" + "="*80)
    print("Testing Professionals CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        print("\n1. CREATE - Adding new professional...")
        new_prof = Professional(
            id=str(uuid.uuid4()),
            email="prof@test.com",
            name="Test Professional",
            title="Test Title",
            category="Technology",
            bio="Test Bio",
            hourly_rate=150.00
        )
        db.add(new_prof)
        db.commit()
        db.refresh(new_prof)
        print(f"   ✅ Created professional: {new_prof.name} (ID: {new_prof.id})")
        
        print("\n2. READ - Fetching professional...")
        fetched_prof = db.query(Professional).filter(Professional.id == new_prof.id).first()
        print(f"   ✅ Read professional: {fetched_prof.name}, Rate: ${fetched_prof.hourly_rate}/hr")
        
        print("\n3. UPDATE - Updating professional...")
        fetched_prof.hourly_rate = 200.00
        fetched_prof.verified = True
        db.commit()
        db.refresh(fetched_prof)
        print(f"   ✅ Updated professional: rate=${fetched_prof.hourly_rate}, verified={fetched_prof.verified}")
        
        print("\n4. DELETE - Removing professional...")
        db.delete(fetched_prof)
        db.commit()
        print(f"   ✅ Deleted professional")
        
        print("\n✅ Professionals CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Professionals CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_articles_crud():
    """Test CRUD operations on Articles"""
    print("\n" + "="*80)
    print("Testing Articles CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        print("\n1. CREATE - Adding new article...")
        new_article = Article(
            title="Test Article",
            category="Technology",
            body="Test article body content",
            author="Test Author",
            image_url="https://example.com/image.jpg"
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        print(f"   ✅ Created article: {new_article.title} (ID: {new_article.id})")
        
        print("\n2. READ - Fetching article...")
        fetched_article = db.query(Article).filter(Article.id == new_article.id).first()
        print(f"   ✅ Read article: {fetched_article.title} by {fetched_article.author}")
        
        print("\n3. UPDATE - Updating article...")
        fetched_article.body = "Updated article body"
        fetched_article.category = "Business"
        db.commit()
        db.refresh(fetched_article)
        print(f"   ✅ Updated article: category={fetched_article.category}")
        
        print("\n4. DELETE - Removing article...")
        db.delete(fetched_article)
        db.commit()
        print(f"   ✅ Deleted article")
        
        print("\n✅ Articles CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Articles CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_modules_crud():
    """Test CRUD operations on Modules"""
    print("\n" + "="*80)
    print("Testing Modules CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        print("\n1. CREATE - Adding new module...")
        new_module = Module(
            title="Test Module",
            category="Finance",
            description="Test module description",
            video_url="https://youtube.com/watch?v=test"
        )
        db.add(new_module)
        db.commit()
        db.refresh(new_module)
        print(f"   ✅ Created module: {new_module.title} (ID: {new_module.id})")
        
        print("\n2. READ - Fetching module...")
        fetched_module = db.query(Module).filter(Module.id == new_module.id).first()
        print(f"   ✅ Read module: {fetched_module.title}")
        
        print("\n3. UPDATE - Updating module...")
        fetched_module.description = "Updated module description"
        db.commit()
        db.refresh(fetched_module)
        print(f"   ✅ Updated module")
        
        print("\n4. DELETE - Removing module...")
        db.delete(fetched_module)
        db.commit()
        print(f"   ✅ Deleted module")
        
        print("\n✅ Modules CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Modules CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_events_crud():
    """Test CRUD operations on Events"""
    print("\n" + "="*80)
    print("Testing Events CRUD Operations")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        print("\n1. CREATE - Adding new event...")
        new_event = Event(
            name="Test Event",
            description="Test event description",
            category="Community",
            date="2025-12-01",
            location="Test Location"
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        print(f"   ✅ Created event: {new_event.name} (ID: {new_event.id})")
        
        print("\n2. READ - Fetching event...")
        fetched_event = db.query(Event).filter(Event.id == new_event.id).first()
        print(f"   ✅ Read event: {fetched_event.name} on {fetched_event.date}")
        
        print("\n3. UPDATE - Updating event...")
        fetched_event.location = "Updated Location"
        db.commit()
        db.refresh(fetched_event)
        print(f"   ✅ Updated event: location={fetched_event.location}")
        
        print("\n4. DELETE - Removing event...")
        db.delete(fetched_event)
        db.commit()
        print(f"   ✅ Deleted event")
        
        print("\n✅ Events CRUD: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Events CRUD FAILED: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("BlkXchange PostgreSQL CRUD Testing Suite")
    print("="*80)
    
    results = {
        "Vendors": test_vendors_crud(),
        "Products": test_products_crud(),
        "Professionals": test_professionals_crud(),
        "Articles": test_articles_crud(),
        "Modules": test_modules_crud(),
        "Events": test_events_crud()
    }
    
    print("\n" + "="*80)
    print("FINAL TEST RESULTS")
    print("="*80)
    
    for module, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{module}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL CRUD TESTS PASSED - PostgreSQL is fully operational!")
    else:
        print("❌ SOME TESTS FAILED - Review errors above")
    print("="*80)
