from models import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    project_name = db.Column(db.String(150), nullable=False)

    technology = db.Column(db.String(150))

    description = db.Column(db.Text)

    github_link = db.Column(db.String(255))

    demo_link = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )