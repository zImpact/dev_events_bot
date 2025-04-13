from app.repository.telegram import TelegramRepository
from app.config import REPO_NAMES
from app.utils import github_to_tg


def process_github_actions_failed_event(data):
    if data.get("action") == "completed" and "workflow_job" in data:
        repo = data["repository"]["name"]
        job = data["workflow_job"]
        job_name = job["name"]
        conclusion = job["conclusion"]
        workflow_url = job["html_url"]
        sender = data["sender"]["login"]
        project_name = REPO_NAMES.get(repo, repo)
        telegram_repo = TelegramRepository()

        if conclusion == "failure":
            text = (
                f"🚨 *Ошибка в GitHub Actions!* 🚨\n"
                f"🔧 *Проект:* {project_name}\n"
                f"⚠️ *Проблемная джоба:* `{job_name}`\n"
                f"👤 *Запустил:* [{sender}](tg://user?id={github_to_tg(sender)})\n"
                f"🔗 [Открыть Workflow]({workflow_url})"
            )
            telegram_repo.send_message(text)
            return "Failure notification sent", 200
        return "Workflow completed successfully", 200
    return "Ignored", 200
