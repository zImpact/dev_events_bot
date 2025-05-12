from app.config import TG_IDS, JIRA_IDS


def github_to_tg(nickname):
    return TG_IDS.get(nickname, -1)

def github_to_jira(nickname):
    return JIRA_IDS.get(nickname, -1)