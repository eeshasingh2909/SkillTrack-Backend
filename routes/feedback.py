from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db
from models.feedback import Feedback, FEEDBACK_TYPES
from models.user import User


feedback = Blueprint("feedback", __name__)


# ── POST /api/feedback ────────────────────────────────────────────────────────
@feedback.route("/feedback", methods=["POST"])
@jwt_required()
def create_feedback():

    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}

    rating          = data.get("rating")
    positive_comment = data.get("positive_comment")
    feedback_text   = data.get("feedback")
    feedback_type   = data.get("feedback_type")

    # ── Validation ────────────────────────────────────────────────────────────

    if rating is None:
        return jsonify({"error": "Rating is required"}), 400

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return jsonify({"error": "Rating must be a number between 1 and 5"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    if feedback_type is not None and feedback_type not in FEEDBACK_TYPES:
        return jsonify({
            "error": f"feedback_type must be one of: {', '.join(FEEDBACK_TYPES)}"
        }), 400

    # ── Create feedback ───────────────────────────────────────────────────────

    new_feedback = Feedback(
        user_id=user_id,
        rating=rating,
        positive_comment=positive_comment.strip() if isinstance(positive_comment, str) and positive_comment.strip() else None,
        feedback=feedback_text.strip() if isinstance(feedback_text, str) and feedback_text.strip() else None,
        feedback_type=feedback_type if feedback_type else None,
    )

    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({
        "message": "Thank you for your feedback!",
        "feedback_id": new_feedback.id,
    }), 201


# ── GET /api/feedback ─────────────────────────────────────────────────────────
# Returns the latest feedback per user for footer cards (auth required)
@feedback.route("/feedback", methods=["GET"])
@jwt_required()
def get_feedback():

    # Subquery: latest created_at per user
    latest_per_user = (
        db.session.query(
            Feedback.user_id,
            func.max(Feedback.created_at).label("latest_at")
        )
        .group_by(Feedback.user_id)
        .subquery()
    )

    # Join back to get the full feedback row + username
    rows = (
        db.session.query(
            User.username,
            Feedback.rating,
            Feedback.positive_comment,
            Feedback.created_at,
        )
        .join(latest_per_user, (Feedback.user_id == latest_per_user.c.user_id) &
                                (Feedback.created_at == latest_per_user.c.latest_at))
        .join(User, User.id == Feedback.user_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )

    result = [
        {
            "username":         row.username,
            "rating":           row.rating,
            "positive_comment": row.positive_comment,
            "created_at":       row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]

    return jsonify(result), 200
