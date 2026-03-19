import pytest
from fastapi.testclient import TestClient
from api.main import app
import uuid

client = TestClient(app)

@pytest.fixture
def user_id():
    return str(uuid.uuid4())

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_session(user_id):
    response = client.post(f"/sessions/start?user_id={user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["user_id"] == user_id
    assert data["status"] == "active"

def test_send_and_get_messages(user_id):
    # Create a session
    response = client.post(f"/sessions/start?user_id={user_id}")
    session_id = response.json()["session_id"]

    # Send a user message
    response = client.post(f"/messages/send?session_id={session_id}&sender=user&content=Hello")
    assert response.status_code == 200

    # Retrieve messages
    response = client.get(f"/messages/{session_id}")
    assert response.status_code == 200
    messages = response.json()["messages"]
    assert any(msg["content"] == "Hello" for msg in messages)
    assert any(msg["sender"] == "user" for msg in messages)