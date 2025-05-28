import git

from app.config import GITHUB_REPO_PATH


class GitRepository:
    def __init__(self) -> None:
        self.repo = git.Repo(GITHUB_REPO_PATH)
        self.origin = self.repo.remotes.origin

    def pull_changes(self) -> None:
        self.repo.git.reset("--hard")
        self.repo.git.clean("-fd")
        self.origin.pull()
