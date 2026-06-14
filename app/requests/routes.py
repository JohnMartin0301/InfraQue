from flask import Blueprint, render_template, redirect, url_for, session, flash
from ..extensions import db
from ..models import Request
from .forms import RequestForm

requests_bp = Blueprint('requests', __name__)

@requests_bp.route("/requests")
def my_requests():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_requests = Request.query.filter_by(user_id=session["user_id"]).all()

    return render_template("my_requests.html", requests=user_requests)

@requests_bp.route("/requests/new", methods=["GET", "POST"])
def create_request():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    form = RequestForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        new_request = Request(title=title, description=description, user_id=session["user_id"])

        db.session.add(new_request)
        db.session.commit()

        flash("Request created successfully", "success")
        return redirect(url_for("requests.my_requests"))
    
    return render_template("create_request.html", form=form)

@requests_bp.route("/requests/<int:request_id>")
def request_detail(request_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    req = Request.query.get_or_404(request_id)

    if req.user_id != session["user_id"]:
        flash("Access denied", "danger")
        return redirect(url_for("requests.my_requests"))
    
    return render_template("request_detail.html", request=req)