from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.event import Event
from models.registration import Registration
from models.attendance import Attendance
from utils.decorators import role_required

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@role_required('student')
def dashboard():
    student_id = session['user_id']
    student = User.query.get_or_404(student_id)

    # Statistics
    total_events_count = Event.query.filter_by(status='Upcoming').count()
    
    student_registrations = Registration.query.filter_by(student_id=student_id).all()
    total_registrations = len([r for r in student_registrations if r.status == 'Registered'])
    
    # Upcoming registered events
    upcoming_registrations = [
        r for r in student_registrations 
        if r.status == 'Registered' and r.event.date >= datetime.utcnow().date()
    ]
    
    # Attendance summary
    attendance_records = Attendance.query.filter_by(student_id=student_id).all()
    total_marked = len(attendance_records)
    presents = len([a for a in attendance_records if a.status == 'Present'])
    attendance_rate = round((presents / total_marked * 100), 1) if total_marked > 0 else 0

    # Cancelled events notifications for student
    cancelled_registered_events = [
        r for r in student_registrations 
        if r.status == 'Registered' and r.event.status == 'Cancelled'
    ]

    return render_template(
        'student/dashboard.html',
        student=student,
        total_events_count=total_events_count,
        total_registrations=total_registrations,
        upcoming_registrations=upcoming_registrations[:5],
        cancelled_registered_events=cancelled_registered_events,
        total_marked=total_marked,
        presents=presents,
        attendance_rate=attendance_rate
    )

@student_bp.route('/events')
@role_required('student')
def events():
    search_query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'upcoming')

    query = Event.query.filter_by(status='Upcoming')

    if search_query:
        query = query.filter(
            (Event.title.ilike(f'%{search_query}%')) |
            (Event.description.ilike(f'%{search_query}%')) |
            (Event.venue.ilike(f'%{search_query}%'))
        )

    if category and category != 'All':
        query = query.filter_by(category=category)

    if sort_by == 'newest':
        query = query.order_by(Event.created_at.desc())
    else:  # upcoming
        query = query.order_by(Event.date.asc(), Event.time.asc())

    event_list = query.all()
    categories = ['All', 'Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']

    # Find registered event IDs for current student
    student_id = session['user_id']
    registered_event_ids = [
        r.event_id for r in Registration.query.filter_by(student_id=student_id, status='Registered').all()
    ]

    return render_template(
        'student/events.html',
        events=event_list,
        categories=categories,
        search_query=search_query,
        selected_category=category,
        selected_sort=sort_by,
        registered_event_ids=registered_event_ids
    )

@student_bp.route('/events/<int:event_id>')
@role_required('student')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    student_id = session['user_id']

    registration = Registration.query.filter_by(
        student_id=student_id,
        event_id=event_id
    ).first()

    is_registered = registration is not None and registration.status == 'Registered'

    return render_template(
        'student/event_detail.html',
        event=event,
        is_registered=is_registered,
        registration=registration
    )

@student_bp.route('/events/<int:event_id>/register', methods=['POST'])
@role_required('student')
def register_event(event_id):
    student_id = session['user_id']
    event = Event.query.get_or_404(event_id)

    # 1. Event Status & Deadline Check (Rule 6)
    if event.status != 'Upcoming' or event.date < date.today():
        flash('Registration has closed for this event.', 'warning')
        return redirect(url_for('student.event_detail', event_id=event_id))

    # 2. Existing Registration Check
    existing_reg = Registration.query.filter_by(
        student_id=student_id,
        event_id=event_id
    ).first()

    if existing_reg:
        if existing_reg.status == 'Registered':
            flash('You are already registered for this event.', 'info')
            return redirect(url_for('student.event_detail', event_id=event_id))
        else: # Reactivate cancelled registration if capacity permits
            if event.is_full:
                flash('Sorry, this event has reached full capacity.', 'danger')
                return redirect(url_for('student.event_detail', event_id=event_id))
            
            existing_reg.status = 'Registered'
            existing_reg.registered_at = datetime.utcnow()
            db.session.commit()
            flash('Your registration for this event has been reactivated!', 'success')
            return redirect(url_for('student.my_registrations'))

    # 3. Capacity Check
    if event.is_full:
        flash('Sorry! Event capacity is full. Cannot register.', 'danger')
        return redirect(url_for('student.event_detail', event_id=event_id))

    # 4. Create new registration
    new_reg = Registration(
        student_id=student_id,
        event_id=event_id,
        status='Registered'
    )

    try:
        db.session.add(new_reg)
        db.session.commit()
        flash(f'Successfully registered for {event.title}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to register. Please try again.', 'danger')

    return redirect(url_for('student.my_registrations'))

@student_bp.route('/my-registrations')
@role_required('student')
def my_registrations():
    student_id = session['user_id']
    registrations = Registration.query.filter_by(student_id=student_id)\
        .order_by(Registration.registered_at.desc()).all()

    return render_template(
        'student/my_registrations.html',
        registrations=registrations
    )

@student_bp.route('/registrations/<int:reg_id>/cancel', methods=['POST'])
@role_required('student')
def cancel_registration(reg_id):
    student_id = session['user_id']
    registration = Registration.query.filter_by(id=reg_id, student_id=student_id).first_or_404()

    if registration.status == 'Cancelled':
        flash('Registration is already cancelled.', 'info')
    else:
        registration.status = 'Cancelled'
        db.session.commit()
        flash(f'Registration for "{registration.event.title}" has been cancelled.', 'success')

    return redirect(url_for('student.my_registrations'))

@student_bp.route('/profile', methods=['GET', 'POST'])
@role_required('student')
def profile():
    student = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        student.name = request.form.get('name', '').strip()
        student.department = request.form.get('department', '').strip()
        student.year = request.form.get('year', '').strip()
        student.phone = request.form.get('phone', '').strip()

        db.session.commit()
        session['user_name'] = student.name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html', student=student)
