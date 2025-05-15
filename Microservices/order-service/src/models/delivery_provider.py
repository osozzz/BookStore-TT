from src.extensions import db

class DeliveryProvider(db.Model):
    __tablename__ = "delivery_providers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(150), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact": self.contact
        }

