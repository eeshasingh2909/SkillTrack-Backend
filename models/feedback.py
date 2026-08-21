from models import db


FEEDBACK_TYPES = ("Bug", "Improvement", "Feature Request")


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # 1–5 stars (required)
    rating = db.Column(
        db.Integer,
        nullable=False
    )

    # Optional positive comment ("What did you like?")
    positive_comment = db.Column(
        db.Text,
        nullable=True
    )

    # Optional negative feedback / report
    feedback = db.Column(
        db.Text,
        nullable=True
    )

    # Optional category: "Bug" | "Improvement" | "Feature Request"
    feedback_type = db.Column(
        db.String(50),
        nullable=True
    )

    # System-managed timestamps
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # Relationship to User (for joins in GET endpoint)
    user = db.relationship("User", backref=db.backref("feedbacks", lazy=True))

    def __repr__(self):
        return f"<Feedback {self.id} - User {self.user_id}>"
