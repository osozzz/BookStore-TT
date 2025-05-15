from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import os

admin_bp = Blueprint("admin", __name__)
ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL", "http://localhost:5003")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:5003")

def get_auth_header():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

@admin_bp.route("/admin/users")
def list_users():
    if session.get("role") != "admin":
        flash("Acceso denegado. Solo administradores.", "danger")
        return redirect(url_for("auth.home"))

    response = requests.get(f"{ADMIN_SERVICE_URL}/admin/users", headers=get_auth_header())

    if response.status_code == 200:
        users = response.json()
        return render_template("list_users.html", users=users)

    flash("Error al cargar usuarios", "danger")
    return redirect(url_for("auth.home"))

@admin_bp.route("/admin/create_user", methods=["GET", "POST"])
def create_user():
    if session.get("role") != "admin":
        flash("Acceso denegado. Solo administradores.", "danger")
        return redirect(url_for("auth.home"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role": "admin"
        }

        response = requests.post(f"{ADMIN_SERVICE_URL}/admin/create_user", json=data, headers=get_auth_header())

        if response.status_code == 201:
            flash("Usuario administrador creado exitosamente ✅", "success")
            return redirect(url_for("admin.list_users"))
        else:
            flash("Error al crear usuario", "danger")

    return render_template("create_user.html")

@admin_bp.route("/admin/add_provider", methods=["GET", "POST"])
def add_provider():
    if session.get("role") != "admin":
        flash("Acceso denegado. Solo administradores.", "danger")
        return redirect(url_for("auth.home"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "contact": request.form.get("contact")
        }

        response = requests.post(f"{ORDER_SERVICE_URL}/deliveries/providers", json=data, headers=get_auth_header())

        if response.status_code == 201:
            flash("Proveedor registrado ✅", "success")
            return redirect(url_for("admin.add_provider"))
        else:
            flash("Error al registrar proveedor", "danger")

    return render_template("add_provider.html")
