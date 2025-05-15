from flask import Blueprint, request, jsonify
from src.services.purchase_service import create_purchase
from src.utils.token_utils import token_required
from src.models.purchase import Purchase

purchase_bp = Blueprint("purchase", __name__)

@purchase_bp.route("/<int:book_id>", methods=["POST"])
@token_required
def buy_book(book_id, current_user_id=None, current_user_name=None):
    """
    Creates a purchase for the authenticated user for the specified book ID.
    Expects JSON body with:
    - quantity: int
    - price: float (unit price)

    Returns JSON response with purchase status and purchase_id.
    """
    data = request.get_json()
    response, status = create_purchase(data, current_user_id, book_id)
    return jsonify(response), status

@purchase_bp.route("/<int:purchase_id>", methods=["GET"])
@token_required
def get_purchase(purchase_id, current_user_id=None, current_user_name=None):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Compra no encontrada"}), 404

    if purchase.user_id != current_user_id:
        return jsonify({"error": "No autorizado"}), 403

    return jsonify({
        "purchase_id": purchase.id,
        "total_price": purchase.total_price
    }), 200
