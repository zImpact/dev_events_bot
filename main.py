import os
import requests
import git
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REPO_PATH = os.getenv("GITHUB_REPO_PATH")
WSGI_PATH = os.getenv("SERVER_WSGI_PATH")
THREAD_ID = os.getenv("TELEGRAM_THREAD_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
TG_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_ID"),
    "paych3ck": os.getenv("ANDREY_ID"),
    "Buhicevskij": os.getenv("DANYA_ID"),
    "Aleron-Meredi": os.getenv("EGOR_ID")
}
REPO_NAMES = {
    "yana": "Яна",
    "din": "Дни нигде",
    "tl": "Петля времени",
    "osd": "Один украденный день",
    "thld": "Преддверие",
    "bsar": "Между сном и явью"
}


def github_to_tg(nickname):
    return TG_IDS.get(nickname, -1)


def send_info(text):
    data = {"chat_id": CHAT_ID, "message_thread_id": THREAD_ID,
            "parse_mode": "Markdown", "text": text, "disable_web_page_preview": 1}
    response = requests.post(URL, data=data)
    return response.json()


app = Flask(__name__)


@app.route("/update_repo", methods=["POST"])
def update_repo():
    try:
        repo = git.Repo(REPO_PATH)
        origin = repo.remotes.origin

        repo.git.reset("--hard")
        repo.git.clean("-fd")

        origin.pull()
        os.system(f"touch {WSGI_PATH}")
        return "Updated and restarted", 200
    except Exception as e:
        return f"Update failed: {str(e)}", 500


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    if not data:
        return "No data", 400

    # if data.get("action") == "opened" and "issue" in data:
    #     repo = data["repository"]["name"]
    #     issue = data["issue"]
    #     title = issue["title"]
    #     user = data["sender"]["login"]
    #     url = issue["html_url"]

    #     project_name = REPO_NAMES.get(repo, repo)

    #     text = f"🆕 Новая задача в проекте *{project_name}*!\n👤 *Автор:* {user}\n📌 *Название:* {title}\n🔗 [Открыть задачу]({url})"
    #     send_info(text)
    #     return "Issue created and sent to Telegram", 200

    if data.get("action") == "completed" and "workflow_job" in data:
        repo = data["repository"]["name"]
        job = data["workflow_job"]
        job_name = job["name"]
        conclusion = job["conclusion"]
        workflow_url = job["html_url"]
        sender = data["sender"]["login"]

        project_name = REPO_NAMES.get(repo, repo)

        if conclusion == "failure":
            text = f"🚨 *Ошибка в GitHub Actions!* 🚨\n🔧 *Проект:* {repo}\n⚠️ *Проблемная джоба:* `{job_name}`\n👤 *Запустил:* [{sender}](tg://user?id={github_to_tg(sender)})\n🔗 [Открыть Workflow]({workflow_url})"

            send_info(text)
            return "Failure notification sent", 200

        return "Ignored", 200

    if data.get("action") == "assigned" and "issue" in data:
        repo = data["repository"]["name"]
        issue = data["issue"]
        assignee = data["assignee"]["login"]
        title = issue["title"]
        url = issue["html_url"]

        project_name = REPO_NAMES.get(repo, repo)

        text = f"🎯 Назначен исполнитель задачи в проекте *{project_name}*!\n📌 *Название:* {title}\n👤 *Исполнитель:* [{assignee}](tg://user?id={github_to_tg(assignee)})\n🔗 [Открыть задачу]({url})"
        send_info(text)
        return "Assignment notification sent", 200

    if data.get("action") == "closed" and "issue" in data:
        repo = data["repository"]["name"]
        issue = data["issue"]
        title = issue["title"]
        url = issue["html_url"]

        project_name = REPO_NAMES.get(repo, repo)

        text = f"✅ Задача в проекте *{project_name}* закрыта!\n📌 *Название:* {title}\n🔗 [Открыть задачу]({url})"
        send_info(text)
        return "Issue closed notification sent", 200

    if "commits" in data:
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]

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

        text = (f"🚀 Новый коммит в репозитории *{repo_part}*!\n"
                f"👤 *Автор:* [{pusher}](tg://user?id={github_to_tg(pusher)})\n"
                f"📝 *Изменения:*\n{commit_text_block}\n"
                f"🔗 [Открыть репозиторий]({data['repository']['html_url']})"
                )

        send_info(text)
        return "Message sended", 200

    return "Ignored", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
