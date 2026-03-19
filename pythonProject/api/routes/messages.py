from fastapi import APIRouter, HTTPException, Query
from agent import session as session_module
from typing import List, Dict

router = APIRouter()

@router.post("/send")
async def send_message(
    session_id: str = Query(..., description="Session ID"),
    sender: str = Query(..., description="'user' or 'agent'"),
    content: str = Query(..., description="Message content")
):
    """
    Send a message to a session (user or agent).
    """
    try:
        session_module.add_message(session_id, sender=sender, content=content)
        return {"status": "sent", "session_id": session_id, "sender": sender, "content": content}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}")
async def get_messages(session_id: str) -> List[Dict]:
    """
    Retrieve message history for a session.
    """
    try:
        messages = session_module.get_messages(session_id)
        return {"session_id": session_id, "messages": messages}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))