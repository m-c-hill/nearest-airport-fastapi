"""
Initialise the FastAPI app using the app factory method from api/__init__.py
"""

from app.api import create_app

app = create_app()
