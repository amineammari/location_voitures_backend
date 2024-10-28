from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Nom d’utilisateur ou mot de passe incorrect"), 401

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

    if User.query.filter_by(username=username).first():
        return jsonify(message="Le nom d’utilisateur existe déjà."), 400

    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Utilisateur enregistré avec succès"), 201

@auth.route('/signup',methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    if User.query.filter_by(username=username).first():
        return jsonify(message="Le nom d'utilisteur existe déjà."), 400
    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), role='locataire')
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Utilisateur enregistré avec succès"), 201

@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if user:
        return jsonify({
            'username': user.username,
            'role': user.role
        }), 200
    return jsonify(message="Utilisateur non trouvé"), 404

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

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify(message="Déconnexion réussie")
    unset_jwt_cookies(response)  # Supprime le cookie JWT pour déconnecter l'utilisateur
    return response, 200
