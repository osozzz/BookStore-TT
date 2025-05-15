from src.extensions import db
from src.models.purchase import Purchase

def create_purchase(data, user_id, book_id):
    required = ["quantity", "price"]
    if not all(k in data for k in required):
        return {"error": "Faltan campos obligatorios"}, 400

    quantity = int(data["quantity"])
    price = float(data["price"])
    total = quantity * price

    purchase = Purchase(
        user_id=user_id,
        book_id=book_id,
        quantity=quantity,
        total_price=total,
        status="Pending Payment"
    )

    db.session.add(purchase)
    db.session.commit()

    return {"message": "Compra registrada", "purchase_id": purchase.id}, 201
