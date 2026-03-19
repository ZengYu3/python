"""
Pydantic schemas for Computer Use Product.

Used for request validation and response serialization in FastAPI.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

# -----------------------------
# Message Schemas
# -----------------------------
class MessageBase(BaseModel):
    sender: str = Field(..., description="Sender of the message: 'user' or 'agent'")
    content: str = Field(..., description="Message content")

class MessageCreate(MessageBase):
    session_id: UUID = Field(..., description="Session ID for the message")

class Message(MessageBase):
    message_id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True

# -----------------------------
# Agent State Schemas
# -----------------------------
class AgentStateBase(BaseModel):
    container_id: Optional[str] = Field(None, description="Docker container ID of the agent")
    status: str = Field("pending", description="Status of the agent container")
    last_action: Optional[dict] = Field(None, description="Last action or state info as JSON")

class AgentStateCreate(AgentStateBase):
    session_id: UUID

class AgentState(AgentStateBase):
    session_id: UUID

    class Config:
        orm_mode = True

# -----------------------------
# Session Schemas
# -----------------------------
class SessionBase(BaseModel):
    user_id: UUID = Field(..., description="User ID")
    status: str = Field("active", description="Session status")

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    session_id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    agent_state: Optional[AgentState] = None

    class Config:
        orm_mode = True