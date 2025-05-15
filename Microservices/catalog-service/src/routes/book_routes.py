from flask import Blueprint, request, jsonify
from src.services.book_service import (
    get_all_books,
    get_user_books,
    add_book,
    update_book,
    delete_book
)
from src.utils.token_utils import token_required

book_bp = Blueprint("book", __name__)

@book_bp.route("/", methods=["GET"])
def list_all_books():
    books = get_all_books()
    return jsonify(books), 200

@book_bp.route("/my-books", methods=["GET"])
@token_required
def list_user_books(current_user_id, current_user_name):
    books = get_user_books(current_user_id)
    return jsonify(books), 200

@book_bp.route("/", methods=["POST"])
@token_required
def create_book(current_user_id, current_user_name):
    data = request.get_json()
    response, status = add_book(data, current_user_id)
    return jsonify(response), status

@book_bp.route("/<int:book_id>", methods=["PUT"])
@token_required
def edit_book(current_user_id, current_user_name, book_id):
    data = request.get_json()
    response, status = update_book(book_id, data, current_user_id)
    return jsonify(response), status

@book_bp.route("/<int:book_id>", methods=["DELETE"])
@token_required
def remove_book(current_user_id, current_user_name, book_id):
    response, status = delete_book(book_id, current_user_id)
    return jsonify(response), status
