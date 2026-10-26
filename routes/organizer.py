import csv
import io
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from models import db
from models.user import User
from models.event import Event, CATEGORY_IMAGES
from models.registration import Registration
from models.attendance import Attendance
from utils.decorators import role_required

organizer_bp = Blueprint('organizer', __name__, url_prefix='/organizer')

@organizer_bp.route('/dashboard')
@role_required('organizer')
def dashboard():
    organizer_id = session['user_id']
    organizer = User.query.get_or_404(organizer_id)

    my_events = Event.query.filter_by(organizer_id=organizer_id).all()
    total_events = len(my_events)
    
    upcoming_events = [e for e in my_events if e.status == 'Upcoming' and e.date >= date.today()]
    
    # Registrations across all organizer events
    event_ids = [e.id for e in my_events]
    registrations = Registration.query.filter(
        Registration.event_id.in_(event_ids),
        Registration.status == 'Registered'
    ).all() if event_ids else []

    total_registrations = len(registrations)
    
    # Attendance summary
    marked_attendance = Attendance.query.filter(
        Attendance.event_id.in_(event_ids)
    ).all() if event_ids else []
    
    presents_count = len([a for a in marked_attendance if a.status == 'Present'])
    attendance_rate = round((presents_count / len(marked_attendance) * 100), 1) if marked_attendance else 0

    return render_template(
        'organizer/dashboard.html',
        organizer=organizer,
        total_events=total_events,
        upcoming_events_count=len(upcoming_events),
        total_registrations=total_registrations,
        attendance_rate=attendance_rate,
        recent_events=sorted(my_events, key=lambda x: x.created_at, reverse=True)[:5]
    )

@organizer_bp.route('/my-events')
@role_required('organizer')
def my_events():
    organizer_id = session['user_id']
    search = request.args.get('q', '').strip()
    status_filter = request.args.get('status', 'All')

    query = Event.query.filter_by(organizer_id=organizer_id)

    if search:
        query = query.filter(Event.title.ilike(f'%{search}%'))

    if status_filter and status_filter != 'All':
        query = query.filter_by(status=status_filter)

    events = query.order_by(Event.date.desc()).all()

    return render_template(
        'organizer/my_events.html',
        events=events,
        search_query=search,
        selected_status=status_filter
    )

@organizer_bp.route('/events/create', methods=['GET', 'POST'])
@role_required('organizer')
def create_event():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        date_str = request.form.get('date', '').strip()
        time_str = request.form.get('time', '').strip()
        venue = request.form.get('venue', '').strip()
        capacity_str = request.form.get('capacity', '100').strip()
        image = request.form.get('image', '').strip() or CATEGORY_IMAGES.get(category, 'default_event.jpg')

        # Basic Form Validation
        categories = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']
        if not title or not description or not category or not date_str or not time_str or not venue:
            flash('All required fields must be filled out.', 'danger')
            return render_template('organizer/create_event.html', categories=categories, preset_images=CATEGORY_IMAGES)

        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            event_time = datetime.strptime(time_str, '%H:%M').time()
            capacity = int(capacity_str)
        except ValueError:
            flash('Invalid date, time, or capacity format.', 'danger')
            return render_template('organizer/create_event.html', categories=categories, preset_images=CATEGORY_IMAGES)

        # Check date not in past
        if event_date < date.today():
            flash('Event date cannot be in the past.', 'warning')
            return render_template('organizer/create_event.html', categories=categories, preset_images=CATEGORY_IMAGES)

        if capacity <= 0:
            flash('Capacity must be a positive integer.', 'warning')
            return render_template('organizer/create_event.html', categories=categories, preset_images=CATEGORY_IMAGES)

        new_event = Event(
            title=title,
            description=description,
            category=category,
            date=event_date,
            time=event_time,
            venue=venue,
            capacity=capacity,
            organizer_id=session['user_id'],
            image=image,
            status='Upcoming'
        )

        try:
            db.session.add(new_event)
            db.session.commit()
            flash(f'Event "{title}" created successfully!', 'success')
            return redirect(url_for('organizer.my_events'))
        except Exception as e:
            db.session.rollback()
            flash('Database error creating event. Please try again.', 'danger')

    categories = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']
    return render_template('organizer/create_event.html', categories=categories, preset_images=CATEGORY_IMAGES)

