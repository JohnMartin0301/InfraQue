from functools import wraps
from flask import session, flash, redirect, url_for
from .models import User

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            flash("Please login to access this page.", "danger")
            return redirect(url_for("auth.login"))
        session["role"] = user.role
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            print(f"DEBUG: user={user}, required_role={role}, user_role={user.role if user else None}")
            if not user:
                flash("Please login to access this page.", "danger")
                return redirect(url_for("auth.login"))
            session["role"] = user.role
            if user.role != role:
                flash("Access denied. You do not have permission to view this page.", "danger")
                return redirect(url_for("main.dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator