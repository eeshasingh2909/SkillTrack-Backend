from app import app
from models.project import Project


with app.app_context():

    projects = Project.query.all()

    print("Projects table working.")

    print(
        "Existing projects:",
        len(projects)
    )