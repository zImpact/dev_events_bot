from typing import Any

from app.config import MAIN_BRANCH
from flask import current_app

from app.models import JiraColumn


def process_pull_request_merged_event(data: Any) -> tuple[str, int]:
    if data.get("action") == "closed" and data.get("pull_request", {}).get(
        "merged"
    ):
        pull_request = data["pull_request"]
        pr_branch = pull_request["head"]["ref"]
        target_branch = pull_request["base"]["ref"]

        if target_branch != MAIN_BRANCH:
            return f"Ignored: merged into {target_branch}", 200

        current_app.jira_repo.move_issue_to_status(
            pr_branch, JiraColumn.DONE.value
        )

        return "Pull request merged event processed", 200

    return "Ignored", 200
