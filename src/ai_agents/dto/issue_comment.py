from typing import List, Literal, Optional
from pydantic import BaseModel, model_validator


class IssueCommentDTO(BaseModel):
    type: Literal[
        "heading",
        "paragraph",
        "bulletList",
        "orderedList",
        "codeBlock"
    ]
    text: Optional[str] = None
    items: Optional[List[str]] = None
    code: Optional[str] = None
    language: Optional[str] = None

    @model_validator(mode="after")
    def validate_code_block(self) -> "IssueCommentDTO":
        if self.type == "codeBlock" and not self.code:
            raise ValueError('codeBlock blocks require the "code" field')

        return self
