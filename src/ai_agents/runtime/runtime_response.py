from dataclasses import dataclass


@dataclass
class RuntimeResponse:
    status: str
    message: str

    def __str__(self) -> str:
        return f"status={self.status}\nmessage={self.message}"
