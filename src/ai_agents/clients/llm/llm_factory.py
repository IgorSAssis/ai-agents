from typing import Callable, Dict

from ai_agents.config import Config
from ai_agents.clients.llm.base_client import BaseClient
from ai_agents.clients.llm.ollama_client import OllamaClient
from ai_agents.clients.llm.cli_client import CLIClient


class LLMFactory:
    _providers: Dict[str, Callable[[], BaseClient]] = {}

    @classmethod
    def create(cls, provider: str) -> BaseClient:
        handler = cls._providers.get(provider)

        if not provider:
            raise ValueError(f"Provider inválido: {provider}")

        return handler()

    @classmethod
    def register(
        cls,
        provider: str,
        handler: Callable[[], BaseClient]
    ) -> None:
        cls._providers[provider] = handler

# ------------ Providers ------------


def create_ollama() -> OllamaClient:
    return OllamaClient(
        model=Config.get("OLLAMA_MODEL"),
        base_url=Config.get("OLLAMA_BASE_URL")
    )


def create_claude() -> CLIClient:
    return CLIClient(
        command=Config.get_list("CLAUDE_CMD")
    )


def create_copilot() -> CLIClient:
    return CLIClient(
        command=Config.get_list("COPILOT_CMD")
    )


# ------------ Register providers ------------
LLMFactory.register("ollama", create_ollama)
LLMFactory.register("claude", create_claude)
LLMFactory.register("copilot", create_copilot)
