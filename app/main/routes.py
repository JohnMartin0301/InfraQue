from flask import Blueprint, render_template, session, redirect, url_for, flash
from ..models import Request    

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return "Home page"

@main_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Access denied. Please login", "danger")
        
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]

    total_requests = Request.query.filter_by(user_id=user_id).count()
    pending_requests = Request.query.filter_by(user_id=user_id, status="Pending").count()

    recent_requests = (Request.query.filter_by(user_id=user_id).order_by(Request.created_at.desc()).limit(5).all())

    return render_template("dashboard.html", username=session["username"], total_requests=total_requests, pending_requests=pending_requests, recent_requests=recent_requests) 

