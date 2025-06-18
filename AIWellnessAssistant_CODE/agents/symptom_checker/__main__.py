# =============================================================================
# agents/google_adk/__main__.py

### UPDATEDDDDD 
from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill

from agents.symptom_checker.task_manager import AgentTaskManager
from agents.symptom_checker.agent import SymptomCheckerAgent
import click         
import logging        


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10002, help="Port number for the server")
def main(host, port):

    capabilities = AgentCapabilities(streaming=False)

    skill = AgentSkill(
        id="symptom_checker",
        name="Symptom Checker Tool",
        description="Analyzes user symptoms and provides health insights or flags potential conditions.",
        tags=["symptoms", "health", "diagnosis", "triage"],
        examples=[
            "I have chest pain and shortness of breath.",
            "I feel dizzy and have a headache.",
            "My throat hurts and I have a fever.",
            "I’ve been coughing non-stop for 3 days.",
        ]
    )

    agent_card = AgentCard(
        name="SymptomCheckerAgent",
        description="Evaluates symptoms shared by the user and offers relevant medical insights or cautionary advice.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=SymptomCheckerAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=SymptomCheckerAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill]
    )

    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=AgentTaskManager(agent=SymptomCheckerAgent())
    )

    server.start()


if __name__ == "__main__":
    main()
