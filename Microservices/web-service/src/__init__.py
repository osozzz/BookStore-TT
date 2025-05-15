import os
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv

from src.routes.auth_routes import auth_bp
from src.routes.book_routes import book_bp
from src.routes.order_routes import order_bp
from src.routes.admin_routes import admin_bp

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder="../templates")

    app.secret_key = os.getenv("SECRET_KEY", "web-secret")

    # Configuración de sesión usando cookies (o filesystem si prefieres)
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

    return app
