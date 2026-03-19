"""
Utility functions for agent operations.
"""

import asyncio
import random

async def simulate_agent_response(user_input: str, delay_range=(0.2, 0.5)):
    """
    Simulate streaming agent response for a given user input.

    Args:
        user_input (str): Message from user
        delay_range (tuple): Min and max delay per token

    Yields:
        str: Chunks of agent response
    """
    response = f"Agent response to: {user_input}"
    tokens = response.split()

    for token in tokens:
        await asyncio.sleep(random.uniform(*delay_range))
        yield token

def format_message(sender: str, content: str) -> dict:
    """
    Format a message dictionary.

    Args:
        sender (str): "user" or "agent"
        content (str): Message content

    Returns:
        dict: Formatted message
    """
    from datetime import datetime
    return {
        "sender": sender,
        "content": content,
        "timestamp": datetime.utcnow()
    }