@organizer_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@role_required('organizer')
def edit_event(event_id):
    organizer_id = session['user_id']
    event = Event.query.filter_by(id=event_id, organizer_id=organizer_id).first_or_404()
    categories = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']

    if request.method == 'POST':
        event.title = request.form.get('title', '').strip()
        event.description = request.form.get('description', '').strip()
        event.category = request.form.get('category', '').strip()
        event.venue = request.form.get('venue', '').strip()
        event.status = request.form.get('status', 'Upcoming')
        
        custom_img = request.form.get('image', '').strip()
        if custom_img:
            event.image = custom_img
        elif not event.image or event.image == 'default_event.jpg':
            event.image = CATEGORY_IMAGES.get(event.category, 'default_event.jpg')

        date_str = request.form.get('date', '').strip()
        time_str = request.form.get('time', '').strip()
        capacity_str = request.form.get('capacity', '100').strip()

        try:
            event.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            event.time = datetime.strptime(time_str, '%H:%M').time()
            event.capacity = int(capacity_str)
        except ValueError:
            flash('Invalid date, time or capacity format.', 'danger')
            return render_template('organizer/edit_event.html', event=event, categories=categories, preset_images=CATEGORY_IMAGES)

        db.session.commit()
        flash('Event details updated successfully!', 'success')
        return redirect(url_for('organizer.my_events'))

    return render_template('organizer/edit_event.html', event=event, categories=categories, preset_images=CATEGORY_IMAGES)

@organizer_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@role_required('organizer')
def delete_event(event_id):
    organizer_id = session['user_id']
    event = Event.query.filter_by(id=event_id, organizer_id=organizer_id).first_or_404()

    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{event.title}" deleted.', 'info')
    return redirect(url_for('organizer.my_events'))

@organizer_bp.route('/events/<int:event_id>/participants')
@role_required('organizer')
def participants(event_id):
    organizer_id = session['user_id']
    event = Event.query.filter_by(id=event_id, organizer_id=organizer_id).first_or_404()

    search_query = request.args.get('q', '').strip()

    registrations_query = Registration.query.filter_by(event_id=event.id, status='Registered')
    
    registrations = registrations_query.all()

    if search_query:
        registrations = [
            r for r in registrations
            if search_query.lower() in r.student.name.lower() or
               search_query.lower() in r.student.email.lower() or
               search_query.lower() in (r.student.department or '').lower()
        ]

    return render_template(
        'organizer/participants.html',
        event=event,
        registrations=registrations,
        search_query=search_query
    )

@organizer_bp.route('/events/<int:event_id>/export-participants')
@role_required('organizer')
def export_participants(event_id):
    organizer_id = session['user_id']
    event = Event.query.filter_by(id=event_id, organizer_id=organizer_id).first_or_404()
    registrations = Registration.query.filter_by(event_id=event.id, status='Registered').all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Student Name', 'Email', 'Department', 'Year', 'Phone', 'Registration Date', 'Attendance Status'])
    for r in registrations:
        att_status = r.attendance.status if r.attendance else 'Not Marked'
        writer.writerow([
            r.student.name,
            r.student.email,
            r.student.department or 'N/A',
            r.student.year or 'N/A',
            r.student.phone or 'N/A',
            r.registered_at.strftime('%Y-%m-%d %H:%M') if r.registered_at else 'N/A',
            att_status
        ])
    output.seek(0)
    filename = f"participants_{event.title.replace(' ', '_').lower()}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

@organizer_bp.route('/events/<int:event_id>/attendance', methods=['GET', 'POST'])
@role_required('organizer')
def attendance(event_id):
    organizer_id = session['user_id']
    event = Event.query.filter_by(id=event_id, organizer_id=organizer_id).first_or_404()

    registrations = Registration.query.filter_by(event_id=event.id, status='Registered').all()

    if request.method == 'POST':
        for reg in registrations:
            status_val = request.form.get(f'attendance_{reg.id}', 'Absent')
            
            att = Attendance.query.filter_by(registration_id=reg.id).first()
            if not att:
                att = Attendance(
                    registration_id=reg.id,
                    event_id=event.id,
                    student_id=reg.student_id,
                    status=status_val
                )
                db.session.add(att)
            else:
                att.status = status_val
                att.marked_at = datetime.utcnow()

        db.session.commit()
        flash('Attendance updated successfully!', 'success')
        return redirect(url_for('organizer.attendance', event_id=event.id))

    # Calculate statistics
    attendance_map = {
        att.registration_id: att.status 
        for att in Attendance.query.filter_by(event_id=event.id).all()
    }
    
    presents = sum(1 for status in attendance_map.values() if status == 'Present')
    absents = sum(1 for status in attendance_map.values() if status == 'Absent')
    total_marked = len(attendance_map)
    percentage = round((presents / total_marked * 100), 1) if total_marked > 0 else 0

    return render_template(
        'organizer/attendance.html',
        event=event,
        registrations=registrations,
        attendance_map=attendance_map,
        presents=presents,
        absents=absents,
        percentage=percentage
    )

@organizer_bp.route('/profile', methods=['GET', 'POST'])
@role_required('organizer')
def profile():
    organizer = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        organizer.name = request.form.get('name', '').strip()
        organizer.department = request.form.get('department', '').strip()
        organizer.phone = request.form.get('phone', '').strip()

        db.session.commit()
        session['user_name'] = organizer.name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('organizer.profile'))

    return render_template('organizer/profile.html', organizer=organizer)
