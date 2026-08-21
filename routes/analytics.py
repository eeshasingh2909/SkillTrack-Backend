from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.skill import Skill
from models.project import Project


analytics = Blueprint("analytics", __name__)


@analytics.route("/analytics", methods=["GET"])
@jwt_required()
def get_analytics():

    try:
        user_id = int(get_jwt_identity())

        # ─────────────────────────────────────────────
        # Check user
        # ─────────────────────────────────────────────
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        # ─────────────────────────────────────────────
        # Skills
        # Remove duplicate skills for analytics
        # ─────────────────────────────────────────────
        skills = Skill.query.filter_by(
            user_id=user_id
        ).all()

        unique_skills = {}

        for skill in skills:

            if not skill.skill_name:
                continue

            normalized_name = skill.skill_name.strip()

            if not normalized_name:
                continue

            # Use lowercase as key so Python and python
            # are treated as the same skill
            skill_key = normalized_name.lower()

            if skill_key not in unique_skills:
                unique_skills[skill_key] = normalized_name

        skill_names = sorted(
            unique_skills.values(),
            key=str.lower
        )

        total_skills = len(skill_names)

        # ─────────────────────────────────────────────
        # Projects
        # ─────────────────────────────────────────────
        projects = Project.query.filter_by(
            user_id=user_id
        ).all()

        total_projects = len(projects)

        # ─────────────────────────────────────────────
        # Technology distribution
        # ─────────────────────────────────────────────
        technology_distribution = {}

        for project in projects:

            if not project.technology:
                continue

            technologies = project.technology.split(",")

            for technology in technologies:

                technology = technology.strip()

                if not technology:
                    continue

                # Normalize technology names so
                # Python and python are not separate
                technology_key = technology.lower()

                if technology_key not in technology_distribution:
                    technology_distribution[technology_key] = {
                        "name": technology,
                        "count": 0
                    }

                technology_distribution[
                    technology_key
                ]["count"] += 1

        # ─────────────────────────────────────────────
        # Convert to chart-friendly format
        # ─────────────────────────────────────────────
        technology_chart = sorted(
            technology_distribution.values(),
            key=lambda item: item["count"],
            reverse=True
        )

        # ─────────────────────────────────────────────
        # Recent projects
        # ─────────────────────────────────────────────
        recent_projects = sorted(
            projects,
            key=lambda project: (
                project.created_at is not None,
                project.created_at
            ),
            reverse=True
        )[:5]

        recent_projects_data = []

        for project in recent_projects:

            recent_projects_data.append({
                "id": project.id,
                "project_name": project.project_name,
                "technology": project.technology,
                "created_at": (
                    project.created_at.isoformat()
                    if project.created_at
                    else None
                )
            })

        # ─────────────────────────────────────────────
        # Profile completion
        # ─────────────────────────────────────────────
        profile_completion = 0

        if user.profile:

            profile_fields = []

            if hasattr(user.profile, "full_name"):
                profile_fields.append(
                    user.profile.full_name
                )

            if hasattr(user.profile, "bio"):
                profile_fields.append(
                    user.profile.bio
                )

            if hasattr(user.profile, "location"):
                profile_fields.append(
                    user.profile.location
                )

            if hasattr(user.profile, "github_url"):
                profile_fields.append(
                    user.profile.github_url
                )

            if hasattr(user.profile, "linkedin_url"):
                profile_fields.append(
                    user.profile.linkedin_url
                )

            if profile_fields:

                filled_fields = sum(
                    1
                    for field in profile_fields
                    if field and str(field).strip()
                )

                profile_completion = round(
                    (filled_fields / len(profile_fields)) * 100
                )

        # ─────────────────────────────────────────────
        # Final response
        # ─────────────────────────────────────────────
        return jsonify({

            "overview": {
                "total_skills": total_skills,
                "total_projects": total_projects,
                "profile_completion": profile_completion
            },

            "skills": skill_names,

            "technology_distribution": technology_chart,

            "recent_projects": recent_projects_data,

            # Placeholder for feedback/ratings module
            "ratings": {
                "average_rating": None,
                "total_ratings": 0,
                "total_feedback": 0
            }

        }), 200

    except Exception as error:

        return jsonify({
            "error": "Failed to fetch analytics",
            "details": str(error)
        }), 500