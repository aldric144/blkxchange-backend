#!/usr/bin/env python3
"""
Data migration script to move data from in-memory/SQLite to PostgreSQL
"""
import json
import sqlite3
from sqlalchemy.orm import Session
from app.db_models import SessionLocal, engine, Base
from app.db_models.models import (
    Vendor, Product, Professional, Order, VendorApplication,
    VendorAccount, ProductEnhanced, Article, Module, Legacy,
    History, ForumTopic, ForumReply, Event, Group, ImpactStat
)
from datetime import datetime
import uuid

def migrate_from_json_snapshot():
    """Migrate data from JSON snapshot to PostgreSQL"""
    print("Starting data migration from JSON snapshot...")
    
    with open('/home/ubuntu/backups/phase13_pre_expansion/inmemory_snapshot.json', 'r') as f:
        snapshot = json.load(f)
    
    db = SessionLocal()
    
    try:
        print(f"\nMigrating {len(snapshot['vendors'])} vendors...")
        for vendor_data in snapshot['vendors']:
            vendor = Vendor(
                id=vendor_data['id'],
                email=vendor_data['email'],
                name=vendor_data['name'],
                business_name=vendor_data['business_name'],
                business_description=vendor_data.get('business_description', ''),
                phone=vendor_data.get('phone', ''),
                stripe_account_id=vendor_data.get('stripe_account_id'),
                verified=vendor_data.get('verified', False),
                total_sales=vendor_data.get('total_sales', 0.0),
                community_contribution=vendor_data.get('community_contribution', 0.0),
                created_at=datetime.fromisoformat(vendor_data['created_at']) if vendor_data.get('created_at') else datetime.utcnow()
            )
            db.add(vendor)
        
        print(f"Migrating {len(snapshot['products'])} products...")
        for product_data in snapshot['products']:
            product = Product(
                id=product_data['id'],
                vendor_id=product_data['vendor_id'],
                name=product_data['name'],
                description=product_data.get('description', ''),
                price=product_data['price'],
                category=product_data.get('category', ''),
                image_url=product_data.get('image_url', ''),
                stock=product_data.get('stock', 0),
                rating=product_data.get('rating', 0.0),
                reviews_count=product_data.get('reviews_count', 0),
                created_at=datetime.fromisoformat(product_data['created_at']) if product_data.get('created_at') else datetime.utcnow()
            )
            db.add(product)
        
        print(f"Migrating {len(snapshot['professionals'])} professionals...")
        for prof_data in snapshot['professionals']:
            professional = Professional(
                id=prof_data['id'],
                email=prof_data['email'],
                name=prof_data['name'],
                title=prof_data['title'],
                category=prof_data.get('category', ''),
                bio=prof_data.get('bio', ''),
                credentials=prof_data.get('credentials', ''),
                hourly_rate=prof_data.get('hourly_rate', 0.0),
                phone=prof_data.get('phone', ''),
                image_url=prof_data.get('image_url', ''),
                verified=prof_data.get('verified', False),
                rating=prof_data.get('rating', 0.0),
                reviews_count=prof_data.get('reviews_count', 0),
                created_at=datetime.fromisoformat(prof_data['created_at']) if prof_data.get('created_at') else datetime.utcnow()
            )
            db.add(professional)
        
        print("Migrating impact stats...")
        impact_stat = ImpactStat(
            total_donations=snapshot['impact_stats'].get('total_donations', 0.0),
            total_orders=snapshot['impact_stats'].get('total_orders', 0),
            total_vendors=snapshot['impact_stats'].get('total_vendors', 0),
            total_professionals=snapshot['impact_stats'].get('total_professionals', 0),
            hbcu_donations=snapshot['impact_stats'].get('hbcu_donations', 0.0),
            scholarship_donations=snapshot['impact_stats'].get('scholarship_donations', 0.0),
            nonprofit_donations=snapshot['impact_stats'].get('nonprofit_donations', 0.0)
        )
        db.add(impact_stat)
        
        db.commit()
        print("\n✅ JSON snapshot migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def migrate_from_sqlite():
    """Migrate data from SQLite databases to PostgreSQL"""
    print("\nStarting data migration from SQLite databases...")
    
    db = SessionLocal()
    
    try:
        articles_db_path = '/home/ubuntu/blkxchange/backend/articles.db'
        conn = sqlite3.connect(articles_db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, category, body, author, image_url, created_at FROM articles")
        articles = cursor.fetchall()
        
        print(f"\nMigrating {len(articles)} articles...")
        for article_data in articles:
            article = Article(
                id=article_data[0],
                title=article_data[1],
                category=article_data[2],
                body=article_data[3],
                author=article_data[4],
                image_url=article_data[5],
                created_at=datetime.fromisoformat(article_data[6]) if article_data[6] else datetime.utcnow()
            )
            db.add(article)
        
        conn.close()
        
        db.commit()
        print("\n✅ SQLite migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during SQLite migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("="*80)
    print("BlkXchange Data Migration Script")
    print("="*80)
    
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    
    migrate_from_json_snapshot()
    migrate_from_sqlite()
    
    print("\n" + "="*80)
    print("✅ All data migration completed successfully!")
    print("="*80)
