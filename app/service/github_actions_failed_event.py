from flask import current_app

from app.config import REPO_NAMES
from app.utils import escape_markdown, github_to_tg


def process_github_actions_failed_event(data):
    if data.get("action") == "completed" and "workflow_job" in data:
        repo = data["repository"]["name"]
        job = data["workflow_job"]
        job_name = job["name"]
        conclusion = job["conclusion"]
        workflow_url = job["html_url"]
        sender = data["sender"]["login"]
        project_name = REPO_NAMES.get(repo, repo)
        sender_mention = f"tg://user?id={github_to_tg(sender)}"

        if conclusion == "failure":
            text = (
                f"🚨 *Ошибка в GitHub Actions!* 🚨\n"
                f"🔧 *Проект:* {escape_markdown(project_name)}\n"
                f"⚠️ *Проблемная джоба:* `{job_name}`\n"
                f"👤 *Запустил:* [{sender}]({sender_mention})\n"
                f"🔗 [Открыть Workflow]({workflow_url})"
            )
            current_app.telegram_repo.send_message(text)
            return "Failure notification sent", 200
        return "Workflow completed successfully", 200
    return "Ignored", 200
