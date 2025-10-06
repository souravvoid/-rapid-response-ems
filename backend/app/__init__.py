from flask import Flask
from flask_cors import CORS
from .db import db
from .routes.incidents import incidents_bp
from .routes.ambulances import ambulances_bp

def create_app():
    app = Flask(__name__, static_folder="../../frontend", template_folder="../../frontend")
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(incidents_bp, url_prefix="/incidents")
    app.register_blueprint(ambulances_bp, url_prefix="/ambulances")

    # Serve frontend
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app
