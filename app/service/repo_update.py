import os

from app.config import SERVER_WSGI_PATH
from app.repository.git import GitRepository


def update_repository():
    git_repo = GitRepository()
    git_repo.pull_changes()
    os.system(f"touch {SERVER_WSGI_PATH}")
