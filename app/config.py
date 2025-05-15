import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH")
SERVER_WSGI_PATH = os.getenv("SERVER_WSGI_PATH")
TELEGRAM_THREAD_ID = os.getenv("TELEGRAM_THREAD_ID")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_LOGIN_EMAIL = os.getenv("JIRA_LOGIN_EMAIL")

REPO_NAMES = {
    "yn": "Яна",
    "din": "Дни нигде",
    "tmlp": "Петля времени",
    "osd": "Один украденный день",
    "thld": "Преддверие",
    "bsar": "Между сном и явью"
}

TG_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_TG_ID"),
    "paych3ck": os.getenv("ANDREY_TG_ID"),
    "Buhicevskij": os.getenv("DANYA_TG_ID"),
    "Aleron-Meredi": os.getenv("EGOR_TG_ID")
}

JIRA_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_JIRA_ID"),
    "paych3ck": os.getenv("ANDREY_JIRA_ID"),
    "Buhicevskij": os.getenv("DANYA_JIRA_ID")
}

JIRA_REVIEWER_FIELD_IDS = {
    "yn": 10092,
    "din": 10042,
    "tmlp": 10041,
    "osd": 10091,
    "thld": 10039,
    "bsar": 10093,
    "dev_events_bot": 10040
}
