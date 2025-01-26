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


def send_info(text):
    data = {"chat_id": CHAT_ID, "message_thread_id": THREAD_ID, "text": text}
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

    if "commits" in data:
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]
        commit_messages = "\n".join(
            [f"- {commit['message']}" for commit in data["commits"]])
        text = f"🚀 Новый коммит в репозитории *{repo}* от {pusher}:\n{commit_messages}"

        send_info(text)
        return "Message sended", 200

    return "Ignored", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
