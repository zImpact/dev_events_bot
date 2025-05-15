import os
from app.repository.git import GitRepository
from app.config import SERVER_WSGI_PATH


def update_repository():
    git_repo = GitRepository()
    git_repo.pull_changes()
    os.system(f"touch {SERVER_WSGI_PATH}")
