# AI-Wellness-Assistant
A2A MVP for AI-powered symptom checking and wellness recommendations.
# 🧠 AI Wellness Assistant – A2A-Enabled MVP

## 📌 Project Objective

The AI Wellness Assistant is a Minimum Viable Product (MVP) built using Google’s Agent-to-Agent (A2A) protocol within the My AI Network framework. The goal is to demonstrate seamless collaboration between specialized AI agents to deliver basic health insights and lifestyle recommendations — all within a constrained 10-hour development window.

---

## 📚 Background

The Agent-to-Agent (A2A) protocol standardizes JSON-RPC communication among AI agents, enabling modular, decentralized decision-making. The AI Wellness Assistant shows how multiple agents — working independently — can collaborate to deliver a valuable, real-world service using this protocol.

---

## 🧠 Key Design Principles

- **Modularity**: Each agent (Coordinator, Symptom Checker, Lifestyle Recommender) is designed independently with a single responsibility.
- **Interoperability**: JSON-RPC protocol ensures seamless agent communication.
- **Simplicity**: User inputs are interpreted by agents and returned in a user-friendly format.
- **Scalability**: Architecture allows for future addition of agents (e.g., Mental Health Agent).
- **Reliability**: Each agent runs in isolation and can be restarted independently.

---

## 🔧 Key Components Implemented

| Component               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Coordinator Agent**  | Receives user input, routes it to agents, collects responses                |
| **Symptom Checker**    | Analyzes basic symptoms and returns potential causes                        |
| **Lifestyle Recommender** | Reviews habits and suggests lifestyle adjustments                     |
| **User Interface (UI)**| Flask-based web interface for data entry and result display                 |
| **JSON-RPC Protocol**  | All communication follows JSON-RPC 2.0 standard using Flask endpoints       |
| **Documentation**      | Agent descriptions, architecture diagrams, test scenarios                   |

---

## 🖼️ System Architecture
User Input
↓
[UI Interface]
↓
[Coordinator Agent]
├──→ [Symptom Checker Agent]
└──→ [Lifestyle Recommender Agent]
↓
[Final Combined Output to User]


---

## 💻 Deployment Context

- **Language**: Python
- **Framework**: Flask (for agents and UI)
- **Execution**: Each agent runs as an independent microservice
- **Environment**: Local machine using virtual environments
- **Communication**: JSON-RPC via HTTP POST requests

---

## 💡 Use Case: Symptom Analysis + Lifestyle Suggestions

**Scenario**:  
A user experiencing “headache and eye strain” with only 5 hours of sleep and 8 hours of screen time wants actionable feedback.

**System Output**:  
- **Symptom Checker**: Likely cause: screen fatigue  
- **Lifestyle Recommender**: Increase sleep to 7–8 hours, reduce screen time, take regular breaks  

---

## ⚙️ Installation Instructions

```bash
# Clone the repository
git clone https://github.com/maryams-del/AI-Wellness-Assistant.git
cd AI-Wellness-Assistant

# Activate virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install agent dependencies individually
cd coordinator
pip install -r requirements.txt
cd ../symptom_checker
pip install -r requirements.txt
cd ../lifestyle_recommender
pip install -r requirements.txt
cd ../ui
pip install -r requirements.txt

