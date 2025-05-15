"""
Configuration module for the authentication service.

This module defines the `Config` class, which provides configuration
settings for the application, such as secret keys and database connection
details.
"""
import os

class Config:
    """
    Configuration class for the application, providing default settings
    and environment variable overrides for sensitive data and database connection.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://user:pass@localhost/bookstore"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
