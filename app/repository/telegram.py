import requests
from app.config import TOKEN, CHAT_ID, THREAD_ID


class TelegramRepository:
    def __init__(self):
        self.url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    def send_message(self, text):
        data = {
            "chat_id": CHAT_ID,
            "message_thread_id": THREAD_ID,
            "parse_mode": "Markdown",
            "text": text,
            "disable_web_page_preview": 1
        }
        response = requests.post(self.url, data=data)
        return response.json()
