import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GIT_REPO_PATH = os.environ["GIT_REPO_PATH"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO_OWNER = os.environ["GITHUB_REPO_OWNER"]
SERVER_WSGI_PATH = os.environ["SERVER_WSGI_PATH"]
TELEGRAM_THREAD_ID = os.environ["TELEGRAM_THREAD_ID"]
JIRA_BASE_URL = os.environ["JIRA_BASE_URL"]
JIRA_API_TOKEN = os.environ["JIRA_API_TOKEN"]
JIRA_LOGIN_EMAIL = os.environ["JIRA_LOGIN_EMAIL"]

MAIN_BRANCH = "main"

REPO_NAMES = {
    "yn": "Яна",
    "din": "Дни нигде",
    "tmlp": "Петля времени",
    "osd": "Один украденный день",
    "thld": "Преддверие",
    "bsar": "Между сном и явью",
}

TG_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_TG_ID"),
    "paych3ck": os.getenv("ANDREY_TG_ID"),
    "Buhicevskij": os.getenv("DANYA_TG_ID"),
    "Aleron-Meredi": os.getenv("EGOR_TG_ID"),
}

JIRA_IDS = {
    "DmytroMamedbekov": os.getenv("DMYTRO_JIRA_ID"),
    "paych3ck": os.getenv("ANDREY_JIRA_ID"),
    "Buhicevskij": os.getenv("DANYA_JIRA_ID"),
}

JIRA_REVIEWER_FIELD_IDS = {
    "yn": 10092,
    "din": 10042,
    "tmlp": 10041,
    "osd": 10091,
    "thld": 10039,
    "bsar": 10093,
    "dev_events_bot": 10040,
}
