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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.String(255), nullable=True)

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
    next_stage_journey = db.Column(db.Text, nullable=True)
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
    approach = db.Column(db.Text, nullable=True)
    mentorship_details = db.Column(db.Text, nullable=True)
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
    approach = db.Column(db.Text, nullable=True)
    mentorship_details = db.Column(db.Text, nullable=True)
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
    profile_image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



# -----------------------------------------------------------------------------
# Event Registration Model
# -----------------------------------------------------------------------------
class EventRegistration(db.Model):
    """
    Represents a user registering for an event.
    """
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    expectation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    event = db.relationship('Event', backref=db.backref('registrations', lazy=True, cascade="all, delete-orphan"))
    member = db.relationship('Member', backref=db.backref('registrations', lazy=True, cascade="all, delete-orphan"))


# -----------------------------------------------------------------------------
# Event Expert Image Model
# -----------------------------------------------------------------------------
class EventExpertImage(db.Model):
    """
    Represents an expert image attached to an event.
    """
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    
    event = db.relationship('Event', backref=db.backref('expert_images', lazy=True, cascade="all, delete-orphan"))

# -----------------------------------------------------------------------------
# Mentorship Request Model
# -----------------------------------------------------------------------------
class MentorshipRequest(db.Model):
    """
    Represents a request for mentorship from a public user.
    """
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    expectation = db.Column(db.Text, nullable=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    founder_id = db.Column(db.Integer, db.ForeignKey('founder.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    member = db.relationship('Member', backref=db.backref('mentorship_requests', lazy=True, cascade="all, delete-orphan"))
    mentor = db.relationship('Mentor', backref=db.backref('requests', lazy=True, cascade="all, delete-orphan"))
    founder = db.relationship('Founder', backref=db.backref('requests', lazy=True, cascade="all, delete-orphan"))

# -----------------------------------------------------------------------------
# Chatbot Message Model
# -----------------------------------------------------------------------------
class ChatbotMessage(db.Model):
    """
    Represents a conversation history with the chatbot.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
