from flask import Flask

from app.handler.commit_event import commit_bp
from app.handler.github_actions_failed_event import actions_bp
from app.handler.repo_update import update_repo_bp
from app.handler.review_requested_event import review_requested_bp

app = Flask(__name__)
app.register_blueprint(update_repo_bp)
app.register_blueprint(commit_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(review_requested_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
