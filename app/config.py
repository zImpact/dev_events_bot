import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REPO_PATH = os.getenv("GITHUB_REPO_PATH")
WSGI_PATH = os.getenv("SERVER_WSGI_PATH")
THREAD_ID = os.getenv("TELEGRAM_THREAD_ID")

REPO_NAMES = {
    "yn": "Яна",
    "din": "Дни нигде",
    "tmlp": "Петля времени",
    "osd": "Один украденный день",
    "thld": "Преддверие",
    "bsar": "Между сном и явью"
}

TG_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_ID"),
    "paych3ck": os.getenv("ANDREY_ID"),
    "Buhicevskij": os.getenv("DANYA_ID"),
    "Aleron-Meredi": os.getenv("EGOR_ID")
}
