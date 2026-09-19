import os
from datetime import datetime
from werkzeug.utils import secure_filename
from fpdf import FPDF
from io import BytesIO
from flask import Flask, make_response, render_template, request, redirect, url_for, flash, abort, session
from functools import wraps

def permission_required(section):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('admin_login'))
            if current_user.is_superadmin:
                return f(*args, **kwargs)
            if not current_user.permissions or section not in current_user.permissions.split(','):
                flash('You do not have permission to access this section.', 'danger')
                return redirect(url_for('admin_dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models import db, Admin, Event, Blog, Mentor, Founder, Member, EventRegistration, EventExpertImage, MentorshipRequest, ChatbotMessage

# =============================================================================
# FLASK APPLICATION SETUP & INITIALIZATION
# =============================================================================

# Initialize the Flask application
basedir_app = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir_app, 'templates'), static_folder=os.path.join(basedir_app, 'static'))
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
    Purpose: Fetches all founders and mentors to display on the community page.
    """
    founders = Founder.query.all()
    mentors = Mentor.query.all()
    return render_template('public/community.html', founders=founders, mentors=mentors)

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
            session['member_photo'] = member.profile_image_filename
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
        session['member_photo'] = None
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
# PUBLIC DETAIL ROUTES
# =============================================================================

import urllib.parse

@app.route('/event/<int:id>')
def public_event_detail(id):
    item = Event.query.get_or_404(id)
    is_registered = False
    if 'member_id' in session:
        reg = EventRegistration.query.filter_by(event_id=id, member_id=session['member_id']).first()
        if reg:
            is_registered = True
            
    # Generate Google Calendar link
    title = urllib.parse.quote(item.title)
    details = urllib.parse.quote(item.description)
    # Format dates as YYYYMMDDTHHMMSSZ. Assuming UTC for simplicity.
    start_str = item.event_date.strftime('%Y%m%dT%H%M%SZ') if item.event_date else ''
    # Assume 2 hour duration
    import datetime as dt
    end_date = item.event_date + dt.timedelta(hours=2) if item.event_date else None
    end_str = end_date.strftime('%Y%m%dT%H%M%SZ') if end_date else ''
    gcal_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={title}&dates={start_str}/{end_str}&details={details}&location=Mumbai"
    
    return render_template('public/event_detail.html', item=item, is_registered=is_registered, gcal_link=gcal_link)

@app.route('/event/<int:id>/register', methods=['POST'])
def register_for_event(id):
    if 'member_id' not in session:
        flash('You must be logged in to register for events.', 'warning')
        return redirect(url_for('public_login'))
        
    item = Event.query.get_or_404(id)
    reg = EventRegistration.query.filter_by(event_id=id, member_id=session['member_id']).first()
    if not reg:
        expectation = request.form.get('expectation', '')
        new_reg = EventRegistration(event_id=id, member_id=session['member_id'], expectation=expectation)
        db.session.add(new_reg)
        db.session.commit()
        flash('Successfully registered for the event!', 'success')
        
    return redirect(url_for('public_event_detail', id=id))

# Admin view for registrations
@app.route('/admin/event/<int:id>/registrations')
@permission_required('events')
def admin_event_registrations(id):
    event = Event.query.get_or_404(id)
    registrations = EventRegistration.query.filter_by(event_id=id).all()
    return render_template('admin/event_registrations.html', event=event, registrations=registrations)


@app.route('/blog/<int:id>')
def public_blog_detail(id):
    item = Blog.query.get_or_404(id)
    return render_template('public/blog_detail.html', item=item)

@app.route('/mentor/<int:id>', methods=['GET', 'POST'])
def public_mentor_detail(id):
    item = Mentor.query.get_or_404(id)
    if request.method == 'POST':
        if 'member_id' not in session:
            flash('Please log in to request mentorship.', 'warning')
            return redirect(url_for('public_login'))
        why = request.form.get('why_connect', '')
        what_working = request.form.get('what_working', '')
        what_help = request.form.get('what_help', '')
        msg = f"WHY DO YOU WANT TO CONNECT?\n{why}\n\nWHAT ARE YOU WORKING ON?\n{what_working}\n\nWHAT WOULD YOU LIKE HELP WITH?\n{what_help}"
        req = MentorshipRequest(member_id=session['member_id'], mentor_id=id, message=msg)
        db.session.add(req)
        db.session.commit()
        flash('Mentorship request sent successfully!', 'success')
        return redirect(url_for('public_mentor_detail', id=id))
    return render_template('public/mentor_detail.html', item=item)

@app.route('/founder/<int:id>', methods=['GET', 'POST'])
def public_founder_detail(id):
    item = Founder.query.get_or_404(id)
    if request.method == 'POST':
        if 'member_id' not in session:
            flash('Please log in to request mentorship.', 'warning')
            return redirect(url_for('public_login'))
        why = request.form.get('why_connect', '')
        what_working = request.form.get('what_working', '')
        what_help = request.form.get('what_help', '')
        msg = f"WHY DO YOU WANT TO CONNECT?\n{why}\n\nWHAT ARE YOU WORKING ON?\n{what_working}\n\nWHAT WOULD YOU LIKE HELP WITH?\n{what_help}"
        req = MentorshipRequest(member_id=session['member_id'], founder_id=id, message=msg)
        db.session.add(req)
        db.session.commit()
        flash('Mentorship request sent successfully!', 'success')
        return redirect(url_for('public_founder_detail', id=id))
    return render_template('public/founder_detail.html', item=item)

# =============================================================================


@app.route('/profile', methods=['GET', 'POST'])
def public_profile():
    if 'member_id' not in session:
        return redirect(url_for('public_login'))
        
    member = Member.query.get(session['member_id'])
    
    if request.method == 'POST':
        member.first_name = request.form.get('first_name')
        member.last_name = request.form.get('last_name')
        member.email = request.form.get('email')
        
        # Handle file upload
        file = request.files.get('profile_image')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Ensure unique filename
                filename = f"{datetime.utcnow().strftime('%Y%md%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                member.profile_image_filename = filename
                session['member_photo'] = filename
        
        db.session.commit()
        session['member_name'] = member.first_name
        session['member_photo'] = member.profile_image_filename
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('public_profile'))
        
    return render_template('public/profile.html', member=member)

@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    if 'member_id' not in session:
        return redirect(url_for('public_login'))
        
    member = Member.query.get(session['member_id'])
    if member:
        # Delete related registrations and requests
        EventRegistration.query.filter_by(member_id=member.id).delete()
        MentorshipRequest.query.filter_by(member_id=member.id).delete()
        db.session.delete(member)
        db.session.commit()
        
    session.pop('member_id', None)
    session.pop('member_name', None)
    flash('Your account has been completely deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/mentorship_requests')
@permission_required('mentorship_requests')
def manage_mentorship_requests():
    requests = MentorshipRequest.query.order_by(MentorshipRequest.created_at.desc()).all()
    return render_template('admin/manage_mentorship_requests.html', items=requests)


@app.route('/admin/members')
@permission_required('members')
def manage_members():
    members = Member.query.order_by(Member.created_at.desc()).all()
    return render_template('admin/manage_members.html', items=members)


@app.route('/admin/mentorship_requests/export')
@permission_required('mentorship_requests')
def export_mentorship_requests():
    requests = MentorshipRequest.query.order_by(MentorshipRequest.created_at.desc()).all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "Mentorship Requests Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("helvetica", size=10)
    for req in requests:
        expert = f"Mentor: {req.mentor.name}" if req.mentor else f"Founder: {req.founder.name}"
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 8, f"Requested By: {req.member.first_name} {req.member.last_name} ({req.member.email})", ln=True)
        pdf.cell(0, 8, f"Expert: {expert} | Date: {req.created_at.strftime('%Y-%m-%d')}", ln=True)
        pdf.set_font("helvetica", size=10)
        # Handle multi-line message
        pdf.multi_cell(0, 6, f"Message:\n{req.message}")
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
    response = make_response(bytes(pdf.output()))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=mentorship_requests.pdf'
    return response

@app.route('/admin/event/<int:id>/registrations/export')
@permission_required('events')
def export_event_registrations(id):
    event = Event.query.get_or_404(id)
    registrations = EventRegistration.query.filter_by(event_id=id).order_by(EventRegistration.created_at.desc()).all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, f"Registrations: {event.title}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("helvetica", size=10)
    for reg in registrations:
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 8, f"Name: {reg.member.first_name} {reg.member.last_name}", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 6, f"Email: {reg.member.email}")
        pdf.ln(6)
        if reg.expectation:
            pdf.multi_cell(0, 6, f"Expectation: {reg.expectation}")
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
    response = make_response(bytes(pdf.output()))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=event_registrations_{event.id}.pdf'
    return response

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
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Look up admin by email
        admin = Admin.query.filter_by(email=email).first()
        
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
@permission_required('events')
def manage_events():
    """
    Route: Manage Events
    Purpose: Lists all events so the admin can edit or delete them.
    """
    events = Event.query.all()
    return render_template('admin/manage_events.html', items=events)

@app.route('/admin/event/add', methods=['GET', 'POST'])
@permission_required('events')
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
            
        new_event = Event(title=title, description=description, event_date=event_date, image_filename=filename, next_stage_journey=request.form.get('next_stage_journey'))
        db.session.add(new_event)

        for i in range(1, 6):
            exp_file = request.files.get(f'expert_image_{i}')
            if exp_file and exp_file.filename != '':
                exp_filename = secure_filename(exp_file.filename)
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)
                exp_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'events', exp_filename))
                # For add_event, the new_event needs to be added to db first to get an ID.
                # Actually, adding objects to relationship works even without ID!
                exp_img = EventExpertImage(image_filename=exp_filename)
                new_event.expert_images.append(exp_img)

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
        item.next_stage_journey = request.form.get('next_stage_journey')
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

        for i in range(1, 6):
            exp_file = request.files.get(f'expert_image_{i}')
            if exp_file and exp_file.filename != '':
                exp_filename = secure_filename(exp_file.filename)
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)
                exp_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'events', exp_filename))
                # For add_event, the new_event needs to be added to db first to get an ID.
                # Actually, adding objects to relationship works even without ID!
                exp_img = EventExpertImage(image_filename=exp_filename)
                item.expert_images.append(exp_img)

        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('manage_events'))
    return render_template('admin/form_event.html', item=item)
@app.route('/admin/blogs')
@permission_required('blogs')
def manage_blogs():
    """
    Route: Manage Blogs
    Purpose: Lists all blogs so the admin can edit or delete them.
    """
    blogs = Blog.query.all()
    return render_template('admin/manage_blogs.html', items=blogs)

@app.route('/admin/blog/add', methods=['GET', 'POST'])
@permission_required('blogs')
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
@permission_required('mentors')
def manage_mentors():
    """
    Route: Manage Mentors
    Purpose: Lists all mentors so the admin can edit or delete them.
    """
    mentors = Mentor.query.all()
    return render_template('admin/manage_mentors.html', items=mentors)

@app.route('/admin/mentor/add', methods=['GET', 'POST'])
@permission_required('mentors')
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
            
        approach=request.form.get('approach')
        mentorship_details=request.form.get('mentorship_details')
        new_mentor = Mentor(name=name, expertise=expertise, bio=bio, approach=approach, mentorship_details=mentorship_details, image_filename=filename)
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
        item.approach = request.form.get('approach')
        item.mentorship_details = request.form.get('mentorship_details')
        
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
@permission_required('founders')
def manage_founders():
    """
    Route: Manage Founders
    Purpose: Lists all founders so the admin can edit or delete them.
    """
    founders = Founder.query.all()
    return render_template('admin/manage_founders.html', items=founders)

@app.route('/admin/founder/add', methods=['GET', 'POST'])
@permission_required('founders')
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
            
        approach=request.form.get('approach')
        mentorship_details=request.form.get('mentorship_details')
        new_founder = Founder(name=name, role=role, bio=bio, approach=approach, mentorship_details=mentorship_details, image_filename=filename)
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

# =============================================================================
# AUTO-INITIALIZE DATABASE FOR VERCEL DEPLOYMENT
# =============================================================================
with app.app_context():
    try:
        db.create_all()
        # Create default admin if not exists
        if not Admin.query.filter_by(email='admin@builtinmumbai.com').first():
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            new_admin = Admin(email='admin@builtinmumbai.com', password_hash=hashed_password, is_superadmin=True)
            db.session.add(new_admin)
            db.session.commit()
    except Exception as e:
        print(f"Could not initialize database: {e}")

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
        item.approach = request.form.get('approach')
        item.mentorship_details = request.form.get('mentorship_details')
        
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'founders', filename))
            item.image_filename = filename
            
        db.session.commit()
        flash('Founder updated successfully!', 'success')
        return redirect(url_for('manage_founders'))
    return render_template('admin/form_founder.html', item=item)

@app.route('/admin/superadmin')
@login_required
def superadmin_dashboard():
    if not current_user.is_superadmin:
        flash('Access denied. Superadmin only.', 'danger')
        return redirect(url_for('admin_dashboard'))
    admins = Admin.query.all()
    return render_template('admin/superadmin.html', admins=admins)

@app.route('/admin/superadmin/add', methods=['POST'])
@login_required
def superadmin_add_admin():
    if not current_user.is_superadmin:
        abort(403)
    email = request.form.get('email')
    password = request.form.get('password')
    permissions_list = request.form.getlist('permissions')
    permissions_str = ",".join(permissions_list) if permissions_list else ""
    
    if Admin.query.filter_by(email=email).first():
        flash('Admin email already exists.', 'warning')
        return redirect(url_for('superadmin_dashboard'))
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = Admin(email=email, password_hash=hashed_password, is_superadmin=False, permissions=permissions_str)
    db.session.add(new_admin)
    db.session.commit()
    flash('New admin created successfully!', 'success')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/admin/superadmin/delete/<int:id>', methods=['POST'])
@login_required
def superadmin_delete_admin(id):
    if not current_user.is_superadmin:
        abort(403)
    if id == current_user.id:
        flash('You cannot delete yourself.', 'warning')
        return redirect(url_for('superadmin_dashboard'))
    
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully.', 'success')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/admin/member/<int:id>/edit', methods=['GET', 'POST'])
@permission_required('members')
def admin_edit_member(id):
    member = Member.query.get_or_404(id)
    if request.method == 'POST':
        member.first_name = request.form.get('first_name')
        member.last_name = request.form.get('last_name')
        member.email = request.form.get('email')
        db.session.commit()
        flash('Member updated successfully.', 'success')
        return redirect(url_for('manage_members'))
    return render_template('admin/edit_member.html', member=member)

@app.route('/admin/member/<int:id>/delete', methods=['POST'])
@permission_required('members')
def admin_delete_member(id):
    member = Member.query.get_or_404(id)
    EventRegistration.query.filter_by(member_id=member.id).delete()
    MentorshipRequest.query.filter_by(member_id=member.id).delete()
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully.', 'success')
    return redirect(url_for('manage_members'))

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.get_json()
    message = data.get('message', '')
    
    # Generic bot response
    response_text = "Thanks for reaching out! A member of our community team will get back to you shortly."
    
    user_email = None
    if 'member_id' in session:
        member = Member.query.get(session['member_id'])
        if member:
            user_email = member.email
            
    # Save to db
    new_msg = ChatbotMessage(
        user_email=user_email,
        message=message,
        response=response_text
    )
    db.session.add(new_msg)
    db.session.commit()
    
    return {"response": response_text}

@app.route('/admin/chatbot')
@login_required
def admin_chatbot():
    if not current_user.is_superadmin:
        flash('Access denied. Superadmin only.', 'danger')
        return redirect(url_for('admin_dashboard'))
    messages = ChatbotMessage.query.order_by(ChatbotMessage.created_at.desc()).all()
    return render_template('admin/manage_chatbot.html', messages=messages)
