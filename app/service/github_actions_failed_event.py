from typing import Any

from flask import current_app

from app.config import REPO_NAMES
from app.utils import escape_markdown, github_to_tg


def process_github_actions_failed_event(data: Any) -> tuple[str, int]:
    if data.get("action") == "completed" and "workflow_job" in data:
        repo = data["repository"]["name"]
        job = data["workflow_job"]
        job_name = job["name"]
        conclusion = job["conclusion"]
        workflow_url = job["html_url"]
        branch_name = job["head_branch"]
        commit_sha = job["head_sha"]
        sender = data["sender"]["login"]
        project_name = REPO_NAMES.get(repo, repo)
        sender_mention = f"tg://user?id={github_to_tg(sender)}"

        if conclusion == "failure":
            lines = [
                "🚨 *Ошибка в GitHub Actions!* 🚨",
                f"🔧 *Проект:* {escape_markdown(project_name)}",
            ]

            if branch_name == "main":
                lines.append("🏷️ *Ветка:* `main`")
            else:
                pr_url = current_app.github_repo.get_first_pr_url(  # type: ignore[attr-defined] # noqa: E501
                    repo, commit_sha
                )
                pr_number = pr_url.rstrip("/").split("/")[-1]
                lines.append(f"🔀 *Pull Request:* [#{pr_number}]({pr_url})")

            lines.extend(
                [
                    f"⚠️ *Проблемная джоба:* `{job_name}`",
                    f"👤 *Запустил:* [{sender}]({sender_mention})",
                    f"🔗 [Открыть Workflow]({workflow_url})",
                ]
            )

            text = "\n".join(lines)
            current_app.telegram_repo.send_message(  # type: ignore[attr-defined] # noqa: E501
                text
            )
            return "Failure notification sent", 200
        return "Workflow completed successfully", 200
    return "Ignored", 200
