from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions.db import init_db
from extensions.jwt import init_jwt
from middleware.auth import jwt_unauthorized_loader
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.video import video_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    """Application factory for the video backend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for the React Native client
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Init extensions
    init_db(app)
    init_jwt(app)

    # Register blueprints (all under /api prefix)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(video_bp, url_prefix="/api")

    # Health check
    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    # Attach custom JWT unauthorized handler
    jwt_unauthorized_loader(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

