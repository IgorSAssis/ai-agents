from typing import List


class IssueCommentDTO:
    def __init__(
        self,
        section: str,
        items: List[str]
    ):
        self.section = section
        self.items = items
