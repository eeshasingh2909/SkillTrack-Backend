from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.profile import Profile

profile = Blueprint("profile", __name__)


# ── GET /api/profile ──────────────────────────────────────────────────────────
# ── PUT /api/profile ──────────────────────────────────────────────────────────
@profile.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile_page():
    user_id = int(get_jwt_identity())
    student = Profile.query.filter_by(user_id=user_id).first()

    if request.method == "GET":
        if student is None:
            return jsonify({
                "full_name": None, "phone": None, "college": None,
                "degree": None, "graduation_year": None,
                "linkedin": None, "github": None, "bio": None,
            }), 200

        return jsonify({
            "full_name":       student.full_name,
            "phone":           student.phone,
            "college":         student.college,
            "degree":          student.degree,
            "graduation_year": student.graduation_year,
            "linkedin":        student.linkedin,
            "github":          student.github,
            "bio":             student.bio,
        }), 200

    # PUT — upsert
    data = request.get_json(silent=True) or {}

    if student is None:
        student = Profile(user_id=user_id)
        db.session.add(student)

    student.full_name       = data.get("full_name",       student.full_name)
    student.phone           = data.get("phone",           student.phone)
    student.college         = data.get("college",         student.college)
    student.degree          = data.get("degree",          student.degree)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.linkedin        = data.get("linkedin",        student.linkedin)
    student.github          = data.get("github",          student.github)
    student.bio             = data.get("bio",             student.bio)

    db.session.commit()

    return jsonify({
        "full_name":       student.full_name,
        "phone":           student.phone,
        "college":         student.college,
        "degree":          student.degree,
        "graduation_year": student.graduation_year,
        "linkedin":        student.linkedin,
        "github":          student.github,
        "bio":             student.bio,
    }), 200
