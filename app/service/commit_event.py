from app.repository.telegram import TelegramRepository
from app.config import REPO_NAMES
from app.utils import github_to_tg


def process_commit_event(data):
    if "commits" in data and data["commits"]:
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]
        telegram_repo = TelegramRepository()

        project_name = REPO_NAMES.get(repo, repo)
        repo_part = f"{project_name}" if project_name != repo else f"{repo}"

        commit_messages = []
        for commit in data["commits"]:
            commit_title, commit_desc = (
                commit["message"].split("\n\n", 1) + [""])[:2]
            commit_text = f"- [{commit_title}]({commit['url']})"
            if commit_desc.strip():
                commit_text += f"\n  _{commit_desc.strip()}_"
            commit_messages.append(commit_text)

        commit_text_block = "\n".join(commit_messages)

        text = (
            f"🚀 Новый коммит в репозитории проекта *{repo_part}*!\n"
            f"👤 *Автор:* [{pusher}](tg://user?id={github_to_tg(pusher)})\n"
            f"📝 *Изменения:*\n{commit_text_block}\n"
            f"🔗 [Открыть репозиторий]({data['repository']['html_url']})"
        )

        telegram_repo.send_message(text)
        return "Commit event processed", 200

    return "Ignored", 200
