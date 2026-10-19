# CrewAI: Production-Grade Multi-Agent Content Engine at Scale

A modular, production-ready multi-agent pipeline built with **CrewAI**, **OpenRouter**, and **Pydantic** to automate deep-dive market research, quantitative analysis, long-form editorial reporting, and omnichannel social media content generation.

---

## 🏗️ Architecture Overview

The system implements a **multi-model orchestration pattern** designed for cost efficiency, speed, and strict schema compliance:

[ DuckDuckGo Search / Scraper ]
│
▼
┌──────────────────────┐
│ Lead Market Analyst  │ ── LLM: Llama 3.3 70B Instruct (Fast ingestion & filtering)
└──────────────────────┘
│
▼
┌──────────────────────┐
│ Chief Data Strategist│ ── LLM: Llama 3.3 70B Instruct (Quantitative synthesis & metrics)
└──────────────────────┘
│
▼
┌────────────────────────┐
│ Creative Content Lead  │ ── LLM: DeepSeek V4.1 Flash (Long-form narrative & copy)
└────────────────────────┘
│
▼
┌────────────────────────┐
│ Chief Content Officer  │ ── LLM: DeepSeek V4.1 Flash + Pydantic Schema Validation
└────────────────────────┘
│
▼
[ ContentOutput (JSON) ]
├── article (Markdown)
└── social_media_posts (Platform-specific list)

### Key Technical Decisions
* **Multi-Model Routing:** Tasks requiring heavy token processing utilize Meta's `llama-3.3-70b-instruct`, while editorial generation and schema enforcement run on `deepseek-v4.1-flash`, slashing inference costs to fractions of a cent per run.
* **Strict Data Contracts:** Outputs are enforced via Pydantic v2 schemas (`ContentOutput`), guaranteeing structured payloads ready for database insertion or REST API consumers.
* **Declarative Configuration:** Agent personas, backstories, task descriptions, and expected outcomes are decoupled into YAML configuration files.

---

## 📁 Repository Structure

```text
├── config/
│   ├── agents.yaml       # Agent personas, goals, and backstories
│   └── tasks.yaml        # Task definitions, requirements, and assignments
├── src/
│   ├── __init__.py
│   ├── main.py           # Orchestration entry point and Crew kickoff
│   ├── models.py         # Pydantic structured output models
│   └── tools.py          # LLM instances and external tool configurations
├── .env.example          # Environment variable template
├── .gitignore
├── requirements.txt      # Production dependencies
└── README.md

🚀 Quickstart
1. Prerequisites
Python 3.11+

OpenRouter API Key

2. Installation
Clone the repository and set up a virtual environment:

git clone <your-repo-url>
cd crewai-content-creation-at-scale
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Environment Setup
Copy the example environment file and add your credentials:

cp .env.example .env

Ensure .env contains:

OPENROUTER_API_KEY="your-openrouter-key-here"
OPENROUTER_BASE_URL="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)"


4. Run the Pipeline
Execute the crew using the module flag:

python -m src.main

📊 Structured Output Schema
The pipeline returns a validated ContentOutput model:

class SocialMediaPost(BaseModel):
    platform: str
    content: str

class ContentOutput(BaseModel):
    article: str
    social_media_posts: List[SocialMediaPost]


🛠️ Tech Stack
Orchestration: CrewAI

LLM Gateway: OpenRouter

Models: Meta Llama 3.3 70B & DeepSeek V4.1 Flash

Validation: Pydantic v2

Tools: DuckDuckGo Search (ddgs), ScrapeWebsiteTool, Sentence Transformers (Local Embeddings)

