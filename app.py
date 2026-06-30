from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# ── Extensions ────────────────────────────────────────────────────────────────
db.init_app(app)
JWTManager(app)

# Allow requests from the Vite dev server (port 3000 — 5173 is used by Apple AirTunes)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

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

app.register_blueprint(auth,      url_prefix="/api/auth")
app.register_blueprint(profile,   url_prefix="/api")
app.register_blueprint(project,   url_prefix="/api")
app.register_blueprint(dashboard, url_prefix="/api")
app.register_blueprint(skill,     url_prefix="/api")

# ── DB init ───────────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
