from flask import Blueprint, jsonify
from flask.wrappers import Response

from app.service.repo_update import update_repository

update_repo_bp = Blueprint("update_repo", __name__)


@update_repo_bp.route("/update_repo", methods=["POST"])
def update_repo() -> tuple[Response, int]:
    try:
        update_repository()
        return jsonify({"message": "Repository updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
