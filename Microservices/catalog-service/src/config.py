import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "catalog-default-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://catalog_user:catalog_pass@localhost/catalogdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
