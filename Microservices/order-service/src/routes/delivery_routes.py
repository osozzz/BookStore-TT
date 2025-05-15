from flask import Blueprint, request, jsonify
from src.services.delivery_service import (
    get_all_providers,
    create_provider,
    assign_delivery_to_order
)
from src.utils.token_utils import token_required

delivery_bp = Blueprint("delivery", __name__)

@delivery_bp.route("/providers", methods=["GET"])
@token_required
def get_delivery_providers(current_user_id=None, current_user_name=None):
    providers = get_all_providers()
    return jsonify({"providers": providers}), 200

@delivery_bp.route("/assign", methods=["POST"])
@token_required
def assign_delivery(current_user_id=None, current_user_name=None):
    data = request.get_json()
    purchase_id = data.get("purchase_id")
    provider_id = data.get("provider_id")

    if not purchase_id or not provider_id:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    response, status = assign_delivery_to_order(purchase_id, provider_id, current_user_id)
    return jsonify(response), status

@delivery_bp.route("/providers", methods=["POST"])
@token_required
def add_provider(current_user_id=None, current_user_name=None):
    data = request.get_json()
    name = data.get("name")
    contact = data.get("contact")

    if not name or not contact:
        return jsonify({"error": "Faltan datos"}), 400

    response, status = create_provider(name, contact)
    return jsonify(response), status
