import os

from flask import current_app

from app.config import SERVER_WSGI_PATH


def update_repository():
    current_app.git_repo.pull_changes()
    os.system(f"touch {SERVER_WSGI_PATH}")
