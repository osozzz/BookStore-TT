from src.extensions import db

class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)       # Viene del JWT
    book_id = db.Column(db.Integer, nullable=False)       # Enviado desde el cliente
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending Payment")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "status": self.status
        }
