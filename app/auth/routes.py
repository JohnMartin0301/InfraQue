from flask import Blueprint, request, render_template, redirect, url_for, session, flash
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
            flash("Username already exists", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("auth.register"))
            
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(username=username, email=email, password_hash=hashed_password, role="User")

        db.session.add(user)
        db.session.commit()

        flash("Registration successful", "success")

        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)

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

            flash ("Login successful", "success")

            return redirect(url_for("main.dashboard"))
        
        flash("Invalid credentials", "danger")
    
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()

    flash("Logout successful", "success")

    return redirect(url_for("auth.login"))