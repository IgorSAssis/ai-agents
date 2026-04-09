from typing import List, Literal, Optional
from pydantic import BaseModel


class IssueCommentDTO(BaseModel):
    type: Literal["heading", "paragraph", "bulletList", "orderedList"]
    text: Optional[str] = None
    items: Optional[List[str]] = None
