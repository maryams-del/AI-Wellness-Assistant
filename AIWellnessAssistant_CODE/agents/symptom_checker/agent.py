# =============================================================================
# agents/google_adk/agent.py

## updateedddd


from datetime import datetime  
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
load_dotenv() 

class SymptomCheckerAgent:

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):

        self._agent = self._build_agent() 
        self._user_id = "symptom_checker_user" 

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
            name="symptom_checker",
            description="Evaluates reported symptoms and provides basic health insights.",
            instruction=(
                "Mention which agent is responding"
                "The user will describe symptoms (e.g. fatigue, fever, pain).\n\n"
                "Make it short, not more than 7 lines, and to the point"
                "Do not be friendly or apologetic. No introductions or summaries.\n"
                "Do not repeat what the user said. Do not show empathy or reassurance.\n\n"
                "Be clear. Be brief. Give the bullet points and stop."
                "Dont ask questions in return"
            )

        )

    async def invoke(self, query: str, session_id: str) -> str:

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

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )

        last_event = None
        async for event in self._runner.run_async(
            user_id=self._user_id,
            session_id=session.id,
            new_message=content
        ):
            last_event = event


        if not last_event or not last_event.content or not last_event.content.parts:
            return ""

        return "\n".join([p.text for p in last_event.content.parts if p.text])


    async def stream(self, query: str, session_id: str):

        yield {
            "is_task_complete": True,
            "content": f"Please describe your symptoms in as much detail as possible for analysis."
        }

    
