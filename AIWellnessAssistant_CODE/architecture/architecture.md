# 🧱 AI Wellness Assistant – System Architecture

## 🗂️ Components

- **User (Web Browser)**: Enters messages via a chat UI
- **Flask UI (localhost:8000)**: Serves the frontend, captures input, and forwards it to the OrchestratorAgent via JSON-RPC
- **OrchestratorAgent (localhost:10002)**: Determines the intent and delegates to one of the child agents
- **SymptomCheckerAgent (localhost:10001)**: Handles health-related symptoms
- **LifestyleRecommenderAgent (localhost:10000)**: Handles behavior and lifestyle advice

## 🔀 Message Flow

```text
User → Flask UI → OrchestratorAgent
           ↓                    ↓
         Receives        Delegates to:
                          - SymptomCheckerAgent
                          - LifestyleRecommenderAgent
