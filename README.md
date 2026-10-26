# ⚡ Alan-Nexus: Enterprise-Grade Multi-Agent Middleware for Voice & Intent Orchestration
> **Tech Stack:** FastAPI | LangGraph | Groq API (`openai/gpt-oss-20b`) | Streamlit | Python 3.10+

---

## 1. What is Alan-Nexus?

**Alan-Nexus** is an open-source, high-performance, multi-agent middleware designed to replace legacy, rigid, cloud-bound client-side intent architectures (such as Alan AI's default JavaScript SDK logic) with a **stateful, modular, and developer-sovereign Python backend**.

By decoupling voice/text capture from execution logic, Alan-Nexus empowers developers to orchestrate complex multi-turn reasoning, dynamic UI action payloads, and enterprise-grade state management using cutting-edge LLMs and agentic graphs (`LangGraph`).

---

## 2. Drawbacks of Current Alan AI Architecture

While traditional platforms like Alan AI offer quick client-side voice integration, enterprise deployments expose severe architectural bottlenecks:

* **Rigid JavaScript Intent Matching:** Default systems rely on flat regular expressions and hardcoded client-side `intent()` syntax trees that fail to grasp complex semantic nuances or multi-intent requests.
* **Cloud Black-Box Reasoning:** Developers have zero control over the underlying prompt chains, safety rails, or model routers running in the proprietary cloud layer.
* **Stateless Conversations:** Lack of native, thread-safe memory checkpointers means context is routinely lost across multi-turn user dialogues.
* **Vendor Lock-in & Latency:** Monolithic cloud execution pipelines introduce unpredictable round-trip latency and restrict custom database or API integrations.

---

## 3. How Alan-Nexus Overcomes These Bottlenecks

Alan-Nexus introduces an enterprise-ready architecture that transforms rigid voice assistants into intelligent, autonomous applications.

### **Key Optimizations & Architectural Changes:**

1. **Modular Multi-Agent Pipeline (`LangGraph`):** Instead of flat rule matching, execution is split into a stateful graph comprising specialized nodes:
* `IntentClassifier`: Dynamically maps user input to categorical actions (`CODE_EXPLAIN`, `DYNAMIC_ACTION`, `GENERAL_QA`).
* `TaskExecutor`: Executes domain-specific logic, queries external tools, and builds structured UI action payloads.
* `ResponseSynthesizer`: Condenses technical outputs into concise, human-like spoken responses.


2. **Stateful Conversation Memory (`InMemorySaver`):** Implements thread-scoped checkpointers (`thread_id`) to preserve complete multi-turn dialogue context across user sessions.
3. **Blazing-Fast Inference (`Groq Engine`):** Leverages hardware-accelerated LLM execution (`openai/gpt-oss-20b`) to bring multi-agent response times down to milliseconds.
4. **Decoupled UI Action Payloads:** The backend outputs explicit JSON control payloads alongside spoken text, allowing the client interface to autonomously trigger UI updates (e.g., opening settings panels, rendering code cards, or navigating views).

---

## 4. System Workflow

1. **Input Ingestion:** The user speaks or types a command into the **Streamlit Developer Control Plane** or client app.
2. **FastAPI Bridge:** The raw text transcript is dispatched via HTTP POST to the FastAPI backend middleware (`/api/nexus/voice`).
3. **Graph Invocation (`LangGraph`):**
* The `IntentClassifier` evaluates semantic intent.
* The `TaskExecutor` processes code explanation or triggers UI state changes.
* The `ResponseSynthesizer` crafts a concise spoken response.


4. **Action & Response Delivery:** The backend returns a structured JSON response containing the intent, spoken text, and UI action payload, which the frontend instantly renders, logs, and speaks aloud via browser text-to-speech.

---

## 5. Architecture Flowchart

```mermaid
graph TD
    A[User Voice / Text Input] -->|Streamlit Control Plane| B(FastAPI Bridge /api/nexus/voice)
    <img width="1000" height="640" alt="Screenshot 2026-10-26 235705" src="https://github.com/user-attachments/assets/0349a378-2a99-4eb8-a1e4-caed68367955" />

    B --> C{LangGraph StateGraph}
    
    C --> D[Node 1: IntentClassifier]
    <img width="1072" height="416" alt="Screenshot 2026-10-26 235754" src="https://github.com/user-attachments/assets/f357ed8d-803b-4f27-90b4-5fa2afd0deed" />

    D -->|Classifies Intent| E[Node 2: TaskExecutor]
    <img width="1197" height="606" alt="Screenshot 2026-10-26 235747" src="https://github.com/user-attachments/assets/7ac8832f-c989-4bec-8437-f49f86645132" />
    
    E -->|Executes Logic & Payload| F[Node 3: ResponseSynthesizer]
    <img width="1156" height="553" alt="Screenshot 2026-10-26 235735" src="https://github.com/user-attachments/assets/af5ac881-305e-4f07-b567-efcaadd30e83" />

    F -->|State Checkpointer| G[(InMemorySaver Thread Memory)]
    
    F --> H[Groq LLM openai/gpt-oss-20b]
    H -->|Optimized Output| I[JSON Response Payload]
    
    I --> J[Browser TTS Audio Output]
    I --> K[Real-Time Event Stream Log]
    I --> L[Live UI State Trigger e.g., Open Settings]

```

---

## 6. How to Set Up the Application

### **Prerequisites**

* Python 3.10 or higher
* A Groq API Key ([Get one here](https://console.groq.com/))

### **Step 1: Clone and Configure Environment**

```bash
git clone https://github.com/your-username/alan-nexus.git
cd alan-nexus

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic langgraph langchain-core langchain-groq python-dotenv streamlit requests

```

### **Step 2: Configure Environment Variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
PORT=8000

```

### **Step 3: Run the FastAPI Backend**

Start the high-performance asynchronous middleware server:

```bash
uvicorn main:app --reload --port 8000

```

*Verify backend is live at:* `http://localhost:8000`

### **Step 4: Launch the Streamlit Control Plane (Frontend)**

Open a **second terminal window**, activate your virtual environment, and launch the developer dashboard:

```bash
streamlit run app.py

```

*Access the control plane in your browser at:* `http://localhost:8501`

---

##  Quick Links & Live Demos

[![Live App](https://img.shields.io/badge/🚀_Live_App-Streamlit_Cloud-4f46e5?style=for-the-badge)](https://alan-nexus-gbrwqtvtu4hwbi2mkmde9z.streamlit.app/)
[![Backend API](https://img.shields.io/badge/⚡_Backend_API-Render-4ade80?style=for-the-badge)](https://alan-nexus.onrender.com)
[![Watch Demo Video](https://img.shields.io/badge/🎥_Demo_Video-Watch_Pitch-ef4444?style=for-the-badge)](https://drive.google.com/file/d/108p_OA1boaD71LFMV_bq-nRq1GwBQAER/view?usp=sharing)

---

##  Project Architecture & UI Gallery

### 1. The Developer Control Plane (Streamlit UI)
*A professional, dark-mode developer testing dashboard featuring real-time event streaming, latency tracking, and active session memory.*
> <img width="1917" height="962" alt="Screenshot 2026-10-26 220757" src="https://github.com/user-attachments/assets/a5fa1c18-993e-42b4-8fc8-0a82d49320aa" />
```text
[ Screenshot Placeholder: Live Streamlit Developer Control Plane ]

---

## 7. Future Improvements & Roadmap

* **Persistent Vector Memory:** Replace in-memory checkpointers with PostgreSQL + ChromaDB for long-term user context retention across system reboots.
* **Edge Air-Gapping:** Support fully localized open-weight models (Llama 3 8B) running via Ollama for zero-data-leakage enterprise environments.
* **WebSocket Streaming:** Upgrade FastAPI endpoints from HTTP REST to bi-directional WebSockets for real-time token streaming and sub-100ms voice streaming feedback.
