from models import db

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    college = db.Column(db.String(150))
    degree = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    bio = db.Column(db.Text)