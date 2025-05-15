"""
This module initializes the Flask application for the authentication service.
Functions:
    create_app(): Creates and configures the Flask application instance.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from src.config import Config
from src.extensions import db, bcrypt
from src.routes.auth_routes import auth_bp

def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: The configured Flask application instance.
    """
    # Cargar variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
