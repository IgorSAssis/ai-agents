from typing import Dict, List, Self


class ADFBuilder:
    def __init__(self):
        self.blocks = []

    def clear(self):
        self.blocks.clear()

    def text(self, text: str) -> Self:
        self.blocks.append({"type": "text", "text": text})

        return self

    def paragraph(self, text: str) -> Self:
        self.blocks.append({
            "type": "paragraph",
            "content": [ADFBuilder.text(text)]
        })

        return self

    def heading(
            self,
            text: str,
            level: int = 2
    ) -> Self:
        self.blocks.append({
            "type": "heading",
            "attrs": {"level": level},
            "content": [ADFBuilder.text(text)]
        })

        return self

    def bullet_list(self, items: List[str]) -> Self:
        self.blocks.append({
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [ADFBuilder.paragraph(item)]
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
                    "content": [ADFBuilder.paragraph(item)]
                }
                for item in items
            ]
        })

        return self

    def build(self) -> Dict:
        return {
            "type": "doc",
            "version": 1,
            "content": self.blocks
        }
