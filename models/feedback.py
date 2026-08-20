from models import db


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # For Flow 1 this will always be "Rating"
    feedback_type = db.Column(
        db.String(50),
        nullable=False,
        default="Rating"
    )

    # 1–5 stars
    rating = db.Column(
        db.Integer,
        nullable=False
    )

    # Optional comment for the rating-only flow
    description = db.Column(
        db.Text,
        nullable=True
    )

    # Automatically captured application context
    module = db.Column(
        db.String(100),
        nullable=True
    )

    page = db.Column(
        db.String(255),
        nullable=True
    )

    # Automatically captured technical context
    user_agent = db.Column(
        db.String(500),
        nullable=True
    )

    # System-managed
    status = db.Column(
        db.String(30),
        nullable=False,
        default="New"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Feedback {self.id} - User {self.user_id}>"