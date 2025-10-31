from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "events.db")

class EventCreate(BaseModel):
    name: str
    description: str
    category: str
    date: str
    location: str
    image_url: Optional[str] = None

class Event(BaseModel):
    id: int
    name: str
    description: str
    category: str
    date: str
    location: str
    image_url: Optional[str] = None
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[Event])
async def get_events(category: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM events WHERE category = ? ORDER BY date ASC", (category,))
    else:
        cursor.execute("SELECT * FROM events ORDER BY date ASC")
    
    rows = cursor.fetchall()
    conn.close()
    
    events = []
    for row in rows:
        events.append(Event(
            id=row[0],
            name=row[1],
            description=row[2],
            category=row[3],
            date=row[4],
            location=row[5],
            image_url=row[6],
            created_at=row[7]
        ))
    
    return events

@router.post("/", response_model=Event)
async def create_event(event: EventCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO events (name, description, category, date, location, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (event.name, event.description, event.category, event.date, event.location, event.image_url))
    
    event_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Event(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        date=row[4],
        location=row[5],
        image_url=row[6],
        created_at=row[7]
    )

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return Event(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        date=row[4],
        location=row[5],
        image_url=row[6],
        created_at=row[7]
    )
