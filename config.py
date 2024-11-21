# config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/location_voiture"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'votre_secret_jwt')
