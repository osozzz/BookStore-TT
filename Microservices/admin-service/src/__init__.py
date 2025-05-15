import os
from flask import Flask
from dotenv import load_dotenv
from src.config import Config
from src.extensions import db
from src.routes.user_admin_routes import admin_bp

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
