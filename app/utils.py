from app.config import TG_IDS, JIRA_IDS

def github_to_tg(nickname):
    return TG_IDS.get(nickname, -1)

def github_to_jira(nickname):
    return JIRA_IDS.get(nickname, -1)

def escape_markdown(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

