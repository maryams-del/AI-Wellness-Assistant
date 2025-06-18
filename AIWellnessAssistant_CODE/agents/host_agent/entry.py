#
# UPDATEDDDDDDDDD

import asyncio                              # Built-in for running async coroutines
import logging                              # Standard Python logging module
import click                                # Library for building CLI interfaces
from utilities.discovery import DiscoveryClient
from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.host_agent.orchestrator import (
    OrchestratorAgent,
    OrchestratorTaskManager
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--host", default="localhost",
    help="Host to bind the OrchestratorAgent server to"
)
@click.option(
    "--port", default=10002,
    help="Port for the OrchestratorAgent server"
)
@click.option(
    "--registry",
    default=None,
    help=(
        "Path to JSON file listing child-agent URLs. "
        "Defaults to utilities/agent_registry.json"
    )
)
def main(host: str, port: int, registry: str):

    discovery = DiscoveryClient(registry_file=registry)
    agent_cards = asyncio.run(discovery.list_agent_cards())

    if not agent_cards:
        logger.warning(
            "No agents found in registry – the orchestrator will have nothing to call"
        )

    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="wellness_orchestrate",                          # Unique skill identifier
        name="Wellness Coordinator",                  # Human-friendly name
        description=(
            "Routes user health concerns and lifestyle queries to the appropriate"
            "AI wellness agent, such as symptom checker or lifestyle recommendor."
        ),
        tags=["health", "wellness", "lifestyle", "symtom checker", "coordinator"],       # Keywords to aid discovery
        examples=[                                  # Sample user queries
            "I've been feeling fatigued and dizzy lately",
            "I sleep 5 hours a night, is that enough?",
            "What should I eat to manage my cholesterol?",
            "I have a sore throat and headache. What could it be?",
            "Suggest a fitness routine for a sedentary lifestyle."
        ]
    )
    orchestrator_card = AgentCard(
        name="OrchestratorAgent",
        description="Delegates tasks to discovered child agents",
        url=f"http://{host}:{port}/",             # Public endpoint
        version="1.0.0",
        defaultInputModes=["text"],                # Supported input modes
        defaultOutputModes=["text"],               # Supported output modes
        capabilities=capabilities,
        skills=[skill]
    )

    # 3) Instantiate the OrchestratorAgent and its TaskManager
    orchestrator = OrchestratorAgent(agent_cards=agent_cards)
    task_manager = OrchestratorTaskManager(agent=orchestrator)

    # 4) Create and start the A2A server
    server = A2AServer(
        host=host,
        port=port,
        agent_card=orchestrator_card,
        task_manager=task_manager
    )
    server.start()


if __name__ == "__main__":
    main()
