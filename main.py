"""
Main entry point for Gunicorn.
Re-exports the FastAPI app from app.main for simplified import path.
"""
from app.main import app

__all__ = ["app"]
