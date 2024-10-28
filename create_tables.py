# create_tables.py
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables créées avec succès dans la base de données.")