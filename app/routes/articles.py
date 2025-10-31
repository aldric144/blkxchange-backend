from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
import sqlite3
import os
from pathlib import Path

from app.models import Article, ArticleCreate

router = APIRouter()

DB_PATH = Path(__file__).parent.parent.parent / "articles.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the articles database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            body TEXT NOT NULL,
            author TEXT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

@router.get("", response_model=List[Article])
async def get_articles(category: Optional[str] = None):
    """
    Get all articles, optionally filtered by category
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if category:
        cursor.execute(
            "SELECT * FROM articles WHERE category = ? ORDER BY created_at DESC",
            (category,)
        )
    else:
        cursor.execute("SELECT * FROM articles ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    articles = []
    for row in rows:
        articles.append(Article(
            id=row["id"],
            title=row["title"],
            category=row["category"],
            body=row["body"],
            author=row["author"],
            image_url=row["image_url"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now()
        ))
    
    return articles

@router.post("", response_model=Article)
async def create_article(article: ArticleCreate):
    """
    Create a new article
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO articles (title, category, body, author, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            article.title,
            article.category,
            article.body,
            article.author,
            article.image_url,
            datetime.now().isoformat()
        )
    )
    
    conn.commit()
    article_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Article(
        id=row["id"],
        title=row["title"],
        category=row["category"],
        body=row["body"],
        author=row["author"],
        image_url=row["image_url"],
        created_at=datetime.fromisoformat(row["created_at"])
    )

@router.get("/{article_id}", response_model=Article)
async def get_article(article_id: int):
    """
    Get a single article by ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return Article(
        id=row["id"],
        title=row["title"],
        category=row["category"],
        body=row["body"],
        author=row["author"],
        image_url=row["image_url"],
        created_at=datetime.fromisoformat(row["created_at"])
    )
