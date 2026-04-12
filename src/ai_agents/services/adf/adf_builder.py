from typing import Any, Dict, List, Optional, Self


class ADFBuilder:
    def __init__(self):
        self.blocks = []

    def clear(self):
        self.blocks.clear()

    @staticmethod
    def _text_node(text: str) -> Dict:
        return {"type": "text", "text": text}

    @staticmethod
    def _paragraph_node(text: str) -> Dict:
        return {
            "type": "paragraph",
            "content": [ADFBuilder._text_node(text)]
        }

    def text(self, text: str) -> Self:
        self.blocks.append(self._text_node(text))
        return self

    def paragraph(self, text: str) -> Self:
        self.blocks.append(self._paragraph_node(text))
        return self

    def heading(
            self,
            text: str,
            level: int = 2
    ) -> Self:
        self.blocks.append({
            "type": "heading",
            "attrs": {"level": level},
            "content": [self._text_node(text)]
        })

        return self

    def bullet_list(self, items: List[str]) -> Self:
        self.blocks.append({
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [self._paragraph_node(item)]
                }
                for item in items
            ]
        })

        return self

    def ordered_list(self, items: List[str]) -> Self:
        self.blocks.append({
            "type": "orderedList",
            "content": [
                {
                    "type": "listItem",
                    "content": [self._paragraph_node(item)]
                }
                for item in items
            ]
        })

        return self

    def code_block(
            self,
            code: str,
            language: Optional[str] = None
    ) -> Self:
        block: Dict[str, Any] = {
            "type": "codeBlock",
            "content": [self._text_node(code)]
        }

        if language:
            block["attrs"] = {"language": language}

        self.blocks.append(block)
        return self

    def build(self) -> Dict:
        return {
            "type": "doc",
            "version": 1,
            "content": self.blocks
        }
