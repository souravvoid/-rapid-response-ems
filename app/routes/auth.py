from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.db import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        # handle form submission
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name", "")
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already exists")
        user = User(email=email, password_hash=generate_password_hash(password), name=name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login_page"))
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Invalid credentials")
        session["user_id"] = user.id
        return redirect(url_for("auth.dashboard_page"))
    return render_template("login.html")


@auth_bp.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name", "")
    if User.query.filter_by(email=email).first():
        return jsonify({"error":"Email exists"}), 400
    user = User(email=email, password_hash=generate_password_hash(password), name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"ok"}), 201

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}), 401
    session["user_id"] = user.id
    return jsonify({"message":"ok","user":{"id":user.id,"email":user.email,"name":user.name}})

@auth_bp.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("dashboard.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
