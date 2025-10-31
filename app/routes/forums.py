from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "forums.db")

class TopicCreate(BaseModel):
    category: str
    title: str
    content: str
    author: str

class Topic(BaseModel):
    id: int
    category: str
    title: str
    content: str
    author: str
    created_at: str
    reply_count: int = 0

class ReplyCreate(BaseModel):
    topic_id: int
    content: str
    author: str

class Reply(BaseModel):
    id: int
    topic_id: int
    content: str
    author: str
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/topics", response_model=List[Topic])
async def get_topics(category: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM topics WHERE category = ? ORDER BY created_at DESC", (category,))
    else:
        cursor.execute("SELECT * FROM topics ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    
    topics = []
    for row in rows:
        cursor.execute("SELECT COUNT(*) FROM replies WHERE topic_id = ?", (row[0],))
        reply_count = cursor.fetchone()[0]
        
        topics.append(Topic(
            id=row[0],
            category=row[1],
            title=row[2],
            content=row[3],
            author=row[4],
            created_at=row[5],
            reply_count=reply_count
        ))
    
    conn.close()
    return topics

@router.post("/topics", response_model=Topic)
async def create_topic(topic: TopicCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO topics (category, title, content, author)
        VALUES (?, ?, ?, ?)
    """, (topic.category, topic.title, topic.content, topic.author))
    
    topic_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Topic(
        id=row[0],
        category=row[1],
        title=row[2],
        content=row[3],
        author=row[4],
        created_at=row[5],
        reply_count=0
    )

@router.get("/topics/{topic_id}", response_model=Topic)
async def get_topic(topic_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Topic not found")
    
    cursor.execute("SELECT COUNT(*) FROM replies WHERE topic_id = ?", (topic_id,))
    reply_count = cursor.fetchone()[0]
    
    conn.close()
    
    return Topic(
        id=row[0],
        category=row[1],
        title=row[2],
        content=row[3],
        author=row[4],
        created_at=row[5],
        reply_count=reply_count
    )

@router.get("/topics/{topic_id}/replies", response_model=List[Reply])
async def get_replies(topic_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM replies WHERE topic_id = ? ORDER BY created_at ASC", (topic_id,))
    rows = cursor.fetchall()
    conn.close()
    
    replies = []
    for row in rows:
        replies.append(Reply(
            id=row[0],
            topic_id=row[1],
            content=row[2],
            author=row[3],
            created_at=row[4]
        ))
    
    return replies

@router.post("/replies", response_model=Reply)
async def create_reply(reply: ReplyCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM topics WHERE id = ?", (reply.topic_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Topic not found")
    
    cursor.execute("""
        INSERT INTO replies (topic_id, content, author)
        VALUES (?, ?, ?)
    """, (reply.topic_id, reply.content, reply.author))
    
    reply_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM replies WHERE id = ?", (reply_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Reply(
        id=row[0],
        topic_id=row[1],
        content=row[2],
        author=row[3],
        created_at=row[4]
    )
