# Grid07 AI Engineering Assignment
## Cognitive Routing & RAG System

This project was built as part of the AI Engineering Internship Assignment for Grid07 Development.

The assignment focuses on building the core AI cognitive loop for a social media bot platform using:

- Vector Embeddings
- Semantic Routing
- LangGraph Orchestration
- Retrieval-Augmented Generation (RAG)
- Prompt Injection Defense

---

# Tech Stack

- Python
- LangChain
- LangGraph
- ChromaDB
- Sentence Transformers
- Groq API
- dotenv

---

# Project Structure

```bash
grid07-assignment/
│
├── phase1_router.py
├── phase2_langgraph.py
├── phase3_rag_defense.py
├── requirements.txt
├── .env.example
├── execution_logs.md
└── README.md

Setup Instructions

    Step 1: Clone Repository

        git clone https://github.com/yourusername/grid07-ai-assignment.git
        cd grid07-ai-assignment

    Step 2: Install Dependencies

        pip install -r requirements.txt

    Step 3: Add API Key

        Create a .env file:
            GROQ_API_KEY=your_actual_api_key

Phase 1: Vector-Based Persona Matching
Objective

The goal of this phase is to route posts only to bots that are semantically relevant to the content.

Instead of broadcasting every post to every bot:

Post gets embedded
Bot personas get embedded
Cosine similarity is calculated
Only relevant bots are selected
Bot Personas
Bot A → Tech Maximalist

Believes:

AI solves everything
Crypto solves everything
Elon Musk
Space exploration
Technology optimism
Bot B → Doomer/Skeptic

Believes:

Tech monopolies are harmful
Billionaires are harmful
Privacy matters
Nature matters
Bot C → Finance Bro

Believes:

ROI matters
Markets matter
Trading matters
Interest rates matter


Workflow

    User Post
        ↓
    Generate Embedding
        ↓
    Compare With Bot Persona Embeddings
        ↓
    Cosine Similarity
        ↓
    Return Matching Bots


Phase 2: Autonomous Content Engine (LangGraph)
Objective

Generate autonomous social media posts using:

Persona
Topic selection
Web search context
Opinion generation

LangGraph Workflow

START
 ↓
Decide Search Topic
 ↓
Web Search Tool
 ↓
Draft Post
 ↓
END

Node 1: Decide Search

The bot decides what topic it wants to post about based on its persona.

Example:

AI
Crypto
Elon Musk
Markets

Node 2: Web Search

This returns hardcoded recent headlines.

Node 3: Draft Post

The LLM combines:

Persona
Topic
Search results

Then generates:

highly opinionated post
under 280 characters
strict JSON output

Phase 3: Deep Thread RAG + Prompt Injection Defense
Objective

Allow bots to understand full thread context before replying.

The bot receives:

Parent post
Previous comments
Human reply

Future Improvements
Replace mock search with real web search API
Store thread memory in vector database
Add multi-agent debate simulation
Add real-time post scheduling

Conclusion

This project demonstrates:

Semantic routing
Vector databases
LangGraph workflows
RAG implementation
Prompt security

These systems simulate how autonomous AI agents can operate safely in real-world social media environments.

