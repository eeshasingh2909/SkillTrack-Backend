from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.skill import Skill

skill = Blueprint("skill", __name__)


# ── GET /api/skills ───────────────────────────────────────────────────────────
# ── POST /api/skills ──────────────────────────────────────────────────────────
@skill.route("/skills", methods=["GET", "POST"])
@jwt_required()
def skills():
    user_id = int(get_jwt_identity())

    if request.method == "GET":
        all_skills = Skill.query.filter_by(user_id=user_id).all()
        return jsonify([{"id": s.id, "skill_name": s.skill_name} for s in all_skills]), 200

    # POST
    data = request.get_json(silent=True) or {}
    skill_name = data.get("skill_name", "").strip()

    if not skill_name:
        return jsonify({"error": "skill_name is required"}), 400

    new_skill = Skill(user_id=user_id, skill_name=skill_name)
    db.session.add(new_skill)
    db.session.commit()

    return jsonify({"id": new_skill.id, "skill_name": new_skill.skill_name}), 201


# ── DELETE /api/skills/<id> ───────────────────────────────────────────────────
@skill.route("/skills/<int:skill_id>", methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):
    user_id = int(get_jwt_identity())
    item = Skill.query.get(skill_id)

    if not item:
        return jsonify({"error": "Skill not found"}), 404
    if item.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Skill deleted"}), 200
