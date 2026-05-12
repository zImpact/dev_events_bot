from typing import Any

from flask import current_app

from app.config import REPO_NAMES
from app.utils import github_to_tg


def process_review_requested_event(data: Any) -> tuple[str, int]:
    if data.get("action") == "review_requested":
        repo = data["repository"]["name"]
        pull_request = data["pull_request"]
        assignee = data["sender"]["login"]

        reviewers = pull_request["requested_reviewers"]
        reviewers_mentions = ", ".join(
            f"[{r['login']}](tg://user?id={github_to_tg(r['login'])})"
            for r in reviewers
        )

        assignee_mention = f"tg://user?id={github_to_tg(assignee)}"

        if len(reviewers) == 1:
            reviewers_label = "Ревьювер:"
            title_label = "Назначен ревьювер"
        else:
            reviewers_label = "Ревьюверы:"
            title_label = "Назначены ревьюверы"

        project_name = REPO_NAMES.get(repo, repo)
        repo_part = project_name if project_name != repo else repo

        lines = [
            f"👀 {title_label} Pull Request-a в проекте *{repo_part}*!",
            f"👤 *Исполнитель:* [{assignee}]({assignee_mention})",
            f"🔍 *{reviewers_label}* {reviewers_mentions}",
            f"🔗 [Pull Request]({pull_request['html_url']})",
        ]

        text = "\n".join(lines)
        current_app.telegram_repo.send_message(  # type: ignore[attr-defined]
            text
        )
        return "Review request event processed", 200

    return "Ignored", 200
