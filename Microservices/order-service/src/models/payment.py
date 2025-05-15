from src.extensions import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchases.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Pending")

    def to_dict(self):
        return {
            "id": self.id,
            "purchase_id": self.purchase_id,
            "amount": self.amount,
            "method": self.method,
            "status": self.status
        }
