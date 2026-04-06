import subprocess
from typing import Dict
from .base_client import BaseClient


class CLIClient(BaseClient):
    def __init__(
            self,
            command: Dict[str, str]
    ):
        self.command = command

    def generate(self, prompt: str) -> str:
        self._validate()

        try:
            full_cmd = self.command + [prompt]
            process = subprocess.run(
                full_cmd,
                text=True,
                capture_output=True,
                timeout=self.DEFAULT_TIMEOUT
            )

            if process.returncode != 0:
                raise RuntimeError(process.stderr.strip())

            return process.stdout.strip()
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout ao executar CLI LLM")
        except Exception as e:
            raise RuntimeError(f"Erro ao executar CLI LLM: {e}")

    def _validate(self):
        if not self.command:
            raise ValueError("O comando não pode ser vazio")
