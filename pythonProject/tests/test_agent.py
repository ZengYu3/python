import pytest
import asyncio
import uuid

from agent import agent_manager, session as session_module, utils

@pytest.mark.asyncio
async def test_spawn_agent_container_and_remove():
    """
    Test dynamic spawn and removal of an agent container.
    """
    session_id = str(uuid.uuid4())

    # Spawn container
    container = await agent_manager.spawn_agent_container(session_id)
    assert container is not None
    assert session_id in agent_manager.active_agents

    # Remove container
    await agent_manager.remove_agent_container(session_id)
    assert session_id not in agent_manager.active_agents

@pytest.mark.asyncio
async def test_simulate_agent_processing_stream():
    """
    Test async streaming of agent response.
    """
    session_id = str(uuid.uuid4())
    user_input = "Hello Agent!"

    chunks = []
    async for chunk in agent_manager.simulate_agent_processing(session_id, user_input):
        chunks.append(chunk)

    # The response should contain all words from simulated response
    response_text = " ".join(chunks)
    assert "Hello" in response_text
    assert "Agent!" in response_text

@pytest.mark.asyncio
async def test_session_message_integration():
    """
    Test session creation, adding messages, and streaming agent responses.
    """
    user_id = str(uuid.uuid4())
    session_id = session_module.create_session(user_id)

    # Add user message
    session_module.add_message(session_id, sender="user", content="Test message")

    messages = session_module.get_messages(session_id)
    assert len(messages) == 1
    assert messages[0]["sender"] == "user"

    # Simulate agent response and store it
    agent_chunks = []
    async for chunk in agent_manager.simulate_agent_processing(session_id, "Hello"):
        agent_chunks.append(chunk)
        session_module.add_message(session_id, sender="agent", content=chunk)

    # Check that messages now include agent chunks
    messages = session_module.get_messages(session_id)
    agent_messages = [m for m in messages if m["sender"] == "agent"]
    assert len(agent_messages) == len(agent_chunks)