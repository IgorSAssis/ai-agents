import requests
from typing import Any, Dict


class JiraClient:
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url
        self.auth = (email, api_token)

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        response = requests.get(url, auth=self.auth)

        if response.status_code != 200:
            raise Exception(
                f"Error while fetching issue data: {
                    response.status_code} - {response.text}"
            )

        return response.json()

    def write_comment(self, issue_key: str, body: Dict) -> Dict[str, Any]:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": body
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            json=payload,
            auth=self.auth,
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(
                f"Error while add comment in issue: {
                    response.status_code} - {response.text}"
            )

        return response.json()
