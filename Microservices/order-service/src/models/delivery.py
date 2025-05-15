from src.extensions import db

class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchases.id"), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey("delivery_providers.id"), nullable=False)
    delivery_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="Pending")

    provider = db.relationship("DeliveryProvider", backref="deliveries")

    def to_dict(self):
        return {
            "id": self.id,
            "purchase_id": self.purchase_id,
            "provider": self.provider.name if self.provider else None,
            "delivery_type": self.delivery_type,
            "status": self.status
        }
