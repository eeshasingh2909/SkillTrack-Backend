from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.project import Project

from services.github_service import (
    extract_github_username,
    extract_github_projects,
    save_github_projects,
    GitHubAPIError
)

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
# ── POST /api/projects/github-import ─────────────────────────────────────────

@project.route(
    "/projects/github-import",
    methods=["POST"]
)
@jwt_required()
def import_github_projects():

    try:

        # Get logged-in user from JWT
        user_id = int(
            get_jwt_identity()
        )

        # Get request data
        data = request.get_json(
            silent=True
        ) or {}

        github_url = data.get(
            "github_url",
            ""
        ).strip()

        if not github_url:
            return jsonify({
                "error":
                    "github_url is required"
            }), 400


        # Extract GitHub username
        github_username = (
            extract_github_username(
                github_url
            )
        )

        if not github_username:

            return jsonify({
                "error": (
                    "Invalid GitHub profile URL. "
                    "Example: "
                    "https://github.com/username"
                )
            }), 400


        # Extract repositories
        github_projects = (
            extract_github_projects(
                github_username
            )
        )


        # Save new projects
        new_projects = (
            save_github_projects(
                user_id,
                github_projects
            )
        )


        return jsonify({

            "message":
                "GitHub projects imported successfully",

            "github_username":
                github_username,

            "total_detected_projects":
                len(github_projects),

            "new_projects":
                new_projects

        }), 200


    except GitHubAPIError as e:

        return jsonify({
            "error": str(e)
        }), 400


    except Exception as e:

        print(
            "GitHub Project Import Error:",
            str(e)
        )

        return jsonify({
            "error":
                "Internal server error",

            "details":
                str(e)
        }), 500

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
