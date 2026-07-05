from __future__ import annotations

from datetime import date

from .models import RepoRecord


SEED_REPOS = [
    ("openai/openai-agents-python", "AI Agent", "Python", 18400, 2100, "SDK for building AI agents and tool workflows.", ["agent", "tools"]),
    ("modelcontextprotocol/servers", "MCP", "TypeScript", 24500, 3200, "Reference MCP servers for the Model Context Protocol.", ["mcp", "tools"]),
    ("run-llama/llama_index", "RAG", "Python", 46200, 6100, "Data framework for LLM applications and retrieval augmented generation.", ["rag", "llamaindex"]),
    ("vllm-project/vllm", "LLM Infrastructure", "Python", 55700, 9200, "High-throughput and memory-efficient inference engine for LLMs.", ["inference", "serving"]),
    ("openfoam/openfoam-dev", "Simulation", "C++", 8900, 2300, "Open source computational fluid dynamics simulation toolbox.", ["cfd", "simulation"]),
    ("ansys/pyansys", "Engineering AI", "Python", 1800, 420, "Pythonic engineering simulation automation across Ansys products.", ["cae", "engineering"]),
    ("browser-use/browser-use", "AI Agent", "Python", 38800, 4100, "Make websites accessible for AI agents.", ["browser-use", "agent"]),
    ("microsoft/autogen", "AI Agent", "Python", 49200, 7600, "Multi-agent conversation framework for AI applications.", ["multi-agent", "autogen"]),
    ("qdrant/qdrant", "RAG", "Rust", 28600, 1900, "Vector database for embeddings and semantic search.", ["vector-database", "embeddings"]),
    ("sgl-project/sglang", "LLM Infrastructure", "Python", 18900, 2400, "Fast serving framework for large language models.", ["llm", "serving"]),
    ("Kitware/ParaView", "Simulation", "C++", 2600, 1100, "Scientific visualization for simulation and engineering data.", ["simulation", "paraview"]),
    ("langchain-ai/langgraph", "AI Agent", "Python", 35200, 5600, "Build resilient language agents as graphs.", ["agent", "langgraph"]),
]


def make_dummy_records(snapshot_date: date | None = None) -> list[RepoRecord]:
    day = snapshot_date or date.today()
    records: list[RepoRecord] = []
    for idx, (full_name, category, language, stars, forks, desc, topics) in enumerate(SEED_REPOS):
        growth = max(6, int(stars * (0.01 + (idx % 5) * 0.004)))
        records.append(
            RepoRecord(
                snapshot_date=day.isoformat(),
                full_name=full_name,
                url=f"https://github.com/{full_name}",
                description=desc,
                language=language,
                stars=stars,
                forks=forks,
                open_issues=idx * 17,
                last_update=day.isoformat(),
                created_at="2024-01-01T00:00:00Z",
                pushed_at=f"{day.isoformat()}T08:00:00Z",
                author=full_name.split("/", 1)[0],
                category=category,
                matched_categories=[category],
                topics=topics,
                source="dummy",
                stars_gained_hint=growth,
                forks_gained_hint=max(1, growth // 8),
                source_notes=["Generated fallback data because live collection was unavailable."],
            )
        )
    return records
