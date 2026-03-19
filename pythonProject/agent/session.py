"""
Session management module.

Handles session state, history, and metadata for each AI agent session.
"""

from datetime import datetime
from typing import List, Dict

# In-memory session storage (placeholder, replace with DB integration later)
sessions_store: Dict[str, Dict] = {}


def create_session(user_id: str) -> str:
    """
    Create a new session for a user.

    Args:
        user_id (str): Unique user identifier

    Returns:
        str: session_id
    """
    import uuid
    session_id = str(uuid.uuid4())
    sessions_store[session_id] = {
        "user_id": user_id,
        "messages": [],
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    return session_id


def add_message(session_id: str, sender: str, content: str):
    """
    Add a message to a session.

    Args:
        session_id (str): Session identifier
        sender (str): "user" or "agent"
        content (str): Message content
    """
    if session_id not in sessions_store:
        raise ValueError(f"Session {session_id} not found.")

    message = {
        "sender": sender,
        "content": content,
        "timestamp": datetime.utcnow()
    }
    sessions_store[session_id]["messages"].append(message)
    sessions_store[session_id]["updated_at"] = datetime.utcnow()


def get_messages(session_id: str) -> List[Dict]:
    """
    Retrieve message history for a session.

    Args:
        session_id (str): Session identifier

    Returns:
        List[Dict]: List of messages
    """
    if session_id not in sessions_store:
        raise ValueError(f"Session {session_id} not found.")
    return sessions_store[session_id]["messages"]


def end_session(session_id: str):
    """
    Mark session as ended.

    Args:
        session_id (str): Session identifier
    """
    if session_id in sessions_store:
        sessions_store[session_id]["status"] = "ended"
        sessions_store[session_id]["updated_at"] = datetime.utcnow()