from typing import List, Optional
from pydantic import BaseModel


class Issue(BaseModel):
    key: str
    summary: str
    description: Optional[str] = None
    comments: List[str] = []

    def __str__(self) -> str:
        return (
            f"Issue (key={self.key}, "
            f"summary={self.summary}, "
            f"description={self.description}, "
            f"comments={self.comments})"
        )
