from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agent import agent_manager, session as session_module, utils
import asyncio

router = APIRouter()

# Active WebSocket connections: session_id -> websocket
active_connections = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time agent interaction.
    Dynamically spawns a container and streams agent responses.
    """
    await websocket.accept()

    # Step 1: Create a new session
    session_id = session_module.create_session(user_id)
    print(f"[WebSocket] New session {session_id} for user {user_id}")

    # Step 2: Spawn agent container
    container = await agent_manager.spawn_agent_container(session_id)

    # Save connection
    active_connections[session_id] = websocket

    try:
        while True:
            # Receive user message
            data = await websocket.receive_text()
            print(f"[Session {session_id}] User says: {data}")

            # Store user message
            session_module.add_message(session_id, sender="user", content=data)

            # Step 3: Stream agent response
            async for chunk in agent_manager.simulate_agent_processing(session_id, data):
                # Send each chunk to WebSocket
                await websocket.send_text(chunk)

                # Store agent chunk as a message
                session_module.add_message(session_id, sender="agent", content=chunk)

    except WebSocketDisconnect:
        print(f"[Session {session_id}] User disconnected")
        # Step 4: End session
        session_module.end_session(session_id)
        # Remove agent container
        await agent_manager.remove_agent_container(session_id)
        # Remove active connection
        active_connections.pop(session_id, None)