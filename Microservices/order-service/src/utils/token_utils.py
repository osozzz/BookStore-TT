import jwt
import os
from flask import request, jsonify
from functools import wraps

# Clave secreta para decodificar el JWT
SECRET_KEY = os.getenv("SECRET_KEY", "order-default-secret")

def token_required(f):
    """
    Decorador que verifica la validez de un token JWT en la cabecera Authorization.
    Agrega los datos del usuario autenticado a kwargs para que puedan ser usados en la función decorada.

    Uso:
        @token_required
        def ruta(purchase_id, current_user_id=None, current_user_name=None):
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtener token de la cabecera Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            # Decodificar token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            kwargs["current_user_id"] = data["id"]
            kwargs["current_user_name"] = data["name"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated
