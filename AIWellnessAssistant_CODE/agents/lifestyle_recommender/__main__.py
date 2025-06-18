# =============================================================================
# agents/google_adk/__main__.py

### UPDATEDDDDD 
from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill

from agents.lifestyle_recommender.task_manager import AgentTaskManager
from agents.lifestyle_recommender.agent import LifestyleRecommenderAgent
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
        id="lifestyle_recommendation",                                 
        name="Lifestyle Recommendation Tool",                      
        description="Analyzes user lifestyle habits and offers health improvement suggestions.",  
        tags=["lifestyle", "habits", "recommendation"],                                
        examples=["I sleep 4 hours and skip breakfast, is that okay?",
            "I exercise daily but eat fast food often. Advice?",
            "Is drinking soda every day bad for me?"] 
    )


    agent_card = AgentCard(
        name="LifestyleRecommenderAgent",                             
        description="Evaluates lifestyle habits and provides healthy recommendations.",  
        url=f"http://{host}:{port}/",                     
        version="1.0.0",                                 
        defaultInputModes=LifestyleRecommenderAgent.SUPPORTED_CONTENT_TYPES, 
        defaultOutputModes=LifestyleRecommenderAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,                         
        skills=[skill]                                     
    )

    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=AgentTaskManager(agent=LifestyleRecommenderAgent())
    )

    server.start()


if __name__ == "__main__":
    main()
