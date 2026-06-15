from flask import Blueprint, render_template, flash, redirect, url_for
from ..models import Request, User
from ..decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin")
@role_required("Admin")
def admin_dashboard():
    total_users = User.query.count()
    total_requests = Request.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_requests = Request.query.order_by(Request.created_at.desc()).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_requests=total_requests,
        recent_users=recent_users,
        recent_requests=recent_requests
    )

@admin_bp.route("/admin/users")
@role_required("Admin")
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users)

@admin_bp.route("/admin/requests")
@role_required("Admin")
def admin_requests():
    requests = Request.query.order_by(Request.created_at.desc()).all()
    return render_template("admin_requests.html", requests=requests)

@admin_bp.route("/requests/<int:request_id>")
@role_required("Admin")
def admin_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    return render_template("admin_request_detail.html", request=req)

@admin_bp.route("/engineer")
@role_required("Engineer")
def engineer_home():
    approved_requests = Request.query.filter_by(status="Approved").order_by(Request.created_at.desc()).all()
    return render_template("engineer_page.html", requests=approved_requests)