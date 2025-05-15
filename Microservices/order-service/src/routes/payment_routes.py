from flask import Blueprint, request, jsonify
from src.services.payment_service import process_payment
from src.utils.token_utils import token_required

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/<int:purchase_id>", methods=["POST"])
@token_required
def pay(purchase_id, current_user_id=None, current_user_name=None):
    data = request.get_json()
    data["purchase_id"] = purchase_id

    response, status = process_payment(data, current_user_id)
    return jsonify(response), status
