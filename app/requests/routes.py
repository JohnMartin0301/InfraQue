from flask import Blueprint, render_template, redirect, url_for, session, flash
from ..extensions import db
from ..models import Request
from .forms import RequestForm
from ..decorators import login_required

requests_bp = Blueprint('requests', __name__)

@requests_bp.route("/requests")
@login_required
def my_requests():
    user_requests = Request.query.filter_by(user_id=session["user_id"]).order_by(Request.created_at.desc()).all()
    return render_template("requests/my_requests.html", requests=user_requests)

@requests_bp.route("/requests/new", methods=["GET", "POST"])
@login_required
def create_request():
    form = RequestForm()

    if form.validate_on_submit():
        new_request = Request(
            title=form.title.data,
            request_type=form.request_type.data,
            description=form.description.data,
            user_id=session["user_id"]
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Request created successfully.", "success")
        return redirect(url_for("requests.my_requests"))

    return render_template("requests/create_request.html", form=form)

@requests_bp.route("/requests/<int:request_id>")
@login_required
def request_detail(request_id):
    req = Request.query.get_or_404(request_id)

    if req.user_id != session["user_id"]:
        flash("Access denied. This request does not belong to you.", "danger")
        return redirect(url_for("requests.my_requests"))

    return render_template("requests/request_detail.html", request=req)