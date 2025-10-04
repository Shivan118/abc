from __future__ import annotations

from typing import Optional

from .config import AppConfig

try:
    from crewai import Agent, Task, Crew, Process  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError("CrewAI is required. Please install 'crewai'.") from e


def _create_llm_kwargs(config: AppConfig) -> dict:
    # CrewAI can use LiteLLM-style provider env via string model name.
    # We pass model name and rely on env keys (e.g., OPENAI_API_KEY)
    return {
        "llm": config.llm.model,
        "verbose": config.verbose,
    }


def build_agent(config: AppConfig) -> Agent:
    llm_kwargs = _create_llm_kwargs(config)
    return Agent(
        role="Helpful Voice Assistant",
        goal=(
            "Understand the user's intent and provide concise, accurate answers. "
            "When helpful, ask a brief follow-up question."
        ),
        backstory=(
            "You are a calm, friendly AI assistant speaking with a user through voice. "
            "Prefer clear, natural language and short answers."
        ),
        **llm_kwargs,
    )


def build_task(user_input: str, agent: Agent) -> Task:
    return Task(
        description=(
            f"Listen to the user's message and respond. Message: '{user_input}'. "
            "Keep the response under 80 words."
        ),
        expected_output="A concise, friendly spoken response.",
        agent=agent,
    )


def run_agent(user_input: str, config: Optional[AppConfig] = None) -> str:
    cfg = config or AppConfig()
    assistant = build_agent(cfg)
    task = build_task(user_input, assistant)
    crew = Crew(agents=[assistant], tasks=[task], process=Process.sequential)
    result = crew.kickoff()
    # CrewAI returns an object or string depending on version; ensure string
    return str(result)
