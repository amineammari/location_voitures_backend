# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' ou 'locataire'

class Voiture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_imma = db.Column(db.Integer, unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    kilometrage = db.Column(db.Integer, nullable=False)
    etat = db.Column(db.String(20), nullable=False)  # Disponible ou En cours de location
    prix_location = db.Column(db.Float, nullable=False)

class Locataire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    voitures = db.relationship('Voiture', secondary='location')

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voiture_id = db.Column(db.Integer, db.ForeignKey('voiture.id'), nullable=False)
    locataire_id = db.Column(db.Integer, db.ForeignKey('locataire.id'), nullable=False)