from flask import Blueprint, jsonify
from src.services.user_admin_service import get_all_users
from src.utils.token_utils import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users(current_user_id, current_user_name):
    users = get_all_users()
    return jsonify(users), 200
