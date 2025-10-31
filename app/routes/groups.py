from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "groups.db")

class GroupCreate(BaseModel):
    name: str
    description: str
    category: str
    is_private: bool = True
    image_url: Optional[str] = None

class Group(BaseModel):
    id: int
    name: str
    description: str
    category: str
    is_private: bool
    image_url: Optional[str] = None
    member_count: int = 0
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            is_private BOOLEAN NOT NULL DEFAULT 1,
            image_url TEXT,
            member_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[Group])
async def get_groups(category: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM groups WHERE category = ? ORDER BY created_at DESC", (category,))
    else:
        cursor.execute("SELECT * FROM groups ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    groups = []
    for row in rows:
        groups.append(Group(
            id=row[0],
            name=row[1],
            description=row[2],
            category=row[3],
            is_private=bool(row[4]),
            image_url=row[5],
            member_count=row[6],
            created_at=row[7]
        ))
    
    return groups

@router.post("/", response_model=Group)
async def create_group(group: GroupCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO groups (name, description, category, is_private, image_url, member_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (group.name, group.description, group.category, group.is_private, group.image_url, 0))
    
    group_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Group(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        is_private=bool(row[4]),
        image_url=row[5],
        member_count=row[6],
        created_at=row[7]
    )

@router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return Group(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        is_private=bool(row[4]),
        image_url=row[5],
        member_count=row[6],
        created_at=row[7]
    )
