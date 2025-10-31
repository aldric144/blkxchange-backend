from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "legacy.db")

class LegacyCreate(BaseModel):
    name: str
    relation: str
    biography: str
    photo_url: Optional[str] = None
    era: Optional[str] = None

class Legacy(BaseModel):
    id: int
    name: str
    relation: str
    biography: str
    photo_url: Optional[str] = None
    era: Optional[str] = None
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS legacy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            relation TEXT NOT NULL,
            biography TEXT NOT NULL,
            photo_url TEXT,
            era TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[Legacy])
async def get_legacy_entries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM legacy ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    entries = []
    for row in rows:
        entries.append(Legacy(
            id=row[0],
            name=row[1],
            relation=row[2],
            biography=row[3],
            photo_url=row[4],
            era=row[5],
            created_at=row[6]
        ))
    
    return entries

@router.post("/", response_model=Legacy)
async def create_legacy_entry(legacy: LegacyCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO legacy (name, relation, biography, photo_url, era)
        VALUES (?, ?, ?, ?, ?)
    """, (legacy.name, legacy.relation, legacy.biography, legacy.photo_url, legacy.era))
    
    legacy_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM legacy WHERE id = ?", (legacy_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Legacy(
        id=row[0],
        name=row[1],
        relation=row[2],
        biography=row[3],
        photo_url=row[4],
        era=row[5],
        created_at=row[6]
    )

@router.get("/{legacy_id}", response_model=Legacy)
async def get_legacy_entry(legacy_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM legacy WHERE id = ?", (legacy_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Legacy entry not found")
    
    return Legacy(
        id=row[0],
        name=row[1],
        relation=row[2],
        biography=row[3],
        photo_url=row[4],
        era=row[5],
        created_at=row[6]
    )

@router.put("/{legacy_id}", response_model=Legacy)
async def update_legacy_entry(legacy_id: int, legacy: LegacyCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM legacy WHERE id = ?", (legacy_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Legacy entry not found")
    
    cursor.execute("""
        UPDATE legacy 
        SET name = ?, relation = ?, biography = ?, photo_url = ?, era = ?
        WHERE id = ?
    """, (legacy.name, legacy.relation, legacy.biography, legacy.photo_url, legacy.era, legacy_id))
    
    conn.commit()
    
    cursor.execute("SELECT * FROM legacy WHERE id = ?", (legacy_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Legacy(
        id=row[0],
        name=row[1],
        relation=row[2],
        biography=row[3],
        photo_url=row[4],
        era=row[5],
        created_at=row[6]
    )

@router.delete("/{legacy_id}")
async def delete_legacy_entry(legacy_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM legacy WHERE id = ?", (legacy_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Legacy entry not found")
    
    cursor.execute("DELETE FROM legacy WHERE id = ?", (legacy_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Legacy entry deleted successfully"}
