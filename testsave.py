from services.github_service import save_github_skills
from app import app
with app.app_context():
    new_skills = save_github_skills(
        7,
        [
            "PythonFlasky",
            "JavaScriptsy",
            "HTMLs"
        ]
    )

    print(new_skills)