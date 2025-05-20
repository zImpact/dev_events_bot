from jira import JIRA, JIRAError

from app.config import JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_LOGIN_EMAIL


class JiraRepository:
    def __init__(self):
        self.jira_client = JIRA(
            server=JIRA_BASE_URL, basic_auth=(JIRA_LOGIN_EMAIL, JIRA_API_TOKEN)
        )

    def get_issue_title(self, key: str) -> str:
        try:
            issue = self.jira_client.issue(key, fields="summary")
            return issue.fields.summary
        except JIRAError as e:
            if e.status_code == 404:
                return None
            raise

    def get_issue_statuses(self, key: str) -> list[dict]:
        return self.jira_client.transitions(key)

    def move_issue_to_status(self, key: str, status_name: str) -> None:
        statuses = self.get_issue_statuses(key)
        st = next((st for st in statuses if st["name"] == status_name), None)
        self.jira_client.transition_issue(key, st["id"])

    def assign_reviewers(self, key: str, field_id: int, ids: list[int]):
        self.jira_client.issue(key).update(
            fields={
                f"customfield_{field_id}": [{"accountId": id} for id in ids]
            }
        )
