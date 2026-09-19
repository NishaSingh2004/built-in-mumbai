import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management and flashing
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'buildinmumbai-secret-key-12345'
    
    # PostgreSQL Database Configuration
    # Format: postgresql://username:password@host:port/database_name
    # Defaulting to a local postgres database named 'builtinmumbai'
    db_url = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost/builtinmumbai'
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB max upload size
    
    # Allowed extensions for uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
