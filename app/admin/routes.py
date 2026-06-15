from flask import Blueprint, render_template
from ..models import Request, User
from ..decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin-page")
@role_required("Admin")
def admin_home():
    all_requests = Request.query.order_by(Request.created_at.desc())
    all_users = User.query.order_by(User.created_at.desc()).all()

    return render_template("admin_page.html", requests=all_requests, users=all_users)

@admin_bp.route("/engineer")
@role_required("Engineer")
def engineer_home():
    approved_requests = Request.query.filter_by(status="Approved").order_by(Request.created_at.desc()).all()

    return render_template("engineer_page.html", requests=approved_requests)