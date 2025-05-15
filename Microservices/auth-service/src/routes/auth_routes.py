"""
Auth Service for handling user registration and authentication.
"""
from flask import Blueprint, request, jsonify
from src.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Endpoint for user registration.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de solicitud vacío"}), 400
    response, status = register_user(data)
    return jsonify(response), status

@auth_bp.route("/token", methods=["POST"])
def token():
    """
    Endpoint for user authentication and token generation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de solicitud vacío"}), 400
    response, status = authenticate_user(data)
    return jsonify(response), status
