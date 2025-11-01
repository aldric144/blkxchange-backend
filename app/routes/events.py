from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

from app.db_models import get_db
from app.db_models.models import UserEvent

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

class EventWithRSVP(BaseModel):
    id: int
    name: str
    description: str
    category: str
    date: str
    location: str
    image_url: Optional[str] = None
    created_at: str
    rsvp_count: int = 0

class RSVPCreate(BaseModel):
    user_id: int
    status: str = "attending"

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

@router.get("/{event_id}", response_model=EventWithRSVP)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    
    rsvp_count = db.query(UserEvent).filter(UserEvent.event_id == event_id).count()
    
    return EventWithRSVP(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        date=row[4],
        location=row[5],
        image_url=row[6],
        created_at=row[7],
        rsvp_count=rsvp_count
    )

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")
    
    cursor.execute("""
        UPDATE events 
        SET name = ?, description = ?, category = ?, date = ?, location = ?, image_url = ?
        WHERE id = ?
    """, (event.name, event.description, event.category, event.date, event.location, event.image_url, event_id))
    
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

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")
    
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Event deleted successfully"}

@router.post("/{event_id}/rsvp")
async def rsvp_to_event(event_id: int, rsvp: RSVPCreate, db: Session = Depends(get_db)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    existing_rsvp = db.query(UserEvent).filter(
        UserEvent.user_id == rsvp.user_id,
        UserEvent.event_id == event_id
    ).first()
    
    if existing_rsvp:
        existing_rsvp.status = rsvp.status
        db.commit()
        db.refresh(existing_rsvp)
        return {"message": "RSVP updated successfully", "rsvp": {
            "id": existing_rsvp.id,
            "user_id": existing_rsvp.user_id,
            "event_id": existing_rsvp.event_id,
            "status": existing_rsvp.status,
            "created_at": existing_rsvp.created_at.isoformat()
        }}
    
    new_rsvp = UserEvent(
        user_id=rsvp.user_id,
        event_id=event_id,
        status=rsvp.status
    )
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    
    return {"message": "RSVP created successfully", "rsvp": {
        "id": new_rsvp.id,
        "user_id": new_rsvp.user_id,
        "event_id": new_rsvp.event_id,
        "status": new_rsvp.status,
        "created_at": new_rsvp.created_at.isoformat()
    }}
