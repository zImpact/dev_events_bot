from github import Github, PullRequest

from app.config import GITHUB_REPO_OWNER, GITHUB_TOKEN


class GithubRepository:
    def __init__(self) -> None:
        self.gh = Github(GITHUB_TOKEN)

    def get_associated_prs(
        self, repo_name: str, commit_sha: str
    ) -> list[PullRequest.PullRequest]:
        repo = self.gh.get_repo(f"{GITHUB_REPO_OWNER}/{repo_name}")
        commit = repo.get_commit(commit_sha)
        pulls = list(commit.get_pulls())
        return pulls

    def get_first_pr_url(self, repo_name: str, commit_sha: str) -> str:
        pulls = self.get_associated_prs(repo_name, commit_sha)
        return pulls[0].html_url
