from app.config import REPO_NAMES
from app.repository.telegram import TelegramRepository
from app.utils import github_to_tg


def process_commit_event(data):
    if "commits" in data and data["commits"]:
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]
        telegram_repo = TelegramRepository()

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

        telegram_repo.send_message(text)
        return "Commit event processed", 200

    return "Ignored", 200
