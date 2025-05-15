import os
from flask import Flask
from dotenv import load_dotenv
from src.config import Config
from src.extensions import db
from src.routes.book_routes import book_bp

def create_app():
    # Cargar variables de entorno
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(book_bp, url_prefix="/catalog")

    return app
