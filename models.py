from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy with no app bounded yet. We'll bind it in app.py
db = SQLAlchemy()

# -----------------------------------------------------------------------------
# Admin Model
# -----------------------------------------------------------------------------
class Admin(db.Model, UserMixin):
    """
    Represents the administrator for the backend.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# -----------------------------------------------------------------------------
# Event Model
# -----------------------------------------------------------------------------
class Event(db.Model):
    """
    Represents an event published on the website.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_filename = db.Column(db.String(255), nullable=True) # Path to the uploaded photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------------------------------------------------------
# Blog Model
# -----------------------------------------------------------------------------
class Blog(db.Model):
    """
    Represents a blog post published on the website.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True) # Path to the uploaded photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------------------------------------------------------
# Mentor Model
# -----------------------------------------------------------------------------
class Mentor(db.Model):
    """
    Represents a mentor listed on the website.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expertise = db.Column(db.String(150), nullable=False) # e.g., "Software Engineering", "Marketing"
    bio = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True) # Path to the uploaded photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------------------------------------------------------
# Founder Model
# -----------------------------------------------------------------------------
class Founder(db.Model):
    """
    Represents a founder of the 'Built in Mumbai' organization.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False) # e.g., "Co-Founder & CEO"
    bio = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True) # Path to the uploaded photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------------------------------------------------------
# Member Model (Public User)
# -----------------------------------------------------------------------------
class Member(db.Model):
    """
    Represents a public user who signed up on the website.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

