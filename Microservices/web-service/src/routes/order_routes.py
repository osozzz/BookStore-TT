from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import os

order_bp = Blueprint("order", __name__)

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:5003")

def get_auth_header():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

@order_bp.route("/buy/<int:book_id>", methods=["POST"])
def buy_book(book_id):
    quantity = request.form.get("quantity")
    price = request.form.get("price")

    if not session.get("token"):
        flash("Debes iniciar sesión para comprar.", "warning")
        return redirect(url_for("auth.login"))

    data = {"quantity": quantity, "price": price}
    headers = get_auth_header()

    try:
        response = requests.post(
            f"{ORDER_SERVICE_URL}/orders/{book_id}",
            json=data,
            headers=headers
        )
        if response.status_code == 302:
            return redirect(response.headers.get("Location"))

        if response.ok:
            return redirect(url_for("order.payment", purchase_id=response.json().get("purchase_id")))

        flash("No se pudo procesar la compra", "danger")
    except Exception as e:
        print("❌ Error en compra:", e)
        flash("Error al contactar el servicio de órdenes", "danger")

    return redirect(url_for("book.catalog"))

@order_bp.route("/payment/<int:purchase_id>", methods=["GET", "POST"])
def payment(purchase_id):
    headers = get_auth_header()

    if request.method == "POST":
        method = request.form.get("method")
        amount = request.form.get("amount")

        data = {"method": method, "amount": amount}
        try:
            response = requests.post(
                f"{ORDER_SERVICE_URL}/payments/{purchase_id}",
                json=data,
                headers=headers
            )
            if response.ok:
                return redirect(url_for("order.delivery", purchase_id=purchase_id))
            flash("Error al procesar pago", "danger")
        except Exception as e:
            print("❌ Error en pago:", e)
            flash("No se pudo contactar el servicio de pagos", "danger")

    # 👇 Este bloque es muy importante
    try:
        response = requests.get(
            f"{ORDER_SERVICE_URL}/orders/{purchase_id}",
            headers=headers
        )
        if response.ok:
            amount = response.json().get("total_price", 0)
        else:
            flash("No se pudo obtener el monto de la compra", "danger")
            amount = 0
    except Exception as e:
        print("❌ Error al obtener monto:", e)
        flash("No se pudo conectar con el servicio de órdenes", "danger")
        amount = 0

    return render_template("payment.html", purchase_id=purchase_id, amount=amount)


@order_bp.route("/deliveries/<int:purchase_id>", methods=["GET", "POST"])
def delivery(purchase_id):
    headers = get_auth_header()

    if request.method == "POST":
        provider_id = request.form.get("provider_id")
        data = {
            "purchase_id": purchase_id,
            "provider_id": provider_id,
            "delivery_type": "Standard"
        }

        try:
            response = requests.post(
                f"{ORDER_SERVICE_URL}/deliveries/assign",
                json=data,
                headers=headers
            )
            if response.ok:
                flash("Entrega asignada correctamente ✅", "success")
                return redirect(url_for("book.catalog"))
            flash("Error al asignar entrega", "danger")
        except Exception as e:
            print("❌ Error en entrega:", e)
            flash("No se pudo contactar el servicio de entregas", "danger")

    try:
        response = requests.get(
            f"{ORDER_SERVICE_URL}/deliveries/providers",
            headers=headers
        )
        providers = response.json().get("providers", []) if response.ok else []
    except Exception as e:
        print("❌ Error al obtener proveedores:", e)
        providers = []

    return render_template("delivery_options.html", providers=providers, purchase_id=purchase_id)
