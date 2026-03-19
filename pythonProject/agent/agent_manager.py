"""
Agent Manager module.

Manages AI agent containers for each session dynamically.
Provides async spawn/remove operations and container tracking.
"""

import docker
import asyncio
from typing import Optional, Dict

# Docker client (ensure Docker is running locally)
client = docker.from_env()

# Active sessions -> containers mapping
active_agents: Dict[str, docker.models.containers.Container] = {}

# Agent image name (build from Dockerfile.agent)
AGENT_IMAGE = "computer-use-product_agent:latest"

async def spawn_agent_container(session_id: str) -> docker.models.containers.Container:
    """
    Spawn a new agent container for a session asynchronously.

    Args:
        session_id (str): Unique session ID

    Returns:
        docker.models.containers.Container: The container object
    """
    print(f"[AgentManager] Spawning container for session {session_id}...")
    container = client.containers.run(
        AGENT_IMAGE,
        name=f"agent_{session_id}",
        detach=True,
        tty=True,
        remove=True  # automatically remove container after stop
    )
    active_agents[session_id] = container
    print(f"[AgentManager] Container spawned: {container.name}")
    return container

async def remove_agent_container(session_id: str):
    """
    Stop and remove the agent container for a session.

    Args:
        session_id (str): Unique session ID
    """
    container = active_agents.get(session_id)
    if container:
        print(f"[AgentManager] Removing container for session {session_id}...")
        try:
            container.stop()
            print(f"[AgentManager] Container stopped: {container.name}")
        except Exception as e:
            print(f"[AgentManager] Error stopping container: {e}")
        finally:
            active_agents.pop(session_id, None)

def get_agent_container(session_id: str) -> Optional[docker.models.containers.Container]:
    """
    Retrieve the active container for a session if exists.

    Args:
        session_id (str): Unique session ID

    Returns:
        Optional[docker.models.containers.Container]: container object or None
    """
    return active_agents.get(session_id)

async def simulate_agent_processing(session_id: str, user_input: str, delay_range=(0.2, 0.5)):
    """
    Placeholder async function to simulate agent processing for a session.

    Args:
        session_id (str): Session ID
        user_input (str): User message
        delay_range (tuple): Min/max delay per token

    Yields:
        str: Streaming response chunks
    """
    from .utils import simulate_agent_response
    async for token in simulate_agent_response(user_input, delay_range):
        yield token

# Example test routine
if __name__ == "__main__":
    import uuid

    async def test():
        session_id = str(uuid.uuid4())
        container = await spawn_agent_container(session_id)
        print(f"Container {container.name} spawned for session {session_id}")

        async for chunk in simulate_agent_processing(session_id, "Hello agent!"):
            print(f"[{session_id}] Agent chunk: {chunk}")

        await remove_agent_container(session_id)
        print(f"Session {session_id} container removed.")

    asyncio.run(test())