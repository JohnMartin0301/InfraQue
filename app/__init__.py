from flask import Flask
from .config import Config
from .extensions import db, bcrypt

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.requests.routes import requests_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(admin_bp)

    return app