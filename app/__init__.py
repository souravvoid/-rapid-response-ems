from flask import Flask
from flask_cors import CORS
from .db import db

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-change-this"

    CORS(app, supports_credentials=True)
    db.init_app(app)

    # register routes
    from .routes.auth import auth_bp
    from .routes.emergency import emergency_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(emergency_bp)

    with app.app_context():
        db.create_all()

    return app
