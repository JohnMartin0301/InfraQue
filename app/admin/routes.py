from flask import Blueprint, session, redirect, url_for, flash, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin-page")
def admin_home():

    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    if session.get("role") != "Admin":
        flash("Access denied")
        return redirect(url_for("main.dashboard"))

    return render_template("admin_page.html")

@admin_bp.route("/engineer")
def engineer_home():

    if not session.get("user_id"):
        return redirect(url_for("auth.login"))
    
    if session.get("role") != "Engineer":
        flash("Access denied")
        return redirect(url_for("main.dashboard"))

    return render_template("engineer_page.html")