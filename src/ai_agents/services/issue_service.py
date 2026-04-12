from typing import Any, Dict, List
from ai_agents.models.issue import Issue
from ai_agents.clients.jira_client import JiraClient
from ai_agents.dto.issue_comment import IssueCommentDTO
from ai_agents.services.adf.adf_parser import ADFParser
from ai_agents.services.adf.adf_builder import ADFBuilder


class IssueService:
    def __init__(
            self,
            jira_client: JiraClient,
            parser: ADFParser,
            builder: ADFBuilder
    ):
        self.jira_client = jira_client
        self.parser = parser
        self.builder = builder

    def get_issue(self, issue_key: str) -> Issue:
        raw_issue_data = self.jira_client.get_issue(issue_key)

        return self._extract_issue_data(raw_issue_data)

    def write_comment(
            self,
            issue_key: str,
            comment_data: List[IssueCommentDTO]
    ) -> Dict[str, Any]:
        self.builder.clear()

        for block in comment_data:
            self._get_block_handler(block.type)(block)

        adf_body = self.builder.build()
        return self.jira_client.write_comment(issue_key, adf_body)

    def _get_block_handler(self, block_type: str):
        handlers = {
            "heading": lambda b:
                self.builder.heading(b.text) if b.text else None,
            "paragraph": lambda b:
                self.builder.paragraph(b.text) if b.text else None,
            "bulletList": lambda b:
                self.builder.bullet_list(b.items) if b.items else None,
            "orderedList": lambda b:
                self.builder.ordered_list(b.items) if b.items else None,
            "codeBlock": lambda b:
                self.builder.code_block(b.code, b.language) if b.code else None,
        }
        return handlers.get(block_type, lambda b: None)

    def _extract_issue_data(self, raw_issue_data: Dict[str, Any]) -> Issue:
        fields: Dict[str, Any] = raw_issue_data.get("fields", {})
        summary: str | None = fields.get("summary")
        description = self.parser.extract_description(
            fields.get("description"))
        comments = self.parser.extract_comments(fields.get("comment", {}))

        return Issue(
            key=raw_issue_data.get("key"),
            summary=summary or "",
            description=description,
            comments=comments
        )
