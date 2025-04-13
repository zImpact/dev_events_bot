from app.config import TG_IDS


def github_to_tg(nickname):
    return TG_IDS.get(nickname, -1)
