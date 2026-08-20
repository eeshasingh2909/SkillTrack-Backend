from flask import Blueprint, jsonify, request

from models.skill import Skill
from models.user import User
from models import db

from services.github_service import (
    extract_github_username,
    extract_github_skills,
    save_github_skills,
    extract_github_projects,
    save_github_projects,
    GitHubAPIError
)


github_bp = Blueprint(
    "github",
    __name__
)


# ==================================================
# IMPORT GITHUB SKILLS
# ==================================================

@github_bp.route(
    "/api/users/<int:user_id>/github-skills",
    methods=["POST"]
)
def get_github_skills(user_id):

    try:

        # Check user exists
        user = db.session.get(
            User,
            user_id
        )

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404


        # Get request JSON
        data = request.get_json(
            silent=True
        )

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400


        # Frontend sends github_url
        github_url = data.get(
            "github_url"
        )

        if not github_url:
            return jsonify({
                "error": "github_url is required"
            }), 400


        # Extract username
        github_username = (
            extract_github_username(
                github_url
            )
        )

        if not github_username:
            return jsonify({
                "error": (
                    "Invalid GitHub profile URL. "
                    "Example: https://github.com/username"
                )
            }), 400


        # Extract skills
        github_skills = extract_github_skills(
            github_username
        )


        # Save skills
        new_skills = save_github_skills(
            user_id,
            github_skills
        )


        return jsonify({

            "message":
                "GitHub skills extracted successfully",

            "user_id":
                user_id,

            "github_url":
                github_url,

            "github_username":
                github_username,

            "total_detected_skills":
                len(github_skills),

            "skills":
                github_skills,

            "new_skills":
                new_skills

        }), 200


    except GitHubAPIError as e:

        return jsonify({
            "error": str(e)
        }), 400


    except Exception as e:

        print(
            "GitHub Skills Error:",
            str(e)
        )

        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


# ==================================================
# IMPORT GITHUB PROJECTS
# ==================================================

@github_bp.route(
    "/api/users/<int:user_id>/github-projects",
    methods=["POST"]
)
def import_github_projects(user_id):

    try:

        # Check user exists
        user = db.session.get(
            User,
            user_id
        )

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404


        # Get request JSON
        data = request.get_json(
            silent=True
        )

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400


        # Accept either GitHub URL or username
        github_url = data.get(
            "github_url"
        )

        github_username = data.get(
            "github_username"
        )


        # If URL is sent, extract username
        if github_url:

            github_username = (
                extract_github_username(
                    github_url
                )
            )

            if not github_username:
                return jsonify({
                    "error": (
                        "Invalid GitHub profile URL. "
                        "Example: https://github.com/username"
                    )
                }), 400


        # If neither exists
        if not github_username:
            return jsonify({
                "error": (
                    "github_url or github_username "
                    "is required"
                )
            }), 400


        github_username = (
            github_username.strip()
        )

        if not github_username:
            return jsonify({
                "error":
                    "GitHub username cannot be empty"
            }), 400


        # Extract projects
        github_projects = (
            extract_github_projects(
                github_username
            )
        )


        # Save projects
        new_projects = save_github_projects(
            user_id,
            github_projects
        )


        return jsonify({

            "message":
                "GitHub projects imported successfully",

            "user_id":
                user_id,

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
            "GitHub Projects Error:",
            str(e)
        )

        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


# ==================================================
# GET USER SKILLS
# ==================================================

@github_bp.route(
    "/api/users/<int:user_id>/skills",
    methods=["GET"]
)
def get_user_skills(user_id):

    try:

        # Check user exists
        user = db.session.get(
            User,
            user_id
        )

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404


        skills = Skill.query.filter_by(
            user_id=user_id
        ).all()


        skills_list = []

        for skill in skills:

            skills_list.append({

                "id":
                    skill.id,

                "name":
                    skill.skill_name

            })


        return jsonify({

            "user_id":
                user_id,

            "total_skills":
                len(skills_list),

            "skills":
                skills_list

        }), 200


    except Exception as e:

        print(
            "Get Skills Error:",
            str(e)
        )

        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500