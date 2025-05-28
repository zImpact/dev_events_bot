import os

from flask import current_app

from app.config import SERVER_WSGI_PATH


def update_repository() -> None:
    current_app.git_repo.pull_changes()  # type: ignore[attr-defined]
    os.system(f"touch {SERVER_WSGI_PATH}")
