import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "order-default-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://order_user:order_pass@localhost/orderdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
