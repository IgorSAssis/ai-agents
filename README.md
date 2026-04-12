# ai-agents

Small MCP server for Jira automation. It exposes tools for reading Jira issues and posting structured Jira comments using Atlassian Document Format (ADF).

## What this project does

This project starts a FastMCP server that connects to Jira with credentials loaded from a `.env` file. Today it exposes two tools:

| Tool | Purpose |
| --- | --- |
| `get_jira_issue` | Fetch a Jira issue by key and return its summary, description, and comments. |
| `add_issue_comment` | Add a structured Jira comment composed of headings, paragraphs, lists, and code blocks. |

## Requirements

- Python 3.12+
- A Jira Cloud account
- A Jira API token
- `uv` recommended for installing and running the project

## Installation

```bash
uv sync
```

## Environment configuration

Create a `.env` file in the project root:

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your_jira_api_token
```

### Variables

| Variable | Purpose |
| --- | --- |
| `JIRA_BASE_URL` | Base URL of your Jira instance. |
| `JIRA_EMAIL` | Jira account email used for authentication. |
| `JIRA_API_TOKEN` | Jira API token used for authenticated requests. |

The runtime validates these variables on startup and fails fast if any of them are missing.

## How to run

Start the MCP server with:

```bash
uv run python -m ai_agents.main
```

## Tool reference

### `get_jira_issue`

Fetches a Jira issue by key.

**Arguments**

| Name | Type | Description |
| --- | --- | --- |
| `issue_key` | `str` | Jira issue key such as `SCRUM-1`. |

**Example**

```json
{
  "issue_key": "SCRUM-1"
}
```

### `add_issue_comment`

Adds a Jira comment using structured blocks. Each block has a `type` and the corresponding content field.

**Supported block types**

| Type | Fields | Purpose |
| --- | --- | --- |
| `heading` | `text` | Section title. |
| `paragraph` | `text` | Plain text paragraph. |
| `bulletList` | `items` | Unordered list. |
| `orderedList` | `items` | Numbered list. |
| `codeBlock` | `code`, optional `language` | Code snippet rendered as a Jira code block. |

**Arguments**

| Name | Type | Description |
| --- | --- | --- |
| `issue_key` | `str` | Jira issue key such as `SCRUM-1`. |
| `comment_data` | `list[IssueCommentDTO]` | Ordered list of comment blocks. |

## Usage examples

### Add a simple text comment

```json
{
  "issue_key": "SCRUM-1",
  "comment_data": [
    { "type": "heading", "text": "Status update" },
    { "type": "paragraph", "text": "The deployment completed successfully." },
    { "type": "bulletList", "items": ["API healthy", "Database migrated"] }
  ]
}
```

### Add a comment with a code block

```json
{
  "issue_key": "SCRUM-1",
  "comment_data": [
    { "type": "heading", "text": "Validation output" },
    { "type": "paragraph", "text": "Testing the new code block support." },
    { "type": "codeBlock", "code": "print('hello world')", "language": "python" }
  ]
}
```

### Add a comment with ordered steps and shell code

```json
{
  "issue_key": "SCRUM-1",
  "comment_data": [
    { "type": "heading", "text": "Deployment steps" },
    { "type": "orderedList", "items": ["Build image", "Push image", "Restart service"] },
    { "type": "codeBlock", "code": "docker compose up -d --build", "language": "bash" }
  ]
}
```

## Implementation notes

- Comments are converted to Jira ADF before being sent to the Jira REST API.
- `codeBlock` support accepts raw code in `code` and optional syntax metadata in `language`.
- The project uses `python-dotenv` to load local environment variables.
