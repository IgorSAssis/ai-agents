from typing import List
from fastmcp import FastMCP

from ai_agents.runtime.agent_runtime import AgentRuntime
from ai_agents.dto.issue_comment import IssueCommentDTO

runtime = AgentRuntime()
mcp = FastMCP("AI-Agents")


@mcp.tool()
def get_jira_issue(issue_key: str) -> str:
    """
    Fetches a Jira issue by its key (e.g., PROJ-123).
    """
    return runtime.get_jira_issue(issue_key)


@mcp.tool()
def add_issue_comment(issue_key: str, comment_data: List[IssueCommentDTO]) -> str:
    """
    Add a comment in a jira issue.

    Args:
        issue_key: issue key (e.g., PROJ-123)
        comment_data: comment's text. Example:
        [
            { "section":  ff }
        ]

    Return:
        Dict with operation status
    """
    result = runtime.write_jira_issue_comment(issue_key, comment)

    return str(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")
