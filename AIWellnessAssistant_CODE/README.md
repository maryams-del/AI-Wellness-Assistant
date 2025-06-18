# 🤖 AI Wellness Assistant using Agent2Agent (A2A) – Lifestyle & Symptom Checker Agents with Google ADK

This project demonstrates a minimal implementation of an AI Wellness Assistant using Google's [Agent Development Kit (ADK)](https://github.com/google/agent-development-kit). It showcases how to build and orchestrate multi-agent interactions with JSON-RPC using A2A patterns

This example demonstrates how to build, serve, and interact with three A2A agents:
1. **LifestyleRecommenderAgent** –provides recommendations based on sleep, diet, and daily habits.
2. **SymptomCheckerAgent** – interprets symptoms and gives user-friendly health insights.
3. **OrchestratorAgent** –  routes messages intelligently between agents based on detected intent.

All of them work together seamlessly via A2A discovery and JSON-RPC.

---

## 📦 Project Structure

```bash
version_3_multi_agent/
├── .env                         # Your GOOGLE_API_KEY (not committed)
├── pyproject.toml              # Dependency config
├── README.md                   # You are reading it!
├── app/
│   └── cmd/
│       └── cmd.py              # CLI to interact with the OrchestratorAgent
├── agents/
│   ├── lifestyle_recommender_agent/
│   │   ├── __main__.py         # Starts LifestyleRecommenderAgent server
│   │   ├── agent.py            # Gemini-based time agent
│   │   └── task_manager.py     # In-memory task handler for LifestyleRecommenderAgent
│   ├── symptom_checker_agent/
│   │   ├── __main__.py         # Starts SymptomCheckerAgent server
│   │   ├── agent.py            # Gemini-based time agent
│   │   └── task_manager.py     # Task handler for SymptomCheckerAgent
│   └── host_agent/
│       ├── entry.py            # CLI to start OrchestratorAgent server
│       ├── orchestrator.py     # LLM router + TaskManager for OrchestratorAgent
│       └── agent_connect.py    # Helper to call child A2A agents
├── server/
│   ├── server.py               # A2A JSON-RPC server implementation
│   └── task_manager.py         # Base in-memory task manager interface
└── utilities/
    ├── discovery.py            # Finds agents via `agent_registry.json`
    └── agent_registry.json     # List of child-agent URLs (one per line)
```

---

## 🛠️ Setup

1. **Clone & navigate**

    ```bash
    git clone https://github.com/theailanguage/a2a_samples.git
    ```

2. **Create & activate a venv**

    ```bash
    python -m venv .venv
    .venv/Scripts/Activate
    ```

3. **Install dependencies**

    ```bash
    pip install asyncclick click fastapi google-adk google-genai httpx httpx-sse pydantic python-dotenv starlette uvicorn    
    ```

4. **Set your API key**

    Create `.env` at the project root:
    ```bash
    echo "GOOGLE_API_KEY=AIzaSyANqJ-Zgtjru2C3oMmpx_mQDgjSVD6Dvmk" > .env
    ```

---

## 🎬 Demo Walkthrough

**Start the LifestyleRecommenderAgent**
```bash
python -m agents.lifestyle_recommender \
  --host localhost --port 10000
```

**Start the SymptomCheckerAgent**
```bash
python -m agents.symptom_checker \
  --host localhost --port 10001
```

**Start the Orchestrator (Host) Agent**
```bash
python -m agents.host_agent.entry \
  --host localhost --port 10002
```

**Launch the CLI (cmd.py)**
```bash
python -m app.cmd.cmd --agent http://localhost:10002
```

**Try it out!**
```bash
> My eyes are sore
Agent says: * Eye strain from screen time.
            * Rest your eyes and use artificial tears.
            * See an ophthalmologist if symptoms worsen or persist.   

> I sleep 2 hours daily
Agent says: * Gradually increase sleep by 30–60 minutes per night.        
            * Avoid screens and caffeine 2 hours before bed.
            * Keep a consistent sleep and wake schedule.


> I eat very unhealthy food, and my stomach hurts
Agent says: * Gradually replace unhealthy snacks with fruits and vegetables.
            * Cook more meals at home using fresh ingredients.
            * Reduce portion sizes.

            * Indigestion or gas.
            * Drink fluids and avoid trigger foods.
            * Consult a doctor if pain is severe or persistent.
```

---

## 🔍 How It Works

1. **Discovery**: OrchestratorAgent reads `utilities/agent_registry.json`, fetches each agent’s `/​.well-known/agent.json`.
2. **Routing**: Based on intent, the Orchestrator’s LLM calls its tools:
   - `list_agents()` → lists child-agent names
   - `delegate_task(agent_name, message)` → forwards tasks
3. **Child Agents**:
   - SymptomCheckerAgent leverages Gemini to interpret user health complaints and return empathetic, informative responses.
   - LifestyleRecommenderAgent uses Gemini to respond to the given query about lifestyle related issues.
4. **JSON-RPC**: Agents communicate using A2A-compliant JSON-RPC 2.0 over HTTP, implemented via FastAPI/Starlette and Uvicorn.

---
## Testing
# See test_scenarios.md in "testing" folder
## Architecture:
# See "architecture" folder

## 📖 Learn More

- A2A GitHub: https://github.com/google/A2A  
- Google ADK: https://github.com/google/agent-development-kit


