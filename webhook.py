import os
import requests
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(text):
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(URL, data=data)


app = Flask(__name__)


@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return 400

    if "commits" in data:
        repo = data["repository"]["name"]
        pusher = data["pusher"]["name"]
        commit_messages = "\n".join(
            [f"- {commit['message']}" for commit in data["commits"]])
        text = f"🚀 Новый коммит в репозитории *{repo}* от {pusher}:\n{commit_messages}"

        send_message(text)
        return 200

    return 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
