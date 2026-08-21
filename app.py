from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.github_routes import github_bp
from config import Config
from models import db
from routes.analytics import analytics
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(github_bp)

# ── Extensions ────────────────────────────────────────────────────────────────
db.init_app(app)
jwt=JWTManager(app)

# Allow all localhost origins during development
# Covers: Vite on 3000, 5173, or any other port it picks
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(_):
    return jsonify({"error": "Internal server error"}), 500

# ── Blueprints (all under /api) ───────────────────────────────────────────────
from routes.auth import auth
from routes.profile import profile
from routes.project import project
from routes.dashboard import dashboard
from routes.skill import skill
from routes.feedback import feedback #new addition

app.register_blueprint(auth,      url_prefix="/api/auth")
app.register_blueprint(profile,   url_prefix="/api")
app.register_blueprint(project,   url_prefix="/api")
app.register_blueprint(dashboard, url_prefix="/api")
app.register_blueprint(skill,     url_prefix="/api")
app.register_blueprint(feedback,  url_prefix="/api") #new addition
app.register_blueprint(analytics, url_prefix="/api")

# ── DB init ───────────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use 5001 — port 5000 may be taken by AirPlay on macOS
