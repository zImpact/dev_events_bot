from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.service.pull_request_merged_event import (
    process_pull_request_merged_event,
)

pull_request_merged_bp = Blueprint("pull_request_merged", __name__)


@pull_request_merged_bp.route("/webhook/pull_request_merged", methods=["POST"])
def pull_request_merged_event() -> tuple[Response, int]:
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    message, status = process_pull_request_merged_event(data)
    return jsonify({"message": message}), status
