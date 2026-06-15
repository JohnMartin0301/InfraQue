from flask import Blueprint, render_template, session, redirect, url_for, flash
from ..models import Request    
from ..decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return "Home page"

@main_bp.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    total_requests = Request.query.filter_by(user_id=user_id).count()

    pending_requests = Request.query.filter_by(user_id=user_id, status="Pending").count()

    recent_requests = (Request.query.filter_by(user_id=user_id).order_by(Request.created_at.desc()).limit(5).all())

    return render_template("dashboard.html", username=session["username"], role=session["role"], total_requests=total_requests, pending_requests=pending_requests, recent_requests=recent_requests)
