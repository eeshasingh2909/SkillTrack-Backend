from models import db

class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    profile  = db.relationship("Profile",  backref="user", uselist=False, cascade="all, delete")
    skills   = db.relationship("Skill",    backref="user", cascade="all, delete-orphan", lazy=True)
    projects = db.relationship("Project",  backref="user", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
