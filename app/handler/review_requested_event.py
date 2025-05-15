from flask import Blueprint, request, jsonify
from app.service.review_requested_event import process_review_requested_event

review_requested_bp = Blueprint("review_requested", __name__)


@review_requested_bp.route("/webhook/review_requested", methods=["POST"])
def review_requested_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    message, status = process_review_requested_event(data)
    return jsonify({"message": message}), status
