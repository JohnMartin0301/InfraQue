from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.requests.routes import request_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(admin_bp)

    return app