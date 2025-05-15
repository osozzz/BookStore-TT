import jwt
import os
from flask import request, jsonify
from functools import wraps

SECRET_KEY = os.getenv("SECRET_KEY", "catalog-default-secret")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtener token del header Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["id"]
            current_user_name = data["name"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        # Pasamos user_id y user_name a la función decorada
        return f(current_user_id, current_user_name, *args, **kwargs)

    return decorated
