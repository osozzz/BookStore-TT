"""
This module initializes and provides extensions for the Flask application, 
including SQLAlchemy for database interactions and Bcrypt for password hashing.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
