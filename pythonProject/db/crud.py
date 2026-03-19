"""
CRUD operations for sessions, messages, and agent state.

Currently, this is a placeholder using in-memory storage.
Later, replace with database integration (e.g., SQLAlchemy + PostgreSQL).
"""

from typing import List, Dict
from datetime import datetime
import uuid

# Placeholder in-memory stores
sessions_store: Dict[str, Dict] = {}
messages_store: Dict[str, List[Dict]] = {}
agent_state_store: Dict[str, Dict] = {}

# -----------------------------
# Session CRUD
# -----------------------------
def create_session(user_id: str) -> str:
    """
    Create a new session and store metadata.
    """
    session_id = str(uuid.uuid4())
    sessions_store[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    messages_store[session_id] = []
    agent_state_store[session_id] = {"container_id": None, "status": "pending"}
    return session_id

def get_session(session_id: str) -> Dict:
    """
    Retrieve session info.
    """
    return sessions_store.get(session_id)

def end_session(session_id: str):
    """
    Mark session as ended.
    """
    if session_id in sessions_store:
        sessions_store[session_id]["status"] = "ended"
        sessions_store[session_id]["updated_at"] = datetime.utcnow()

# -----------------------------
# Message CRUD
# -----------------------------
def add_message(session_id: str, sender: str, content: str):
    """
    Add a message to a session.
    """
    if session_id not in messages_store:
        raise ValueError(f"Session {session_id} not found")
    messages_store[session_id].append({
        "sender": sender,
        "content": content,
        "timestamp": datetime.utcnow()
    })
    # Update session timestamp
    sessions_store[session_id]["updated_at"] = datetime.utcnow()

def get_messages(session_id: str) -> List[Dict]:
    """
    Retrieve all messages for a session.
    """
    if session_id not in messages_store:
        raise ValueError(f"Session {session_id} not found")
    return messages_store[session_id]

# -----------------------------
# Agent State CRUD
# -----------------------------
def set_agent_state(session_id: str, container_id: str, status: str):
    """
    Update agent state for a session.
    """
    if session_id not in agent_state_store:
        agent_state_store[session_id] = {}
    agent_state_store[session_id]["container_id"] = container_id
    agent_state_store[session_id]["status"] = status

def get_agent_state(session_id: str) -> Dict:
    """
    Retrieve agent state for a session.
    """
    return agent_state_store.get(session_id, {})