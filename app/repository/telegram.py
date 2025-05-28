from typing import Any

import requests

from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_THREAD_ID


class TelegramRepository:
    def __init__(self) -> None:
        self.url = (
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        )

    def send_message(self, text: str) -> Any:
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "message_thread_id": TELEGRAM_THREAD_ID,
            "parse_mode": "Markdown",
            "text": text,
            "disable_web_page_preview": 1,
        }
        response = requests.post(self.url, data=data)
        return response.json()
