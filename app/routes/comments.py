from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os
from pathlib import Path

router = APIRouter()

DB_PATH = Path(__file__).parent.parent.parent / "comments.db"

class CommentCreate(BaseModel):
    article_id: int
    author: str
    content: str

class Comment(BaseModel):
    id: int
    article_id: int
    author: str
    content: str
    created_at: str

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[Comment])
async def get_comments(article_id: Optional[int] = None):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    if article_id:
        cursor.execute("SELECT * FROM comments WHERE article_id = ? ORDER BY created_at ASC", (article_id,))
    else:
        cursor.execute("SELECT * FROM comments ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    comments = []
    for row in rows:
        comments.append(Comment(
            id=row[0],
            article_id=row[1],
            author=row[2],
            content=row[3],
            created_at=row[4]
        ))
    
    return comments

@router.post("/", response_model=Comment)
async def create_comment(comment: CommentCreate):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO comments (article_id, author, content)
        VALUES (?, ?, ?)
    """, (comment.article_id, comment.author, comment.content))
    
    comment_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Comment(
        id=row[0],
        article_id=row[1],
        author=row[2],
        content=row[3],
        created_at=row[4]
    )

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Comment not found")
    
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Comment deleted successfully"}
