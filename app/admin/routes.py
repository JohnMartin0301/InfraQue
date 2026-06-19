from flask import Blueprint, render_template, flash, redirect, url_for, request as flask_request, session
from ..models import Request, User, StatusHistory
from ..decorators import role_required, login_required
from ..extensions import db

admin_bp = Blueprint('admin', __name__)

ALLOWED_STATUSES = ["Pending", "Approved", "In Progress", "On Hold", "Completed", "Rejected"]

VALID_TRANSITIONS = {
    "Pending":     ["Approved", "Rejected"],
    "Approved":    ["In Progress", "Rejected", "On Hold"],
    "In Progress": ["Completed", "On Hold"],
    "On Hold":     ["Approved"],
    "Completed":   [],
    "Rejected":    [],
}

ALLOWED_ROLES = ["User", "Manager", "Engineer", "Support", "Viewer", "Admin"]


def apply_status_update(req, new_status, changed_by, redirect_url):
    if new_status not in ALLOWED_STATUSES:
        flash("Invalid status selected.", "danger")
        return redirect(redirect_url)

    if new_status == req.status:
        flash("Status is already set to that value.", "warning")
        return redirect(redirect_url)

    allowed_next = VALID_TRANSITIONS.get(req.status, [])
    if new_status not in allowed_next:
        flash(f"Invalid transition: '{req.status}' cannot move to '{new_status}'.", "danger")
        return redirect(redirect_url)

    log = StatusHistory(
        request_id=req.id,
        old_status=req.status,
        new_status=new_status,
        changed_by=changed_by
    )
    req.status = new_status
    db.session.add(log)
    db.session.commit()

    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(redirect_url)


def get_role_allowed_transitions(current_status, role):
    all_transitions = VALID_TRANSITIONS.get(current_status, [])

    if role == "Admin":
        return all_transitions

    if role == "Manager":
        return [s for s in all_transitions if s in ["Approved", "Rejected"]]

    if role == "Engineer":
        return [s for s in all_transitions if s in ["In Progress", "Completed"]]

    if role == "Support":
        return [s for s in all_transitions if s in ["On Hold", "Approved"]]

    return []


# ─── Admin Routes ─────────────────────────────────────────────────────────────

@admin_bp.route("/admin-dashboad")
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

@admin_bp.route("/admin/users/<int:user_id>/update-role", methods=["POST"])
@role_required("Admin")
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = flask_request.form.get("role")

    if new_role not in ALLOWED_ROLES:
        flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.admin_users"))

    if user.role == new_role:
        flash("User already has that role.", "warning")
        return redirect(url_for("admin.admin_users"))

    user.role = new_role
    db.session.commit()

    flash(f"{user.username} has been assigned the {new_role} role.", "success")
    return redirect(url_for("admin.admin_users"))

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
    allowed_next = get_role_allowed_transitions(req.status, "Admin")

    return render_template(
        "admin/admin_request_detail.html",
        request=req,
        allowed_next=allowed_next,
        history=history
    )

@admin_bp.route("/admin/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Admin")
def update_request_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")
    redirect_url = url_for("admin.admin_request_detail", request_id=request_id)
    return apply_status_update(req, new_status, session["username"], redirect_url)


# ─── Engineer Routes ───────────────────────────────────────────────────────────

@admin_bp.route("/engineer")
@role_required("Engineer")
def engineer_home():
    approved_requests = Request.query.filter_by(status="Approved").order_by(Request.created_at.desc()).all()
    return render_template("engineer/engineer_page.html", requests=approved_requests)

@admin_bp.route("/engineer/requests/<int:request_id>")
@role_required("Engineer")
def engineer_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()
    allowed_next = get_role_allowed_transitions(req.status, "Engineer")

    return render_template(
        "engineer/engineer_request_detail.html",
        request=req,
        allowed_next=allowed_next,
        history=history
    )

@admin_bp.route("/engineer/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Engineer")
def engineer_update_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")
    redirect_url = url_for("admin.engineer_request_detail", request_id=request_id)
    return apply_status_update(req, new_status, session["username"], redirect_url)


# ─── Manager Routes ────────────────────────────────────────────────────────────

@admin_bp.route("/manager")
@role_required("Manager")
def manager_home():
    pending_requests = Request.query.filter_by(status="Pending").order_by(Request.created_at.desc()).all()
    return render_template("manager/manager_page.html", requests=pending_requests)

@admin_bp.route("/manager/requests/<int:request_id>")
@role_required("Manager")
def manager_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()
    allowed_next = get_role_allowed_transitions(req.status, "Manager")

    return render_template(
        "manager/manager_request_detail.html",
        request=req,
        allowed_next=allowed_next,
        history=history
    )

@admin_bp.route("/manager/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Manager")
def manager_update_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")
    redirect_url = url_for("admin.manager_request_detail", request_id=request_id)
    return apply_status_update(req, new_status, session["username"], redirect_url)


# ─── Viewer Routes ─────────────────────────────────────────────────────────────

@admin_bp.route("/viewer")
@role_required("Viewer")
def viewer_home():
    requests = Request.query.order_by(Request.created_at.desc()).all()
    return render_template("viewer/viewer_page.html", requests=requests)

@admin_bp.route("/viewer/requests/<int:request_id>")
@role_required("Viewer")
def viewer_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()

    return render_template(
        "viewer/viewer_request_detail.html",
        request=req,
        history=history
    )


# ─── Support Routes ────────────────────────────────────────────────────────────

@admin_bp.route("/support")
@role_required("Support")
def support_home():
    requests = Request.query.filter(
        Request.status.in_(["Approved", "In Progress", "On Hold"])
    ).order_by(Request.created_at.desc()).all()
    return render_template("support/support_page.html", requests=requests)

@admin_bp.route("/support/requests/<int:request_id>")
@role_required("Support")
def support_request_detail(request_id):
    req = Request.query.get_or_404(request_id)
    history = StatusHistory.query.filter_by(request_id=request_id).order_by(StatusHistory.changed_at.desc()).all()
    allowed_next = get_role_allowed_transitions(req.status, "Support")

    return render_template(
        "support/support_request_detail.html",
        request=req,
        allowed_next=allowed_next,
        history=history
    )

@admin_bp.route("/support/requests/<int:request_id>/update-status", methods=["POST"])
@role_required("Support")
def support_update_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = flask_request.form.get("status")
    redirect_url = url_for("admin.support_request_detail", request_id=request_id)
    return apply_status_update(req, new_status, session["username"], redirect_url)