import os
from dotenv import load_dotenv
from crewai import LLM
from crewai.tools import tool
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from duckduckgo_search import DDGS

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not OPENROUTER_API_KEY:
    raise ValueError("Falta la variable OPENROUTER_API_KEY en tu archivo .env")

# ============================================================================
# HACK: BYPASS DEL VALIDADOR DE CREWAI
# Engañamos al validador inyectando una llave falsa para que no bloquee la ejecución.
# Como usamos nuestro propio 'config' abajo, esta llave jamás se utilizará.
# ============================================================================
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-para-burlar-el-validador-de-crewai"

# ============================================================================
# 1. ARQUITECTURA BI-MODELO CON OPENROUTER (ULTRA ECONÓMICA)
# ============================================================================

analyst_llm = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    temperature=0.1
)

editorial_llm = LLM(
    model="openrouter/deepseek/deepseek-v4.1-flash",
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    temperature=0.4
)

# ============================================================================
# 2. HERRAMIENTAS WEB (DUCKDUCKGO, SCRAPER Y RAG)
# ============================================================================

@tool("DuckDuckGo Web Search")
def duckduckgo_search_tool(query: str) -> str:
    """Busca en la web información reciente, artículos y noticias en tiempo real."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return "No se encontraron resultados para la consulta."
            
            formatted_results = []
            for item in results:
                title = item.get("title", "")
                link = item.get("href", "")
                body = item.get("body", "")
                formatted_results.append(f"Título: {title}\nURL: {link}\nResumen: {body}")
            
            return "\n\n---\n\n".join(formatted_results)
    except Exception as e:
        return f"Error al ejecutar búsqueda en DuckDuckGo: {str(e)}"

scrape_tool = ScrapeWebsiteTool()

# RAG dinámico sobre páginas web con ChromaDB y embeddings locales
rag_website_search_tool = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="openai",
            config=dict(
                model="meta-llama/llama-3.3-70b-instruct",
                api_base=OPENROUTER_BASE_URL,
                api_key=OPENROUTER_API_KEY,
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2"
            ),
        ),
    )
)