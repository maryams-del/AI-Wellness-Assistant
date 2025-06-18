
import os                           
import uuid                     
import logging                     
from dotenv import load_dotenv   

load_dotenv()
import re
from google.adk.agents.llm_agent import LlmAgent

from google.adk.sessions import InMemorySessionService

from google.adk.memory.in_memory_memory_service import InMemoryMemoryService

from google.adk.artifacts import InMemoryArtifactService

from google.adk.runners import Runner

from google.adk.agents.readonly_context import ReadonlyContext

from google.adk.tools.tool_context import ToolContext

from google.genai import types           
from server.task_manager import InMemoryTaskManager

from models.request import SendTaskRequest, SendTaskResponse
from google.adk.tools.function_tool import FunctionTool
from models.task import Message, TaskStatus, TaskState, TextPart
from agents.host_agent.agent_connect import AgentConnector
from models.agent import AgentCard

logger = logging.getLogger(__name__)


class OrchestratorAgent:

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, agent_cards: list[AgentCard]):
        self.connectors = {
            card.name: AgentConnector(card.name, card.url)
            for card in agent_cards
        }
        logger.info(f"Discovered child agents: {list(self.connectors.keys())}")
        self._agent = self._build_agent()
        self._user_id = "orchestrator_user"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def _build_agent(self) -> LlmAgent:

        return LlmAgent(
            model="gemini-1.5-flash-latest",    
            name="orchestrator_agent",          
            description="Delegates user queries to child A2A agents based on intent.",
            instruction=self._root_instruction, 
            tools=[
                self._list_agents,           
                self._delegate_task           
            ],
        )

    def _root_instruction(self, context: ReadonlyContext) -> str:
        agent_list = "\n".join(f"- {name}" for name in self.connectors)
        print("Available agents:", self.connectors.keys())
        return(
            "You are a Wellness Orchestrator. Your job is to understand user health concerns "
            "and route them to the right specialist AI agent.\n"
            "You can use two tools:\n"
            "1) list_agents() – list all available wellness agents\n"
            "2) delegate_task(agent_name, message) – send the user's concern to a specific agent\n"
            "\n"
            "Route the following:\n"
            "- Symptoms (e.g. pain, fatigue, discomfort) → send to 'SymptomCheckerAgent'\n"
            "- Habits (e.g. diet, sleep, exercise, hydration) → send to 'LifestyleRecommenderAgent'\n"
            "\n"
            "Always use delegate_task(agent_name, message) and return the full response from the agent. Do not generate your own replies. Just pass back what the agent says."
            "Example: User says 'I feel dizzy' → call delegate_task('SymptomCheckerAgent', 'I feel dizzy') and return exactly what the agent says."
        )

    def _list_agents(self) -> list[str]:
        return list(self.connectors.keys())

    async def _delegate_task(
        self,
        agent_name: str,
        message: str,
        tool_context: ToolContext
    ) -> str:

        if agent_name not in self.connectors:
            raise ValueError(f"Unknown agent: {agent_name}")
        connector = self.connectors[agent_name]

        state = tool_context.state
        if "session_id" not in state:
            state["session_id"] = str(uuid.uuid4())
        session_id = state["session_id"]

        child_task = await connector.send_task(message, session_id)

        print("Child task response:", child_task.history)
        tool_context.reply_text = (
            child_task.history[-1].parts[0].text
            if child_task.history and len(child_task.history) > 1
            else child_task.history[0].parts[0].text
            if child_task.history
            else ""
        )

        return tool_context.reply_text
    
    async def invoke(self, query: str, session_id: str) -> str:
        lines = re.split(r'[.,!?\n]+', query.strip())
        lines = [line.strip() for line in lines if line.strip()]
        print("SPLIT INPUT LINES:", lines)
        if not lines:
            return "Please enter a valid message."
        
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                session_id=session_id,
                state={}
            )
        responses = []

        for line in lines:
            content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=line)]
            )

            last_event = None
            async for event in self._runner.run_async(
                user_id=self._user_id,
                session_id=session.id,
                new_message=content
            ):
                last_event = event
            if last_event and last_event.content and last_event.content.parts:
                response = "\n".join([p.text for p in last_event.content.parts if p.text])
                if response:
                    responses.append(response)
        return "\n\n".join(responses) if responses else "No response generated."


class OrchestratorTaskManager(InMemoryTaskManager):

    def __init__(self, agent: OrchestratorAgent):
        super().__init__()     
        self.agent = agent      

    def _get_user_text(self, request: SendTaskRequest) -> str:

        return request.params.message.parts[0].text

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        logger.info(f"OrchestratorTaskManager received task {request.params.id}")

        task = await self.upsert_task(request.params)

        user_text = self._get_user_text(request)
        response_text = await self.agent.invoke(user_text, request.params.sessionId)

        reply = Message(role="agent", parts=[TextPart(text=response_text)])
        async with self.lock:
            task.status = TaskStatus(state=TaskState.COMPLETED)
            task.history.append(reply)

        return SendTaskResponse(id=request.id, result=task)
