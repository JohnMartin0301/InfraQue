from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return "Home page"

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Access denied", "danger")
        
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html", username=session.get("username")) 