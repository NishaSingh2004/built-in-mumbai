import os
from app import app
from models import db, Admin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def initialize_database():
    """
    Creates all database tables and inserts a default admin user if none exists.
    Make sure you have created the database in PostgreSQL before running this.
    """
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if an admin user already exists
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            # Default password is 'admin123'
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = Admin(username='admin', password_hash=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
        else:
            print("Admin user already exists.")
            
        print("Database initialization complete.")

if __name__ == '__main__':
    initialize_database()
