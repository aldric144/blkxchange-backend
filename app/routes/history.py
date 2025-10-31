from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "history.db")

class HistoryCreate(BaseModel):
    title: str
    year: int
    description: str
    image_url: Optional[str] = None

class History(BaseModel):
    id: int
    title: str
    year: int
    description: str
    image_url: Optional[str] = None
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[History])
async def get_history_entries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY year DESC")
    rows = cursor.fetchall()
    conn.close()
    
    entries = []
    for row in rows:
        entries.append(History(
            id=row[0],
            title=row[1],
            year=row[2],
            description=row[3],
            image_url=row[4],
            created_at=row[5]
        ))
    
    return entries

@router.post("/", response_model=History)
async def create_history_entry(history: HistoryCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO history (title, year, description, image_url)
        VALUES (?, ?, ?, ?)
    """, (history.title, history.year, history.description, history.image_url))
    
    history_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM history WHERE id = ?", (history_id,))
    row = cursor.fetchone()
    conn.close()
    
    return History(
        id=row[0],
        title=row[1],
        year=row[2],
        description=row[3],
        image_url=row[4],
        created_at=row[5]
    )

@router.get("/{history_id}", response_model=History)
async def get_history_entry(history_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE id = ?", (history_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="History entry not found")
    
    return History(
        id=row[0],
        title=row[1],
        year=row[2],
        description=row[3],
        image_url=row[4],
        created_at=row[5]
    )
