from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .models import User, Locataire, db

auth = Blueprint('auth', __name__)

# Route de connexion (login)
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(message="Nom d’utilisateur et mot de passe sont requis"), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Nom d’utilisateur ou mot de passe incorrect"), 401

# Route d'enregistrement d'un nouvel utilisateur (par un administrateur)
@auth.route('/register', methods=['POST'])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify(message="Accès non autorisé"), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify(message="Nom d’utilisateur, mot de passe et rôle sont requis"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message="Le nom d’utilisateur existe déjà."), 400

    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Utilisateur enregistré avec succès"), 201

# Route d'inscription (pour les locataires uniquement)
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'locataire')  # Default role to locataire if not provided
    adresse = data.get('adresse')  # Ajouter l'adresse pour le locataire

    if not username or not password or not adresse:
        return jsonify(message="Nom d’utilisateur, mot de passe et adresse sont requis"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(message="Le nom d'utilisateur existe déjà."), 400

    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
    db.session.add(new_user)
    db.session.commit()

    # Associer un Locataire à cet utilisateur
    new_locataire = Locataire(nom=username, prenom='', adresse=adresse, user_id=new_user.id)
    db.session.add(new_locataire)
    db.session.commit()

    return jsonify(message="Utilisateur et locataire enregistrés avec succès"), 201

# Route pour afficher le profil de l'utilisateur connecté
@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if user:
        locataire = Locataire.query.filter_by(user_id=user.id).first()  # Obtenir les informations liées au locataire
        if locataire:
            return jsonify({
                'username': user.username,
                'role': user.role,
                'locataire': {
                    'nom': locataire.nom,
                    'prenom': locataire.prenom,
                    'adresse': locataire.adresse
                }
            }), 200
        return jsonify(message="Locataire non trouvé pour cet utilisateur"), 404
    return jsonify(message="Utilisateur non trouvé"), 404

# Route pour mettre à jour le profil de l'utilisateur connecté
@auth.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if not user:
        return jsonify(message="Utilisateur non trouvé"), 404

    data = request.get_json()
    new_password = data.get('password')
    if new_password:
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    return jsonify(message="Profil mis à jour avec succès"), 200

# Route pour se déconnecter
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify(message="Déconnexion réussie")
    unset_jwt_cookies(response)  # Supprime le cookie JWT pour déconnecter l'utilisateur
    return response, 200
