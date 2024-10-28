# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from .auth import auth as auth_blueprint
from .routes import main as main_blueprint
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app)  # Permettre les requêtes cross-origin
    jwt = JWTManager(app)  # Initialiser JWT pour l’authentification

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, url_prefix='/api')

    return app