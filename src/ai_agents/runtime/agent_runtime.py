from dataclasses import dataclass
from typing import Any, Dict, List

from ai_agents.config import Config
from ai_agents.clients.jira_client import JiraClient
from ai_agents.dto.issue_comment import IssueCommentDTO
from ai_agents.services.issue_service import IssueService
from ai_agents.utils import Logger
from ai_agents.services.adf.adf_parser import ADFParser
from ai_agents.services.adf.adf_builder import ADFBuilder
from ai_agents.runtime.runtime_response import RuntimeResponse


class AgentRuntime:
    logger = Logger.get_logger(__name__)

    def __init__(self):
        Logger.setup()

        try:
            self.logger.info("Initializing AgentRuntime")

            Config.load_environments()
            Config.validate()

            self.issue_service = self._build_issue_service()

            self.logger.info("AgentRuntime initialized successfully")
        except Exception as e:
            self.logger.exception(
                f"Failed to initialize AgentRuntime {str(e)}")
            raise

    def _build_issue_service(self) -> IssueService:
        jira_client = JiraClient(
            base_url=Config.get("JIRA_BASE_URL"),
            email=Config.get("JIRA_EMAIL"),
            api_token=Config.get("JIRA_API_TOKEN")
        )

        return IssueService(
            jira_client,
            ADFParser(),
            ADFBuilder()
        )

    def get_jira_issue(self, issue_key: str) -> RuntimeResponse:
        self.logger.info(f"Fetching jira issue with key {issue_key}")

        try:
            return RuntimeResponse(
                status="OK",
                message=str(self.issue_service.get_issue(issue_key))
            )
        except Exception as e:
            error_msg = f"Error while fetching issue {
                issue_key}. Error: {str(e)}"
            self.logger.exception(error_msg)
            return RuntimeResponse(status="ERROR", message=error_msg)

    def write_jira_issue_comment(
            self,
            issue_key: str,
            comment_data: List[IssueCommentDTO]
    ) -> RuntimeResponse:
        self.logger.info(f"Writing comment in issue {issue_key}")

        try:
            result = self.issue_service.write_comment(issue_key, comment_data)
            return RuntimeResponse(status="OK", message=str(result))
        except Exception as e:
            error_msg = f"Error while writing comment in issue {
                issue_key}. Error: {str(e)}"
            self.logger.exception(error_msg)
            return RuntimeResponse(status="ERROR", message=error_msg)
