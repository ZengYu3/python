from fastapi import APIRouter, HTTPException, Query
from agent import session as session_module

router = APIRouter()

@router.post("/start")
async def start_session(user_id: str = Query(..., description="Unique user identifier")):
    """
    Create a new session for a user.
    """
    session_id = session_module.create_session(user_id)
    return {
        "session_id": session_id,
        "user_id": user_id,
        "status": "active"
    }

@router.get("/{session_id}")
async def get_session(session_id: str):
    """
    Retrieve session information and status.
    """
    try:
        session_data = session_module.sessions_store.get(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        return {
            "session_id": session_id,
            "user_id": session_data["user_id"],
            "status": session_data["status"],
            "created_at": session_data["created_at"],
            "updated_at": session_data["updated_at"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))