from abc import ABC, abstractmethod


class BaseClient(ABC):
    DEFAULT_TIMEOUT: int = 360

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
