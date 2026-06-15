from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Access denied. Please login first", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("user_id"):
                flash("Access denied. Please login first", "danger")
                return redirect(url_for("auth.login"))
            if session.get("role") != role:
                flash("Access denied. You don't have permission to access this page", "danger")
                return redirect(url_for("main.dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator