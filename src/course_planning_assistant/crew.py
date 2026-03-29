from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
import chromadb
from sentence_transformers import SentenceTransformer
from pydantic import Field

# ── RAG Tool ─────────────────────────────────────────────────
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    collection = chroma_client.get_collection("course_catalog")
except:
    collection = chroma_client.create_collection("course_catalog")

class CatalogSearchTool(BaseTool):
    name: str = "Catalog Search Tool"
    description: str = "Search the course catalog for prerequisites, program requirements, and academic policies. Always returns results with source URLs and chunk IDs."

    def _run(self, query: str) -> str:
        query_embedding = embedding_model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        if not results["documents"][0]:
            return "NOT FOUND IN CATALOG: No relevant information found."

        formatted = []
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            formatted.append(f"""
--- Result {i+1} ---
Chunk ID:   {meta.get('chunk_id', 'N/A')}
Source:     {meta.get('source_url', 'N/A')}
Section:    {meta.get('section', 'N/A')}
Relevance:  {round((1 - dist) * 100, 1)}%
Content:    {doc}
""")
        return "\n".join(formatted)

# ── Crew ─────────────────────────────────────────────────────
@CrewBase
class CoursePlanningAssistant():
    """Course Planning Assistant Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config  = 'config/tasks.yaml'

    @agent
    def intake_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intake_agent'],
            verbose=True
        )

    @agent
    def catalog_retriever_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['catalog_retriever_agent'],
            tools=[CatalogSearchTool()],
            verbose=True
        )

    @agent
    def planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['planner_agent'],
            verbose=True
        )

    @agent
    def verifier_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['verifier_agent'],
            verbose=True
        )

    @task
    def intake_task(self) -> Task:
        return Task(config=self.tasks_config['intake_task'])

    @task
    def retrieval_task(self) -> Task:
        return Task(config=self.tasks_config['retrieval_task'])

    @task
    def planning_task(self) -> Task:
        return Task(config=self.tasks_config['planning_task'])

    @task
    def verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['verification_task'],
            output_file='output/final_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )