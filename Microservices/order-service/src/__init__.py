import os
from flask import Flask
from dotenv import load_dotenv
from src.config import Config
from src.extensions import db
from src.routes.purchase_routes import purchase_bp
from src.routes.payment_routes import payment_bp
from src.routes.delivery_routes import delivery_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(purchase_bp, url_prefix="/orders")
    app.register_blueprint(payment_bp, url_prefix="/payments")
    app.register_blueprint(delivery_bp, url_prefix="/deliveries")

    return app
