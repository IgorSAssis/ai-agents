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
    return str(runtime.get_jira_issue(issue_key))


@mcp.tool()
def add_issue_comment(
        issue_key: str,
        comment_data: List[IssueCommentDTO]
) -> str:
    """
    Add a comment in a jira issue.

    The comment is composed of a list of blocks. Each block has a "type" and
    the corresponding content field (
        "text" for heading/paragraph, "items" for lists,
        "code" for code blocks
    ).

    Supported block types:
      - "heading"      → section title (uses "text")
      - "paragraph"    → plain text paragraph (uses "text")
      - "bulletList"   → unordered list (uses "items")
      - "orderedList"  → numbered list (uses "items")
      - "codeBlock"    → code snippet (uses "code", optional "language")

    Args:
        issue_key: issue key (e.g., PROJ-123)
        comment_data: list of content blocks. Full example with all types:
        [
            { "type": "heading",     "text": "Analysis Summary" },
            { "type": "paragraph",   "text": "The analysis was completed successfully." },
            { "type": "bulletList",  "items": ["Finding A", "Finding B", "Finding C"] },
            { "type": "orderedList", "items": ["Step 1: Review", "Step 2: Approve", "Step 3: Deploy"] },
            { "type": "codeBlock",   "code": "print('hello world')", "language": "python" }
        ]

    Returns:
        Dict with the created comment data returned by Jira.
    """
    return str(runtime.write_jira_issue_comment(issue_key, comment_data))


if __name__ == "__main__":
    mcp.run(transport="stdio")
