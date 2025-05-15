from src.extensions import db
from src.models.delivery import Delivery
from src.models.purchase import Purchase
from src.models.delivery_provider import DeliveryProvider

def get_all_providers():
    return [p.to_dict() for p in DeliveryProvider.query.all()]

def create_provider(name, contact):
    provider = DeliveryProvider(name=name, contact=contact)
    db.session.add(provider)
    db.session.commit()
    return {"message": "Proveedor registrado", "provider_id": provider.id}, 201

def assign_delivery_to_order(purchase_id, provider_id, user_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return {"error": "Orden no encontrada"}, 404

    if purchase.user_id != user_id:
        return {"error": "No autorizado para esta orden"}, 403

    provider = DeliveryProvider.query.get(provider_id)
    if not provider:
        return {"error": "Proveedor no encontrado"}, 404

    delivery = Delivery(
        purchase_id=purchase.id,
        provider_id=provider.id,
        delivery_type="Standard",
        status="Assigned"
    )

    db.session.add(delivery)
    db.session.commit()

    return {"message": "Entrega asignada exitosamente"}, 201
