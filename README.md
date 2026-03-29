# 🎓 Course Planning Assistant

> An agentic RAG system built with CrewAI + ChromaDB that helps students plan courses, check prerequisites, and navigate degree requirements — all grounded in real catalog documents with verifiable citations.

---

## 📌 Overview

This project is a **multi-agent AI assistant** that answers student course-planning questions strictly based on academic catalog documents. It uses **Retrieval-Augmented Generation (RAG)** to ensure every answer is cited and grounded — no hallucinations, no guessing.

---

## 🏗️ Architecture

<img width="551" height="660" alt="Screenshot 2026-03-29 at 8 55 45 PM" src="https://github.com/user-attachments/assets/cc0277c0-fe2b-486d-8dce-8ad05356a4ec" />

---

## 🗂️ Project Structure

```
course-planning-assistant/
├── data/
│   └── catalog/
│       ├── cs_courses.txt           # 11 course descriptions
│       ├── degree_requirements.txt  # BS CS program requirements
│       └── academic_policies.txt    # Grading, repeat, credit policies
├── src/
│   └── course_planning_assistant/
│       ├── config/
│       │   ├── agents.yaml          # Agent roles, goals, backstories
│       │   └── tasks.yaml           # Task descriptions & expected outputs
│       ├── crew.py                  # CrewAI crew + RAG tool definition
│       ├── ingest.py                # Data ingestion pipeline
│       └── main.py                  # Entry point
├── output/
│   └── final_plan.md                # Last generated plan saved here
├── chroma_db/                       # Persistent vector store (auto-created)
├── .env                             # API keys
├── pyproject.toml
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/course-planning-assistant.git
cd course-planning-assistant
```

### 2. Create project using CrewAI CLI

```bash
uv tool install crewai
crewai create crew course-planning-assistant
cd course-planning-assistant
```

### 3. Install dependencies

```bash
uv add langchain-groq langchain-community chromadb sentence-transformers pypdf beautifulsoup4 requests
```

### 4. Set up environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=groq/llama3-70b-8192
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🚀 Running the Project

### Step 1 — Build the index

Ingest catalog documents into ChromaDB:

```bash
python3 src/course_planning_assistant/ingest.py
```

### Step 2 — Run the assistant

```bash
crewai run
```

Enter your query when prompted. Example:

```
Can i take CS61A? I am computer science student.
```

---

## 🤖 Agents

| Agent | Role | Key Behavior |
|---|---|---|
| **Intake Agent** | Student Profile Specialist | Extracts info, asks clarifying questions if incomplete |
| **Catalog Retriever Agent** | Research Specialist | Searches ChromaDB, always returns chunk ID + source URL |
| **Planner Agent** | Course Planning Strategist | Builds plan using ONLY retrieved evidence |
| **Verifier Agent** | Plan Auditor | Flags/removes any claim without citation |

---

## 📋 Output Format

Every response follows this structure:

```
Answer / Plan:
Why (requirements/prereqs satisfied):
Citations:
Clarifying Questions (if needed):
Assumptions / Not in catalog:
```

---

## 🗄️ RAG Configuration

| Component | Choice | Reason |
|---|---|---|
| Embeddings | `all-MiniLM-L6-v2` | Fast, free, good semantic accuracy |
| Vector Store | ChromaDB (persistent) | Easy setup, metadata filtering support |
| Chunking | Paragraph-based (`\n\n` split) | Keeps course/policy blocks intact |
| Retriever k | Top-5 per query | Enough context without noise |
| Similarity | Cosine (default) | Standard for semantic search |

---

## 📚 Data Sources

| File | Contents | Source |
|---|---|---|
| `cs_courses.txt` | 11 CS course descriptions with prereqs | UC Berkeley Course Catalog 2024-25 |
| `degree_requirements.txt` | BS CS degree requirements, breadth, electives | UC Berkeley Degree Guide 2024-25 |
| `academic_policies.txt` | Grading, repeat policy, credit limits, co-reqs | UC Berkeley Academic Policies 2024-25 |

---

## 🧪 Evaluation

Test set includes **25 queries**:
- 10 prerequisite checks (eligible / not eligible)
- 5 prerequisite chain questions (multi-hop)
- 5 program requirement questions
- 5 "not in docs" / trick questions

| Metric | Description |
|---|---|
| Citation Coverage Rate | % responses with at least one citation |
| Eligibility Correctness | Manual grading vs expected decision |
| Abstention Accuracy | % of "not in docs" queries correctly refused |

---

## 🔧 Troubleshooting

**Tool call validation error with Groq?**
```env
# Use this model in .env — more stable with CrewAI tool calling
MODEL=groq/llama3-70b-8192
```

**ChromaDB collection not found?**
```bash
# Re-run ingestion first
python3 src/course_planning_assistant/ingest.py
```

**HuggingFace warning about unauthenticated requests?**
```
# Safe to ignore — model still downloads correctly
# Or set HF_TOKEN in .env to suppress it
```

---

## 🛠️ Tech Stack

- [CrewAI](https://docs.crewai.com) — Multi-agent orchestration
- [ChromaDB](https://www.trychroma.com) — Vector store
- [Sentence Transformers](https://www.sbert.net) — Embeddings (`all-MiniLM-L6-v2`)
- [Groq](https://console.groq.com) — LLM inference (llama3-70b-8192)
- [LangChain Community](https://python.langchain.com) — Document loaders

---

## 📄 License
  
                      Apache License
                Version 2.0, January 2004
