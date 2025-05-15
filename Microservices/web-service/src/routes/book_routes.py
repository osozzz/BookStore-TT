from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import os

book_bp = Blueprint("book", __name__)
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:5001/catalog")

def get_auth_header():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

@book_bp.route("/catalog")
def catalog():
    response = requests.get(f"{CATALOG_SERVICE_URL}/")
    books = response.json() if response.ok else []
    return render_template("catalog.html", books=books)

@book_bp.route("/my_books")
def my_books():
    token = session.get("token")
    if not token:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for("auth.login"))

    headers = get_auth_header()
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/my-books", headers=headers)

        if response.status_code == 200:
            books = response.json()
        else:
            flash(f"Error al obtener tus libros: {response.status_code}", "danger")
            print("⚠️ Respuesta no 200:", response.status_code, response.text)
            books = []

    except Exception as e:
        print("❌ Error en my_books:", str(e))
        flash("No se pudo conectar con el servicio de catálogo.", "danger")
        books = []

    user_name = session.get("name")
    return render_template("my_books.html", books=books, user_name=user_name)

@book_bp.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "description": request.form.get("description"),
            "price": request.form.get("price"),
            "stock": request.form.get("stock")
        }
        response = requests.post(f"{CATALOG_SERVICE_URL}/", json=data, headers=get_auth_header())

        if response.status_code != 201:
            flash("Error al agregar libro", "danger")
            print("❌ Error al agregar libro:", response.status_code, response.text)
            return render_template("add_book.html", user_name=session.get("name"))

        return redirect(url_for("book.my_books"))

    return render_template("add_book.html", user_name=session.get("name"))

@book_bp.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if request.method == "POST":
        data = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "description": request.form.get("description"),
            "price": request.form.get("price"),
            "stock": request.form.get("stock")
        }
        response = requests.put(f"{CATALOG_SERVICE_URL}/{book_id}", json=data, headers=get_auth_header())
        if response.status_code != 200:
            flash("Error al editar libro", "danger")
            print("❌ Error editando libro:", response.status_code, response.text)
        return redirect(url_for("book.my_books"))

    response = requests.get(f"{CATALOG_SERVICE_URL}/{book_id}", headers=get_auth_header())
    book = response.json() if response.ok else {}
    return render_template("edit_book.html", book=book, user_name=session.get("name"))

@book_bp.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    response = requests.delete(f"{CATALOG_SERVICE_URL}/{book_id}", headers=get_auth_header())
    if response.status_code != 200:
        flash("Error al eliminar libro", "danger")
        print("❌ Error eliminando libro:", response.status_code, response.text)
    return redirect(url_for("book.my_books"))
