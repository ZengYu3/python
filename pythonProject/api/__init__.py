"""
api package initializer.

Contains:
- main.py: FastAPI entry point
- websocket.py: WebSocket streaming logic
- routes/: REST API endpoints for sessions, messages, and health checks
"""

from . import main
from . import websocket
from . import routes

__all__ = [
    "main",
    "websocket",
    "routes",
]