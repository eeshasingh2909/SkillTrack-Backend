
from app import app
from models.skill import Skill

with app.app_context():
    skills = Skill.query.all()

    for skill in skills:
        print(
            skill.id,
            skill.user_id,
            skill.skill_name
        )