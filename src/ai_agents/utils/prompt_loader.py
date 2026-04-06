from pathlib import Path


class PromptLoader:
    def __init__(
            self,
            base_path: str = "prompts"
    ):
        project_root = Path(__file__).resolve().parent.parent
        self.base_path = project_root / base_path

    def load(self, filename: str) -> str:
        file_path = self.base_path / filename

        if not file_path.exists() or not file_path.is_file():
            error_msg = f"Prompt file not found or is not a file: {file_path}"
            raise FileNotFoundError(error_msg)

        return file_path.read_text(encoding="utf-8")
