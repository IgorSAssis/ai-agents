from typing import Dict, Any

from ai_agents.config import Config
from ai_agents.clients.jira_client import JiraClient
from ai_agents.services.issue_service import IssueService
from ai_agents.utils import Logger
from ai_agents.services.adf.adf_parser import ADFParser
from ai_agents.services.adf.adf_builder import ADFBuilder


class AgentRuntime:
    logger = Logger.get_logger(__name__)

    def __init__(self):
        self._initialize()

    def _initialize(self):
        Logger.setup()

        try:
            self.logger.info("Initializing AgentRuntime")

            Config.load_environments()
            Config.validate()

            self.jira_client = JiraClient(
                base_url=Config.get("JIRA_BASE_URL"),
                email=Config.get("JIRA_EMAIL"),
                api_token=Config.get("JIRA_API_TOKEN")
            )

            self.issue_service = IssueService(
                self.jira_client,
                ADFParser(),
                ADFBuilder()
            )

            self.logger.info("AgentRuntime initialized successfully")
        except Exception as e:
            self.logger.exception(
                f"Failed to initialize AgentRuntime {str(e)}")
            raise

    def get_jira_issue(self, issue_key: str) -> str:
        self.logger.info(f"Fetching jira issue with key {issue_key}")

        try:
            return self.issue_service.get_issue(issue_key)
        except Exception as e:
            error_msg = f"Error while fetching issue {
                issue_key}. Error: {str(e)}"
            self.logger.exception(error_msg)
            return error_msg

    def write_jira_issue_comment(
            self,
            issue_key: str,
            comment: str
    ) -> Dict[str, str]:
        self.logger.info(f"Writting comment in issue {issue_key}")

        try:
            return self.issue_service.write_comment(issue_key, comment)
        except Exception as e:
            error_result = {
                "status": "ERROR",
                "message": f"Error while writting comment in issue {
                    issue_key}. Error: {str(e)}"
            }
            self.logger.exception(error_result.message)
            return error_result
