from app import create_app, db  # Import your app creation function and db instance
from app.models import User
from werkzeug.security import generate_password_hash

def add_user(username, password, role):
    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        print("Le nom d’utilisateur existe déjà.")
        return

    # Use pbkdf2:sha256 as the hash method
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    # Create a new user
    new_user = User(username=username, password=hashed_password, role=role)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    print("Utilisateur enregistré avec succès")

# Create an application context
app = create_app()  # Ensure create_app() returns your Flask app instance
with app.app_context():
    add_user("amin", "Alihanen1@11643771", "admin")