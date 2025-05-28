from flask import Flask

from app.handler.commit_event import commit_bp
from app.handler.github_actions_failed_event import actions_bp
from app.handler.repo_update import update_repo_bp
from app.handler.review_requested_event import review_requested_bp
from app.repository.git import GitRepository
from app.repository.jira import JiraRepository
from app.repository.telegram import TelegramRepository


def create_app() -> Flask:
    app = Flask(__name__)
    app.git_repo = GitRepository()  # type: ignore[attr-defined]
    app.jira_repo = JiraRepository()  # type: ignore[attr-defined]
    app.telegram_repo = TelegramRepository()  # type: ignore[attr-defined]
    app.register_blueprint(update_repo_bp)
    app.register_blueprint(commit_bp)
    app.register_blueprint(actions_bp)
    app.register_blueprint(review_requested_bp)
    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
