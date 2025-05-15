from src import create_app
from src.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas en authdb.")
