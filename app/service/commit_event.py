from typing import Any

from flask import current_app

from app.config import MAIN_BRANCH, REPO_NAMES
from app.utils import github_to_tg


def process_commit_event(data: Any) -> tuple[str, int]:
    if data.get("commits") and data.get("ref") == f"refs/heads/{MAIN_BRANCH}":
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]

        project_name = REPO_NAMES.get(repo, repo)
        repo_part = f"{project_name}" if project_name != repo else f"{repo}"

        for commit in data["commits"]:
            commit_title = commit["message"].split("\n", 1)[0]
            commit_text = f"- [{commit_title}]({commit['url']})"

        text = (
            f"🚀 Новый коммит в репозитории проекта *{repo_part}*!\n"
            f"👤 *Автор:* [{pusher}](tg://user?id={github_to_tg(pusher)})\n"
            f"📝 *Изменения:*\n{commit_text}\n"
            f"🔗 [Открыть репозиторий]({data['repository']['html_url']})"
        )

        current_app.telegram_repo.send_message(  # type: ignore[attr-defined]
            text
        )
        return "Commit event processed", 200

    return "Ignored", 200
