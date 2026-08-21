from models.user import User
from app import app
with app.app_context():
    users = User.query.all()

    for user in users:
        print(
            user.id,
            user.email
        )