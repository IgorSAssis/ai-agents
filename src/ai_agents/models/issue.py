from typing import List, Optional


class Issue:
    def __init__(
        self,
        key: str,
        summary: str,
        description: Optional[str],
        comments: List[str],
    ):
        self.key = key
        self.summary = summary
        self.description = description
        self.comments = comments

    def __str__(self):
        return (
            f"Issue (key={self.key}, "
            f"summary={self.summary}, "
            f"description={self.description}, "
            f"comments={self.comments})"
        )
