import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_REGISTRATION_CODE = os.environ.get("ADMIN_REGISTRATION_CODE")
    WTF_CSRF_ENABLED = True