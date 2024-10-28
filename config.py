import os
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/location_voiture"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    WT_SECRET_KEY = 'votre_secret_jwt'  # Clé secrète pour JWT