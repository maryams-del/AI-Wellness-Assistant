# =============================================================================
# agents/google_adk/task_manager.py
# =============================================================================
## updatedddd
import logging  
from server.task_manager import InMemoryTaskManager
from agents.symptom_checker.agent import SymptomCheckerAgent

from models.request import SendTaskRequest, SendTaskResponse
from models.task import Message, Task, TextPart, TaskStatus, TaskState


logger = logging.getLogger(__name__)


class AgentTaskManager(InMemoryTaskManager):
    """
    🧠 This class connects the Gemini agent to the task system.

    - It "inherits" all the logic from InMemoryTaskManager
    - It overrides the part where we handle a new task (on_send_task)
    - It uses the Gemini agent to generate a response
    """

    def __init__(self, agent: SymptomCheckerAgent):
        super().__init__()    
        self.agent = agent   

    def _get_user_query(self, request: SendTaskRequest) -> str:
  
        return request.params.message.parts[0].text

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:

        logger.info(f"Processing new task: {request.params.id}")

        task = await self.upsert_task(request.params)

        query = self._get_user_query(request)

        result_text = await self.agent.invoke(query, request.params.sessionId)

        agent_message = Message(
            role="agent",                  
            parts=[TextPart(text=result_text)] 
        )

        async with self.lock:                  
            task.status = TaskStatus(state=TaskState.COMPLETED)  
            task.history.append(agent_message) 

        return SendTaskResponse(id=request.id, result=task)

