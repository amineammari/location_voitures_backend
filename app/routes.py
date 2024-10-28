# app/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from .models import db, Voiture, Locataire, Location

main = Blueprint('main', __name__)

# CRUD pour Voiture
@main.route('/voitures', methods=['GET'])
@jwt_required()
def list_voitures():
    voitures = Voiture.query.all()
    return jsonify([{
        'id': voiture.id,
        'num_imma': voiture.num_imma,
        'marque': voiture.marque,
        'modele': voiture.modele,
        'kilometrage': voiture.kilometrage,
        'etat': voiture.etat,
        'prix_location': voiture.prix_location
    } for voiture in voitures])

@main.route('/voitures/<int:id>', methods=['GET'])
@jwt_required()
def get_voiture(id):
    voiture = Voiture.query.get_or_404(id)
    return jsonify({
        'id': voiture.id,
        'num_imma': voiture.num_imma,
        'marque': voiture.marque,
        'modele': voiture.modele,
        'kilometrage': voiture.kilometrage,
        'etat': voiture.etat,
        'prix_location': voiture.prix_location
    })

@main.route('/voitures', methods=['POST'])
@jwt_required()
def add_voiture():
    data = request.get_json()
    voiture = Voiture(
        num_imma=data['num_imma'],
        marque=data['marque'],
        modele=data['modele'],
        kilometrage=data['kilometrage'],
        etat='Disponible',
        prix_location=data['prix_location']
    )
    db.session.add(voiture)
    db.session.commit()
    return jsonify(message="Voiture ajoutée avec succès"), 201

@main.route('/voitures/<int:id>', methods=['PUT'])
@jwt_required()
def update_voiture(id):
    voiture = Voiture.query.get_or_404(id)
    data = request.get_json()
    voiture.num_imma = data.get('num_imma', voiture.num_imma)
    voiture.marque = data.get('marque', voiture.marque)
    voiture.modele = data.get('modele', voiture.modele)
    voiture.kilometrage = data.get('kilometrage', voiture.kilometrage)
    voiture.etat = data.get('etat', voiture.etat)
    voiture.prix_location = data.get('prix_location', voiture.prix_location)
    db.session.commit()
    return jsonify(message="Voiture mise à jour avec succès"), 200

@main.route('/voitures/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_voiture(id):
    voiture = Voiture.query.get_or_404(id)
    db.session.delete(voiture)
    db.session.commit()
    return jsonify(message="Voiture supprimée avec succès"), 200


# CRUD pour Locataire
@main.route('/locataires', methods=['GET'])
@jwt_required()
def list_locataires():
    locataires = Locataire.query.order_by(Locataire.nom.asc()).all()
    return jsonify([{
        'id': locataire.id,
        'nom': locataire.nom,
        'prenom': locataire.prenom,
        'adresse': locataire.adresse
    } for locataire in locataires])

@main.route('/locataires/<int:id>', methods=['GET'])
@jwt_required()
def get_locataire(id):
    locataire = Locataire.query.get_or_404(id)
    return jsonify({
        'id': locataire.id,
        'nom': locataire.nom,
        'prenom': locataire.prenom,
        'adresse': locataire.adresse
    })

@main.route('/locataires', methods=['POST'])
@jwt_required()
def add_locataire():
    data = request.get_json()
    locataire = Locataire(
        nom=data['nom'],
        prenom=data['prenom'],
        adresse=data['adresse']
    )
    db.session.add(locataire)
    db.session.commit()
    return jsonify(message="Locataire ajouté avec succès"), 201

@main.route('/locataires/<int:id>', methods=['PUT'])
@jwt_required()
def update_locataire(id):
    locataire = Locataire.query.get_or_404(id)
    data = request.get_json()
    locataire.nom = data.get('nom', locataire.nom)
    locataire.prenom = data.get('prenom', locataire.prenom)
    locataire.adresse = data.get('adresse', locataire.adresse)
    db.session.commit()
    return jsonify(message="Locataire mis à jour avec succès"), 200

@main.route('/locataires/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_locataire(id):
    locataire = Locataire.query.get_or_404(id)
    db.session.delete(locataire)
    db.session.commit()
    return jsonify(message="Locataire supprimé avec succès"), 200


# Gestion des Locations
@main.route('/locations', methods=['POST'])
@jwt_required()
def louer_voiture():
    data = request.get_json()
    voiture_id = data['voiture_id']
    locataire_id = data['locataire_id']
    
    voiture = Voiture.query.get_or_404(voiture_id)
    if voiture.etat != 'Disponible':
        return jsonify(message="Voiture déjà louée"), 400
    
    location = Location(voiture_id=voiture_id, locataire_id=locataire_id)
    voiture.etat = 'En cours de location'
    db.session.add(location)
    db.session.commit()
    return jsonify(message="Voiture louée avec succès"), 201

@main.route('/locations/<int:id>', methods=['GET'])
@jwt_required()
def get_louer(id):
    location = Location.query.get_or_404(id)
    return jsonify({
        'id': location.id,
        'Voiture': location.voiture_id,
        'Locataire': location.locataire_id
    })

@main.route('/locations/<int:id>/retour', methods=['POST'])
@jwt_required()
def rendre_voiture(id):
    location = Location.query.get_or_404(id)
    voiture = Voiture.query.get_or_404(location.voiture_id)
    voiture.etat = 'Disponible'
    db.session.delete(location)
    db.session.commit()
    return jsonify(message="Voiture rendue avec succès"), 200

@main.route('/parc_voitures', methods=['GET'])
@jwt_required()
def etat_parc():
    total_voitures = Voiture.query.count()
    kilometrage_total = db.session.query(db.func.sum(Voiture.kilometrage)).scalar() or 0
    kilometrage_moyen = kilometrage_total / total_voitures if total_voitures > 0 else 0
    return jsonify({
        'nombre_total_voitures': total_voitures,
        'kilometrage_moyen': kilometrage_moyen
    })