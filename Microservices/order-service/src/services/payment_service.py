from src.extensions import db
from src.models.payment import Payment
from src.models.purchase import Purchase

def process_payment(data, purchase_id):
    required = ["amount", "method", "purchase_id"]
    if not all(k in data for k in required):
        return {"error": "Faltan datos de pago"}, 400

    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return {"error": "Orden no encontrada"}, 404

    payment = Payment(
        purchase_id=purchase.id,
        amount=float(data["amount"]),
        method=data["method"],
        status="Paid"
    )

    purchase.status = "Paid"

    db.session.add(payment)
    db.session.commit()

    return {"message": "Pago registrado con éxito"}, 201
