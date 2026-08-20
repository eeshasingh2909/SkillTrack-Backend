from services.github_service import (
    extract_github_skills,
    save_github_skills
)
from app import app
github_skills = extract_github_skills(
    "eeshasingh2909"
)
print(github_skills)

with app.app_context():
    new_skills = save_github_skills(
        7,
        github_skills
    )

    print(new_skills)