from flask import Blueprint, render_template, session, redirect, url_for
from ..models import Request, User
from ..decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("main/home.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]

    total_requests = Request.query.filter_by(user_id=user_id).count()
    pending_requests = Request.query.filter_by(user_id=user_id, status="Pending").count()
    approved_requests = Request.query.filter_by(user_id=user_id, status="Approved").count()
    in_progress_requests = Request.query.filter_by(user_id=user_id, status="In Progress").count()
    completed_requests = Request.query.filter_by(user_id=user_id, status="Completed").count()

    recent_requests = (
        Request.query
        .filter_by(user_id=user_id)
        .order_by(Request.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "main/dashboard.html",
        username=session["username"],
        role=session["role"],
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        in_progress_requests=in_progress_requests,
        completed_requests=completed_requests,
        recent_requests=recent_requests
    )

@main_bp.route("/profile")
@login_required
def profile():
    user = User.query.get_or_404(session["user_id"])
    return render_template("main/profile.html", user=user)


@main_bp.route("/test-admin")
def test_admin():
    from flask import current_app
    rules = [str(rule) for rule in current_app.url_map.iter_rules()]
    return "<br>".join(rules)