import re

from app.config import JIRA_IDS, TG_IDS


def github_to_tg(nickname: str) -> str | None:
    return TG_IDS.get(nickname)


def github_to_jira(nickname: str) -> str | None:
    return JIRA_IDS.get(nickname)


def escape_markdown(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
