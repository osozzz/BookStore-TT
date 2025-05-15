from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import os

auth_bp = Blueprint("auth", __name__)
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5000")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/token", json=data)

        if response.status_code == 200:
            token_data = response.json()
            session["token"] = token_data["token"]
            session["name"] = token_data.get("name")
            session["role"] = token_data.get("role")
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("auth.home"))
        else:
            flash("Credenciales inválidas", "danger")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role": request.form.get("role", "user")
        }
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/register", json=data)

        if response.status_code == 201:
            flash("Registro exitoso, ahora puedes iniciar sesión", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Registro fallido", "danger")

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/")
def home():
    return render_template("home.html", user_name=session.get("name"))
