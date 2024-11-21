from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Enum, CheckConstraint
import enum

db = SQLAlchemy()

# Enum pour les rôles d'utilisateur
class RoleEnum(enum.Enum):
    admin = "admin"
    locataire = "locataire"

# Modèle pour les utilisateurs
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)  # Utilisation de l'énumération pour les rôles
    
    # Relation avec Locataire (un utilisateur peut être un locataire)
    locataire = db.relationship('Locataire', backref='user', uselist=False)

# Modèle pour les voitures
class Voiture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_imma = db.Column(db.Integer, unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    kilometrage = db.Column(db.Integer, nullable=False)
    etat = db.Column(db.String(20), nullable=False)  # Disponible ou En cours de location
    prix_location = db.Column(db.Float, nullable=False)

# Modèle pour les locataires
class Locataire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers User

    # Relation avec User
    user = db.relationship('User', back_populates='locataire')

    # Relation avec les voitures via la table Location
    voitures = db.relationship('Voiture', secondary='location', backref='locataires')

# Modèle pour les locations
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voiture_id = db.Column(db.Integer, db.ForeignKey('voiture.id'), nullable=False)
    locataire_id = db.Column(db.Integer, db.ForeignKey('locataire.id'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    prix_total = db.Column(db.Float, nullable=False)

    # Contraintes sur la validité des dates
    __table_args__ = (
        CheckConstraint('date_debut < date_fin', name='check_date_debut_fin'),
    )
    
    # Relations avec Voiture et Locataire
    voiture = db.relationship('Voiture', backref='locations')
    locataire = db.relationship('Locataire', backref='locations')

