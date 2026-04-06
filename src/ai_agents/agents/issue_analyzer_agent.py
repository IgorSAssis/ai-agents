from typing import List
from ai_agents.models.issue import Issue
from ai_agents.services.issue_service import IssueService
from ai_agents.clients.llm import BaseClient
from ai_agents.utils.prompt_loader import PromptLoader


class IssueAnalyzerAgent:
    def __init__(
        self,
        issue_service: IssueService,
        llm_client: BaseClient,
        prompt_loader: PromptLoader
    ):
        self.issue_service = issue_service
        self.llm_client = llm_client
        self.prompt_loader = prompt_loader

    def run(self, issue_key: str) -> str:
        issue = self.issue_service.get_issue(issue_key)
        prompt = self.build_prompt(issue)

        return self.llm_client.generate(prompt)

    def build_prompt(self, issue: Issue) -> str:
        template = self.prompt_loader.load("issue_analysis.md")

        return template.format(
            summary=issue.summary,
            description=issue.description or "Sem descrição",
            comments=self._format_comments(issue.comments)
        )

    def _format_comments(self, comments: List[str]) -> str:
        if not comments:
            return "Sem comentários"

        return "\n".join(f"- {comment}" for comment in comments)
