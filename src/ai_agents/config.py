import os
from typing import List
from dotenv import load_dotenv


class Config:
    @staticmethod
    def load_environments():
        load_dotenv()

    @staticmethod
    def get(key: str) -> str:
        value = os.getenv(key)

        if not value:
            raise ValueError(f"{key} não está definido no .env")

        return value

    @staticmethod
    def get_list(key: str) -> List[str]:
        value = Config.get(key)

        return value.split(" ")

    @classmethod
    def validate(cls):
        required_fields = [
            "JIRA_BASE_URL",
            "JIRA_EMAIL",
            "JIRA_API_TOKEN",
        ]

        missing = [
            field for field in required_fields
            if not os.getenv(field)
        ]

        if missing:
            raise ValueError(
                f"Variáveis de ambiente não definidas: {', '.join(missing)}"
            )
