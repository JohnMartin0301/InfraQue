from flask import Blueprint, render_template, flash, redirect, url_for, request as flask_request
from ..models import Request, User, StatusHistory
from ..decorators import role_required
from ..extensions import db
from flask import session

admin_bp = Blueprint('admin', __name__)

ALLOWED_STATUSES = ["Pending", "In Progress", "Approved", "Rejected"]

@admin_bp.route("/admin")
@role_required("Admin")
def admin_dashboard():
    total_users = User.query.count()
    total_requests = Request.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_requests = Request.query.order_by(Request.created_at.desc()).limit(5).all()

    return render_template(
        "admin/admin_dashboard.html",
        total_users=total_users,
        total_requests=total_requests,
        recent_users=recent_users,
        recent_requests=recent_requests
    )

@admin_bp.route("/admin/users")
@role_required("Admin")
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/admin_users.html", users=users)

@admin_bp.route("/admin/requests")
@role_required("Admin")
def admin_requests():
    requests = Request.query.order_by(Request.created_at.desc()).all()
    return render_template("admin/admin_requests.html", requests=requests)

@admin_bp.route("/admin/requests/<int:request_id>")
@role_required("Admin")
def admin_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()

    return render_template(
        "admin/admin_request_detail.html",
        request=req,
        allowed_statuses=ALLOWED_STATUSES,
        history=history
    )

@admin_bp.route("/admin/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Admin")
def update_request_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")

    if new_status not in ALLOWED_STATUSES:
        flash("Invalid status selected.", "danger")
        return redirect(url_for("admin.admin_request_detail", request_id=request_id))

    if new_status == req.status:
        flash("Status is already set to that value.", "warning")
        return redirect(url_for("admin.admin_request_detail", request_id=request_id))

    log = StatusHistory(
        request_id=req.id,
        old_status=req.status,
        new_status=new_status,
        changed_by=session["username"]
    )

    req.status = new_status

    db.session.add(log)
    db.session.commit()

    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(url_for("admin.admin_request_detail", request_id=request_id))

@admin_bp.route("/engineer")
@role_required("Engineer")
def engineer_home():
    approved_requests = Request.query.filter_by(status="Approved").order_by(Request.created_at.desc()).all()
    return render_template("engineer_page.html", requests=approved_requests)

@admin_bp.route("/engineer/requests/<int:request_id>")
@role_required("Engineer")
def engineer_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()

    return render_template(
        "engineer_request_detail.html",
        request=req,
        allowed_statuses=ALLOWED_STATUSES,
        history=history
    )

@admin_bp.route("/engineer/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Engineer")
def engineer_update_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")

    if new_status not in ALLOWED_STATUSES:
        flash("Invalid status selected.", "danger")
        return redirect(url_for("admin.engineer_request_detail", request_id=request_id))

    if new_status == req.status:
        flash("Status is already set to that value.", "warning")
        return redirect(url_for("admin.engineer_request_detail", request_id=request_id))

    log = StatusHistory(
        request_id=req.id,
        old_status=req.status,
        new_status=new_status,
        changed_by=session["username"]
    )

    req.status = new_status

    db.session.add(log)
    db.session.commit()

    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(url_for("admin.engineer_request_detail", request_id=request_id))