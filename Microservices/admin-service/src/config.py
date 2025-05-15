import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "admin-default-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://auth_user:auth_pass@localhost/authdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
