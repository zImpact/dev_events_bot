# app/handlers/github_actions_handler.py
from flask import Blueprint, request, jsonify
from app.service.github_actions_failed_event import process_github_actions_failed_event

actions_bp = Blueprint("github_actions", __name__)


@actions_bp.route("/webhook/github_actions", methods=["POST"])
def github_actions_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    message, status = process_github_actions_failed_event(data)
    return jsonify({"message": message}), status
