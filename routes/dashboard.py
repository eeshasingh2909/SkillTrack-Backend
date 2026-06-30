from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.profile import Profile
from models.skill import Skill
from models.project import Project

dashboard = Blueprint("dashboard", __name__)


# ── GET /api/dashboard ────────────────────────────────────────────────────────
@dashboard.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard_page():
    user_id = int(get_jwt_identity())

    prof = Profile.query.filter_by(user_id=user_id).first()

    total_skills   = Skill.query.filter_by(user_id=user_id).count()
    total_projects = Project.query.filter_by(user_id=user_id).count()

    recent_projects = Project.query.filter_by(user_id=user_id) \
        .order_by(Project.id.desc()).limit(5).all()

    return jsonify({
        "total_skills":   total_skills,
        "total_projects": total_projects,
        "recent_projects": [
            {
                "id":           p.id,
                "project_name": p.project_name,
                "technology":   p.technology,
                "description":  p.description,
                "github_link":  p.github_link,
                "demo_link":    p.demo_link,
                "created_at":   str(p.created_at),
            }
            for p in recent_projects
        ],
        "profile": {
            "full_name":       prof.full_name,
            "phone":           prof.phone,
            "college":         prof.college,
            "degree":          prof.degree,
            "graduation_year": prof.graduation_year,
            "linkedin":        prof.linkedin,
            "github":          prof.github,
            "bio":             prof.bio,
        } if prof else None,
    }), 200
