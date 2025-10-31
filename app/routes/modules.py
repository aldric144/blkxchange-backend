from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "modules.db")

class ModuleCreate(BaseModel):
    title: str
    category: str
    description: str
    video_url: Optional[str] = None

class Module(BaseModel):
    id: int
    title: str
    category: str
    description: str
    video_url: Optional[str] = None
    created_at: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            video_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.get("/", response_model=List[Module])
async def get_modules(category: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM modules WHERE category = ? ORDER BY created_at DESC", (category,))
    else:
        cursor.execute("SELECT * FROM modules ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    modules = []
    for row in rows:
        modules.append(Module(
            id=row[0],
            title=row[1],
            category=row[2],
            description=row[3],
            video_url=row[4],
            created_at=row[5]
        ))
    
    return modules

@router.post("/", response_model=Module)
async def create_module(module: ModuleCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO modules (title, category, description, video_url)
        VALUES (?, ?, ?, ?)
    """, (module.title, module.category, module.description, module.video_url))
    
    module_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Module(
        id=row[0],
        title=row[1],
        category=row[2],
        description=row[3],
        video_url=row[4],
        created_at=row[5]
    )

@router.get("/{module_id}", response_model=Module)
async def get_module(module_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return Module(
        id=row[0],
        title=row[1],
        category=row[2],
        description=row[3],
        video_url=row[4],
        created_at=row[5]
    )

@router.put("/{module_id}", response_model=Module)
async def update_module(module_id: int, module: ModuleCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Module not found")
    
    cursor.execute("""
        UPDATE modules 
        SET title = ?, category = ?, description = ?, video_url = ?
        WHERE id = ?
    """, (module.title, module.category, module.description, module.video_url, module_id))
    
    conn.commit()
    
    cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Module(
        id=row[0],
        title=row[1],
        category=row[2],
        description=row[3],
        video_url=row[4],
        created_at=row[5]
    )

@router.delete("/{module_id}")
async def delete_module(module_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Module not found")
    
    cursor.execute("DELETE FROM modules WHERE id = ?", (module_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Module deleted successfully"}
