from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.feedback import Feedback


feedback = Blueprint("feedback", __name__)


# ── POST /api/feedback ────────────────────────────────────────────────────────
# Flow 1: Just rate us
@feedback.route("/feedback", methods=["POST"])
@jwt_required()
def create_feedback():

    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}

    rating = data.get("rating")
    comment = data.get("comment")

    module = data.get("module")
    page = data.get("page")
    user_agent = request.headers.get("User-Agent")

    # ── Validation ────────────────────────────────────────────────────────────

    if rating is None:
        return jsonify({
            "error": "Rating is required"
        }), 400

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return jsonify({
            "error": "Rating must be a number between 1 and 5"
        }), 400

    if rating < 1 or rating > 5:
        return jsonify({
            "error": "Rating must be between 1 and 5"
        }), 400

    # ── Create feedback ──────────────────────────────────────────────────────

    new_feedback = Feedback(
        user_id=user_id,
        feedback_type="Rating",
        rating=rating,
        description=comment.strip() if isinstance(comment, str) and comment.strip() else None,
        module=module,
        page=page,
        user_agent=user_agent,
        status="New",
    )

    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({
        "message": "Thank you for your feedback!",
        "feedback_id": new_feedback.id,
    }), 201