"""
Auth Service for handling user registration and authentication.
"""
from src.extensions import db
from src.models.user import User
from src.utils.token_utils import generate_token

def register_user(data):
    """
    Registers a new user with the provided data.
    """
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not all([name, email, password]):
        return {"error": "Faltan campos obligatorios"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "El usuario ya existe"}, 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "Usuario registrado con éxito"}, 201

def authenticate_user(data):
    """
    Authenticates a user with the provided email and password.
    """
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return {"error": "Email y contraseña son requeridos"}, 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = generate_token(user.id, user.name, user.role)
        return {"token": token, "name": user.name, "role": user.role}, 200

    return {"error": "Credenciales inválidas"}, 401
