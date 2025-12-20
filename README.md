# 🧵 AgentWeave — Agentic AI with Tool Use & RAG

**AgentWeave** is a production-style **Agentic AI application** that intelligently routes user queries between **real-time tools** and **Retrieval-Augmented Generation (RAG)** pipelines.

Built using **LangGraph**, **LangChain**, **Google Gemini**, **Qdrant**, and **Streamlit**, the project demonstrates clean, explainable, and scalable **GenAI system design** with strong emphasis on agent orchestration, vector search, and LLM evaluation.

---

## 🔍 What This Project Demonstrates

- Agentic workflows using **LangGraph**
- Tool-aware LLM reasoning (API vs knowledge routing)
- **Retrieval-Augmented Generation (RAG)**
- Vector databases and semantic search using **Qdrant**
- Embeddings with **Gemini `text-embedding-004`**
- Explainable AI via retrieved context visibility
- Persistent and isolated knowledge base management
- Modular, production-ready Python architecture
- Interactive chat UI with **Streamlit**

---

## 🚀 Key Capabilities

### 🤖 Agent Orchestration

- Deterministic routing using graph-based workflows
- Clear separation between tool execution and RAG logic
- Easily extensible agent design

### 🌦️ Real-Time Tool Integration

- Live weather data via **OpenWeather API**
- Structured responses summarized using **Google Gemini**

### 📚 Retrieval-Augmented Generation (RAG)

- PDF ingestion and chunking using `RecursiveCharacterTextSplitter`
- Semantic vector search using **Qdrant**
- Top-K retrieval for grounded LLM responses
- Strict query isolation per knowledge base

### 🔎 Explainability

- Retrieved document chunks displayed in the UI
- Source transparency for every RAG-based answer
- Reduced hallucinations through enforced context grounding

### 🖥️ Streamlit UI

- Chat-style interface with conversation history
- Streaming LLM responses
- Expandable panels for retrieved chunks and sources
- Knowledge base selection and lifecycle management

---

## 🧠 Architecture Overview

```
User Query
↓
Streamlit UI
↓
LangGraph Agent
↓
Routing Logic
├── Tool Path → OpenWeather API → Gemini Summary
└── RAG Path → Qdrant Vector Search → Gemini Answer
↓
Answer + Retrieved Chunks + Sources
```

---

## 🛠️ Tech Stack

**Languages**

- Python

**GenAI & LLMs**

- Google Gemini
- Gemini `text-embedding-004`
- Prompt engineering
- RAG-based hallucination mitigation

**Frameworks**

- LangGraph
- LangChain

**Databases**

- Qdrant (vector database)

**UI**

- Streamlit

**Tooling**

- Docker
- REST APIs
- Environment-based configuration

---

## 📄 Demo Knowledge Base

The demo uses **_Moby-Dick_** (public-domain literature) to showcase RAG behavior.
The same pipeline works without modification for enterprise documents such as manuals, policies, or internal knowledge bases.

---

## ✂️ Chunking Strategy

```python
RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=250,
)
```

Optimized for semantic coherence and retrieval quality.

---

## 🧪 Example Queries

**Tool-based**

```
What is the weather in Delhi today?
```

**RAG-based**

```
Who is Ishmael?
```

```
What is the Pequod?
```

```
Why does Captain Ahab hate the white whale?
```

---

## 📈 LangSmith Tracing & Evaluation

AgentWeave integrates **LangSmith** for observability across the agentic workflow, including routing decisions, tool calls, retrieval steps, and LLM responses.

### 🔍 Tracked Components

- LangGraph execution flow
- OpenWeather API usage
- Qdrant retrieval context
- Gemini prompt–response cycles
- Safety and guardrail behavior

---

### 1️⃣ LangGraph Execution Trace

![LangGraph Trace](screenshots/agent_graph.jpg)

---

### 2️⃣ RAG Retrieval & Vector Search Trace

![RAG Retrieval Trace](screenshots/langsmith-rag-question-ss.png)

---

### 3️⃣ Weather Agent Trace

![Weather Agent Trace](screenshots/langsmith-weather-agent-ss.png)

---

## ⚙️ Setup (Windows)

```bash
git clone https://github.com/your-username/AgentWeave.git
cd AgentWeave
```

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

Run Qdrant:

```bash
docker run -d ^
  -p 6431:6333 ^
  -p 6432:6334 ^
  qdrant/qdrant
```

Run the app:

```powershell
streamlit run app.py
```

## 📜 License

MIT License
