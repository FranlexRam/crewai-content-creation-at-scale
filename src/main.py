import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from src.models import ContentOutput
from src.tools import (
    analyst_llm,
    editorial_llm,
    duckduckgo_search_tool,
    scrape_tool,
    rag_website_search_tool
)

# ============================================================================
# 1. CARGA DE CONFIGURACIONES DECLARATIVAS (YAML)
# ============================================================================
current_dir = Path(__file__).parent.parent

with open(current_dir / "config" / "agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)

with open(current_dir / "config" / "tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

# ============================================================================
# 2. INSTANCIACIÓN DE AGENTES
# ============================================================================
market_monitor = Agent(
    config=agents_config["market_news_monitor_agent"],
    llm=analyst_llm,
    tools=[duckduckgo_search_tool]
)

data_analyst = Agent(
    config=agents_config["data_analyst_agent"],
    llm=analyst_llm,
    tools=[duckduckgo_search_tool, scrape_tool, rag_website_search_tool]
)

content_creator = Agent(
    config=agents_config["content_creator_agent"],
    llm=editorial_llm,
    tools=[duckduckgo_search_tool, scrape_tool]
)

qa_reviewer = Agent(
    config=agents_config["quality_assurance_agent"],
    llm=editorial_llm
    # El QA no necesita herramientas de búsqueda, solo lee el borrador y lo valida
)

# ============================================================================
# 3. INSTANCIACIÓN DE TAREAS
# ============================================================================
monitor_task = Task(
    config=tasks_config["monitor_financial_news"],
    agent=market_monitor
)

analyze_task = Task(
    config=tasks_config["analyze_market_data"],
    agent=data_analyst
)

create_task = Task(
    config=tasks_config["create_content"],
    agent=content_creator
)

qa_task = Task(
    config=tasks_config["quality_assurance"],
    agent=qa_reviewer,
    output_pydantic=ContentOutput  # <-- Aquí ocurre la magia del contrato estructurado
)

# ============================================================================
# 4. ENSAMBLAJE DE LA CUADRILLA Y EJECUCIÓN
# ============================================================================
content_crew = Crew(
    agents=[market_monitor, data_analyst, content_creator, qa_reviewer],
    tasks=[monitor_task, analyze_task, create_task, qa_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Iniciando la cuadrilla de creación de contenido...")
    
    # Un tema de prueba realista para evaluar la profundidad analítica y técnica de los agentes
    tema = "Impacto de los agentes autónomos de IA en el desarrollo de software B2B durante 2026"
    
    # Ejecución del pipeline inyectando el tema en los placeholders {subject} de los YAML
    resultado = content_crew.kickoff(inputs={"subject": tema})
    
    print("\n================================================")
    print("🎯 ARTÍCULO COMPLETO EN MARKDOWN:")
    print("================================================\n")
    
    # Extraemos el objeto Pydantic (ContentOutput) del resultado de la cuadrilla
    contenido = resultado.pydantic

    # 1. Imprimimos el artículo (ahora sí interpretará los \n como saltos de línea reales)
    print(contenido.article)

    print("\n\n" + "=" * 50)
    print("📱 COPYS PARA REDES SOCIALES")
    print("=" * 50)

    # 2. Iteramos la lista de publicaciones estructuradas
    for post in contenido.social_media_posts:
        print(f"\n📍 Plataforma: {post.platform}")
        print(f"📝 Copy:\n{post.content}")
        print("-" * 40)