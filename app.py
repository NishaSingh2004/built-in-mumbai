import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models import db, Admin, Event, Blog, Mentor, Founder, Member

# =============================================================================
# FLASK APPLICATION SETUP & INITIALIZATION
# =============================================================================

# Initialize the Flask application
app = Flask(__name__)
# Load configuration from config.py
app.config.from_object(Config)

# Initialize Database with the Flask app
db.init_app(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize LoginManager for handling admin sessions
login_manager = LoginManager(app)
# Tell login manager which view function handles logins (for unauthorized redirects)
login_manager.login_view = 'admin_login'

# Helper function to check if an uploaded file has an allowed extension
def allowed_file(filename):
    """
    Checks if the filename has an extension that we allow (e.g., .png, .jpg).
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Load user for Flask-Login session management
@login_manager.user_loader
def load_user(user_id):
    """
    Reloads the user object from the user ID stored in the session.
    """
    return Admin.query.get(int(user_id))

# =============================================================================
# PUBLIC FACING ROUTES (WHAT REGULAR VISITORS SEE)
# =============================================================================

@app.route('/')
def index():
    """
    Route: Splash Page
    Purpose: Displays the splash screen landing page (YOUR PEOPLE ARE OUT THERE).
    """
    return render_template('public/index.html')

@app.route('/home')
def public_home():
    """
    Route: Home Page
    Purpose: Displays the main landing page after login.
    """
    return render_template('public/home.html')

@app.route('/events')
def public_events():
    """
    Route: Public Events Page
    Purpose: Fetches all events from the database and displays them to the public.
    """
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('public/events.html', events=events)

@app.route('/about')
def public_about():
    """
    Route: Public About Us Page
    Purpose: Displays the About Us page with the timeline.
    """
    return render_template('public/about.html')

@app.route('/community')
def public_community():
    """
    Route: Public Community Page
    Purpose: Displays the community members mock page.
    """
    return render_template('public/community.html')

@app.route('/blogs')
def public_blogs():
    """
    Route: Public Blogs Page
    Purpose: Fetches all blog posts from the database and displays them to the public.
    """
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('public/blogs.html', blogs=blogs)

@app.route('/mentors')
def public_mentors():
    """
    Route: Public Mentors Page
    Purpose: Fetches all mentors from the database and displays them to the public.
    """
    mentors = Mentor.query.all()
    return render_template('public/mentors.html', mentors=mentors)

@app.route('/founders')
def public_founders():
    """
    Route: Public Founders Page
    Purpose: Fetches all founders from the database and displays them to the public.
    """
    founders = Founder.query.all()
    return render_template('public/founders.html', founders=founders)

@app.route('/login', methods=['GET', 'POST'])
def public_login():
    """
    Route: Public Login
    Purpose: Handles public user login.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        member = Member.query.filter_by(email=email).first()
        
        if member and bcrypt.check_password_hash(member.password_hash, password):
            session['member_id'] = member.id
            session['member_name'] = member.first_name
            return redirect(url_for('public_success'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('public/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def public_signup():
    """
    Route: Public Signup
    Purpose: Handles public user registration.
    """
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_member = Member.query.filter_by(email=email).first()
        if existing_member:
            flash('Email address already exists. Please log in.', 'warning')
            return redirect(url_for('public_login'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_member = Member(first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password)
        db.session.add(new_member)
        db.session.commit()
        
        session['member_id'] = new_member.id
        session['member_name'] = new_member.first_name
        return redirect(url_for('public_success'))
        
    return render_template('public/signup.html')

@app.route('/success')
def public_success():
    """
    Route: Public Success
    Purpose: Displays a success screen after login/signup.
    """
    return render_template('public/success.html')

@app.route('/logout')
def public_logout():
    """
    Route: Public Logout
    Purpose: Logs out the public user.
    """
    session.pop('member_id', None)
    session.pop('member_name', None)
    return redirect(url_for('index'))


# =============================================================================
# ADMIN AUTHENTICATION ROUTES
# =============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Route: Admin Login
    Purpose: Handles displaying the login form (GET) and processing login credentials (POST).
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Look up admin by username
        admin = Admin.query.filter_by(username=username).first()
        
        # Check if admin exists and password matches the hash
        if admin and bcrypt.check_password_hash(admin.password_hash, password):
            login_user(admin)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """
    Route: Admin Logout
    Purpose: Logs the admin out and destroys the session.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """
    Route: Admin Dashboard
    Purpose: Main control panel for the admin, showing summary statistics.
    Requires the admin to be logged in (@login_required).
    """
    stats = {
        'events': Event.query.count(),
        'blogs': Blog.query.count(),
        'mentors': Mentor.query.count(),
        'founders': Founder.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)


# =============================================================================
# ADMIN CRUD: EVENTS
# =============================================================================

@app.route('/admin/events')
@login_required
def manage_events():
    """
    Route: Manage Events
    Purpose: Lists all events so the admin can edit or delete them.
    """
    events = Event.query.all()
    return render_template('admin/manage_events.html', items=events)

@app.route('/admin/event/add', methods=['GET', 'POST'])
@login_required
def add_event():
    """
    Route: Add Event
    Purpose: Handles the form to create a new event and upload its photo.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M') if event_date_str else datetime.utcnow()
        
        # Handle file upload
        file = request.files.get('image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'events', filename))
            
        new_event = Event(title=title, description=description, event_date=event_date, image_filename=filename)
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('manage_events'))
        
    return render_template('admin/form_event.html', action="Add")

@app.route('/admin/event/delete/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    """
    Route: Delete Event
    Purpose: Deletes a specific event from the database based on its ID.
    """
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('manage_events'))


# =============================================================================
# ADMIN CRUD: BLOGS
# =============================================================================


@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    item = Event.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        if event_date_str:
            try:
                item.event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                item.event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M:%S')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'events', filename))
            item.image_filename = filename
            
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('manage_events'))
    return render_template('admin/form_event.html', item=item)
@app.route('/admin/blogs')
@login_required
def manage_blogs():
    """
    Route: Manage Blogs
    Purpose: Lists all blogs so the admin can edit or delete them.
    """
    blogs = Blog.query.all()
    return render_template('admin/manage_blogs.html', items=blogs)

@app.route('/admin/blog/add', methods=['GET', 'POST'])
@login_required
def add_blog():
    """
    Route: Add Blog
    Purpose: Handles the form to create a new blog post and upload its photo.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        
        # Handle file upload
        file = request.files.get('image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'blogs', filename))
            
        new_blog = Blog(title=title, content=content, author=author, image_filename=filename)
        db.session.add(new_blog)
        db.session.commit()
        flash('Blog added successfully!', 'success')
        return redirect(url_for('manage_blogs'))
        
    return render_template('admin/form_blog.html', action="Add")

@app.route('/admin/blog/delete/<int:id>', methods=['POST'])
@login_required
def delete_blog(id):
    """
    Route: Delete Blog
    Purpose: Deletes a specific blog post from the database based on its ID.
    """
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog deleted.', 'success')
    return redirect(url_for('manage_blogs'))


# =============================================================================
# ADMIN CRUD: MENTORS
# =============================================================================


@app.route('/admin/blogs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    item = Blog.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.content = request.form.get('content')
        item.author = request.form.get('author')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'blogs', filename))
            item.image_filename = filename
            
        db.session.commit()
        flash('Blog updated successfully!', 'success')
        return redirect(url_for('manage_blogs'))
    return render_template('admin/form_blog.html', item=item)
@app.route('/admin/mentors')
@login_required
def manage_mentors():
    """
    Route: Manage Mentors
    Purpose: Lists all mentors so the admin can edit or delete them.
    """
    mentors = Mentor.query.all()
    return render_template('admin/manage_mentors.html', items=mentors)

@app.route('/admin/mentor/add', methods=['GET', 'POST'])
@login_required
def add_mentor():
    """
    Route: Add Mentor
    Purpose: Handles the form to add a new mentor and upload their photo.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        expertise = request.form.get('expertise')
        bio = request.form.get('bio')
        
        # Handle file upload
        file = request.files.get('image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'mentors', filename))
            
        new_mentor = Mentor(name=name, expertise=expertise, bio=bio, image_filename=filename)
        db.session.add(new_mentor)
        db.session.commit()
        flash('Mentor added successfully!', 'success')
        return redirect(url_for('manage_mentors'))
        
    return render_template('admin/form_mentor.html', action="Add")

@app.route('/admin/mentor/delete/<int:id>', methods=['POST'])
@login_required
def delete_mentor(id):
    """
    Route: Delete Mentor
    Purpose: Deletes a specific mentor from the database based on their ID.
    """
    mentor = Mentor.query.get_or_404(id)
    db.session.delete(mentor)
    db.session.commit()
    flash('Mentor deleted.', 'success')
    return redirect(url_for('manage_mentors'))


# =============================================================================
# ADMIN CRUD: FOUNDERS
# =============================================================================


@app.route('/admin/mentors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mentor(id):
    item = Mentor.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.expertise = request.form.get('expertise')
        item.bio = request.form.get('bio')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'mentors', filename))
            item.image_filename = filename
            
        db.session.commit()
        flash('Mentor updated successfully!', 'success')
        return redirect(url_for('manage_mentors'))
    return render_template('admin/form_mentor.html', item=item)
@app.route('/admin/founders')
@login_required
def manage_founders():
    """
    Route: Manage Founders
    Purpose: Lists all founders so the admin can edit or delete them.
    """
    founders = Founder.query.all()
    return render_template('admin/manage_founders.html', items=founders)

@app.route('/admin/founder/add', methods=['GET', 'POST'])
@login_required
def add_founder():
    """
    Route: Add Founder
    Purpose: Handles the form to add a new founder and upload their photo.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        bio = request.form.get('bio')
        
        # Handle file upload
        file = request.files.get('image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'founders', filename))
            
        new_founder = Founder(name=name, role=role, bio=bio, image_filename=filename)
        db.session.add(new_founder)
        db.session.commit()
        flash('Founder added successfully!', 'success')
        return redirect(url_for('manage_founders'))
        
    return render_template('admin/form_founder.html', action="Add")

@app.route('/admin/founder/delete/<int:id>', methods=['POST'])
@login_required
def delete_founder(id):
    """
    Route: Delete Founder
    Purpose: Deletes a specific founder from the database based on their ID.
    """
    founder = Founder.query.get_or_404(id)
    db.session.delete(founder)
    db.session.commit()
    flash('Founder deleted.', 'success')
    return redirect(url_for('manage_founders'))

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
if __name__ == '__main__':
    # Run the application in debug mode on port 5000
    app.run(debug=True, port=5000)

@app.route('/admin/founders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_founder(id):
    item = Founder.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.role = request.form.get('role')
        item.bio = request.form.get('bio')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'founders', filename))
            item.image_filename = filename
            
        db.session.commit()
        flash('Founder updated successfully!', 'success')
        return redirect(url_for('manage_founders'))
    return render_template('admin/form_founder.html', item=item)
