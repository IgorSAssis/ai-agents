import requests
from .base_client import BaseClient


class OllamaClient(BaseClient):
    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=self.DEFAULT_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()
            print("Printing response...")
            print(data)

            return data.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Cannot call ollama: {e}")
