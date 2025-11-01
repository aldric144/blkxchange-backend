from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
import sqlite3
import os

from app.db_models import get_db
from app.db_models.models import User, UserEvent, Article, ForumTopic, ForumReply

router = APIRouter()

COMMENTS_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "comments.db")
EVENTS_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "events.db")

@router.get("/overview")
async def get_analytics_overview(db: Session = Depends(get_db)):
    """Get overall platform analytics including views, comments, likes, and user activity"""
    
    total_users = db.query(User).count()
    
    total_articles = db.query(Article).count()
    
    total_topics = db.query(ForumTopic).count()
    total_replies = db.query(ForumReply).count()
    
    total_comments = 0
    try:
        conn = sqlite3.connect(COMMENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM comments")
        total_comments = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
    
    total_events = 0
    try:
        conn = sqlite3.connect(EVENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
    
    total_rsvps = db.query(UserEvent).count()
    
    top_contributors = []
    try:
        conn = sqlite3.connect(COMMENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT author, COUNT(*) as comment_count 
            FROM comments 
            GROUP BY author 
            ORDER BY comment_count DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        conn.close()
        
        top_contributors = [
            {"username": row[0], "comment_count": row[1]}
            for row in rows
        ]
    except Exception:
        pass
    
    most_active_forum_users = db.query(
        ForumTopic.author,
        func.count(ForumTopic.id).label('topic_count')
    ).group_by(ForumTopic.author).order_by(func.count(ForumTopic.id).desc()).limit(10).all()
    
    return {
        "total_users": total_users,
        "total_articles": total_articles,
        "total_comments": total_comments,
        "total_topics": total_topics,
        "total_replies": total_replies,
        "total_events": total_events,
        "total_rsvps": total_rsvps,
        "engagement_score": total_comments + total_topics + total_replies + total_rsvps,
        "top_contributors": top_contributors,
        "most_active_forum_users": [
            {"username": user[0], "topic_count": user[1]}
            for user in most_active_forum_users
        ]
    }

@router.get("/events")
async def get_event_analytics(db: Session = Depends(get_db)):
    """Get event-specific analytics including RSVP data and participation rates"""
    
    events_with_rsvps = []
    try:
        conn = sqlite3.connect(EVENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date, category FROM events ORDER BY date DESC")
        events = cursor.fetchall()
        conn.close()
        
        for event in events:
            event_id = event[0]
            rsvp_count = db.query(UserEvent).filter(UserEvent.event_id == event_id).count()
            
            status_breakdown = db.query(
                UserEvent.status,
                func.count(UserEvent.id)
            ).filter(UserEvent.event_id == event_id).group_by(UserEvent.status).all()
            
            events_with_rsvps.append({
                "event_id": event_id,
                "event_name": event[1],
                "event_date": event[2],
                "event_category": event[3],
                "total_rsvps": rsvp_count,
                "status_breakdown": {
                    status: count for status, count in status_breakdown
                }
            })
    except Exception as e:
        pass
    
    category_rsvps = {}
    try:
        conn = sqlite3.connect(EVENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, category FROM events")
        events = cursor.fetchall()
        conn.close()
        
        for event in events:
            event_id = event[0]
            category = event[1]
            rsvp_count = db.query(UserEvent).filter(UserEvent.event_id == event_id).count()
            
            if category not in category_rsvps:
                category_rsvps[category] = 0
            category_rsvps[category] += rsvp_count
    except Exception:
        pass
    
    most_popular_events = sorted(
        events_with_rsvps,
        key=lambda x: x['total_rsvps'],
        reverse=True
    )[:10]
    
    return {
        "events_with_rsvps": events_with_rsvps,
        "category_rsvps": category_rsvps,
        "most_popular_events": most_popular_events,
        "total_events": len(events_with_rsvps),
        "total_rsvps": sum(event['total_rsvps'] for event in events_with_rsvps),
        "average_rsvps_per_event": sum(event['total_rsvps'] for event in events_with_rsvps) / len(events_with_rsvps) if events_with_rsvps else 0
    }
