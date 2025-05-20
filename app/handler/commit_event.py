from flask import Blueprint, jsonify, request

from app.service.commit_event import process_commit_event

commit_bp = Blueprint("commit", __name__)


@commit_bp.route("/webhook/commits", methods=["POST"])
def commit_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    message, status = process_commit_event(data)
    return jsonify({"message": message}), status
