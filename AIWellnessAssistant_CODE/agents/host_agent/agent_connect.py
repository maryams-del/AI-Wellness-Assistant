# =============================================================================
# agents/host_agent/agent_connect.py
# =============================================================================
# 🎯 Purpose:
# Provides a simple wrapper (`AgentConnector`) around the A2AClient to send tasks
# to any remote agent identified by a base URL. This decouples the Orchestrator
# from low-level HTTP details and HTTP client setup.
# =============================================================================

### UPDATEDDDD 



import uuid                           # Standard library for generating unique IDs
import logging                        # Standard library for configurable logging

# Import our custom A2AClient which handles JSON-RPC task requests
from client.client import A2AClient
# Import Task model to represent the full task response
from models.task import Task

# Create a logger for this module using its namespace
logger = logging.getLogger(__name__)


class AgentConnector:

    def __init__(self, name: str, base_url: str):

        self.name = name

        self.client = A2AClient(url=base_url)
        logger.info(f"AgentConnector: initialized for {self.name} at {base_url}")

    async def send_task(self, message: str, session_id: str) -> Task:

        task_id = uuid.uuid4().hex

        payload = {
            "id": task_id,
            "sessionId": session_id,
            "message": {
                "role": "user",                # Indicates this message is from the user
                "parts": [                       # Wrap the text in a list of parts
                    {"type": "text", "text": message}
                ]
            }
        }

        task_result = await self.client.send_task(payload)

        logger.info(f"AgentConnector: received response from {self.name} for task {task_id}")
        # Return the Task Pydantic model for further processing by the orchestrator
        return task_result
