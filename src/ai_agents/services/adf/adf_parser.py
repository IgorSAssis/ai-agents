from typing import Dict, List, Any, Optional


class ADFParser:
    def extract_description(
            self,
            description_field: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        if not description_field:
            return None

        try:
            texts: List[str] = []

            self._process_node(description_field, texts)

            return "\n".join(texts)
        except Exception:
            return None

    def extract_comments(
            self,
            comment_field: Dict[str, Any]
    ) -> List[str]:
        comments: List[str] = []

        for comment in comment_field.get("comments", []):
            author_name: str = comment.get("author", {}).get("displayName")
            content = comment.get("body", {}).get("content")
            text = self.extract_description(content)

            if text:
                prefix = f"{author_name}: " if author_name else ""
                comments.append(f"{prefix}{text}")

        return comments

    def _process_node(
            self,
            node: Any,
            texts: List[str],
            prefix: str = ""
    ):
        if isinstance(node, list):
            for item in node:
                self._process_node(item, texts, prefix)
            return

        if not isinstance(node, dict):
            return

        node_type = node.get("type")
        handler = self._get_handler(node_type)
        handler(node, texts, prefix)

    def _get_handler(self, node_type: str):
        handlers = {
            "orderedList": self._handle_ordered_list,
            "bulletList": self._handle_bullet_list,
            "listItem": self._handle_list_item,
            "paragraph": self._handle_paragraph,
            "text": self._handle_text,
        }

        return handlers.get(node_type, self._handle_default)

    def _handle_ordered_list(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        for index, item in enumerate(node.get("content", []), start=1):
            self._process_node(item, texts, prefix=f"{index}. ")

    def _handle_bullet_list(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        for item in node.get("content", []):
            self._process_node(item, texts, prefix="- ")

    def _handle_list_item(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        item_texts: List[str] = []

        for child in node.get("content", []):
            self._process_node(child, item_texts, "")

        line = "".join(item_texts).strip()

        if line:
            texts.append(prefix + line)

    def _handle_paragraph(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        for child in node.get("content", []):
            self._process_node(child, texts, prefix)

    def _handle_text(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        text = node.get("text")

        if text:
            texts.append(prefix + text)

    def _handle_default(
            self,
            node: Any,
            texts: List[str],
            prefix: str
    ) -> None:
        if "content" in node:
            self._process_node(node["content"], texts, prefix)
