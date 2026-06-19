from flask import Blueprint, render_template, redirect, url_for, session, flash, request as flask_request, current_app
from .forms import RegisterForm, LoginForm
from ..extensions import db, bcrypt
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role="User"
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/register/admin", methods=["GET", "POST"])
def register_admin():
    # If no admin registration code is set in environment, block access
    if not current_app.config["ADMIN_REGISTRATION_CODE"]:
        flash("Admin registration is not available.", "danger")
        return redirect(url_for("auth.login"))

    # If Admin already exists, this page is permanently closed
    admin_exists = User.query.filter_by(role="Admin").first()
    if admin_exists:
        flash("Setup has already been completed.", "warning")
        return redirect(url_for("auth.login"))

    if flask_request.method == "POST":
        code = flask_request.form.get("code", "").strip()
        username = flask_request.form.get("username", "").strip()
        email = flask_request.form.get("email", "").strip()
        password = flask_request.form.get("password", "").strip()
        confirm_password = flask_request.form.get("confirm_password", "").strip()

        if code != current_app.config["ADMIN_REGISTRATION_CODE"]:
            flash("Invalid registration code.", "danger")
            return render_template("auth/register_admin.html")

        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template("auth/register_admin.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register_admin.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("auth/register_admin.html")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return render_template("auth/register_admin.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return render_template("auth/register_admin.html")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        admin_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role="Admin"
        )
        db.session.add(admin_user)
        db.session.commit()

        flash("Admin account created successfully. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register_admin.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            flash("Login successful.", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))