"""
SQLAlchemy ORM models for Computer Use Product.

Defines:
- Session
- Message
- AgentState
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

# -----------------------------
# Session Model
# -----------------------------
class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    agent_state = relationship("AgentState", back_populates="session", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id}, status={self.status})>"

# -----------------------------
# Message Model
# -----------------------------
class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" or "agent"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message(message_id={self.message_id}, sender={self.sender})>"

# -----------------------------
# AgentState Model
# -----------------------------
class AgentState(Base):
    __tablename__ = "agent_state"

    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"), primary_key=True)
    container_id = Column(String(50), nullable=True)
    status = Column(String(20), default="pending")
    last_action = Column(JSONB, nullable=True)

    session = relationship("Session", back_populates="agent_state")

    def __repr__(self):
        return f"<AgentState(session_id={self.session_id}, status={self.status})>"