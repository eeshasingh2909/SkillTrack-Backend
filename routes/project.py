from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.project import Project

project = Blueprint("project", __name__)


# ── GET /api/projects ─────────────────────────────────────────────────────────
# ── POST /api/projects ────────────────────────────────────────────────────────
@project.route("/projects", methods=["GET", "POST"])
@jwt_required()
def projects():
    user_id = int(get_jwt_identity())

    if request.method == "GET":
        all_projects = Project.query.filter_by(user_id=user_id).all()
        return jsonify([_project_dict(p) for p in all_projects]), 200

    # POST
    data = request.get_json(silent=True) or {}
    project_name = data.get("project_name", "").strip()

    if not project_name:
        return jsonify({"error": "project_name is required"}), 400

    new_project = Project(
        user_id=user_id,
        project_name=project_name,
        technology=data.get("technology"),
        description=data.get("description"),
        github_link=data.get("github_link"),
        demo_link=data.get("demo_link"),
    )
    db.session.add(new_project)
    db.session.commit()

    return jsonify(_project_dict(new_project)), 201


# ── DELETE /api/projects/<id> ─────────────────────────────────────────────────
@project.route("/projects/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user_id = int(get_jwt_identity())
    item = Project.query.get(project_id)

    if not item:
        return jsonify({"error": "Project not found"}), 404
    if item.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Project deleted"}), 200


# ── Helper ────────────────────────────────────────────────────────────────────
def _project_dict(p):
    return {
        "id":           p.id,
        "project_name": p.project_name,
        "technology":   p.technology,
        "description":  p.description,
        "github_link":  p.github_link,
        "demo_link":    p.demo_link,
        "created_at":   str(p.created_at),
    }
