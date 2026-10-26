import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, Response
from sqlalchemy import func
from models import db
from models.user import User
from models.event import Event, CATEGORY_IMAGES
from models.registration import Registration
from models.attendance import Attendance
from utils.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_organizers = User.query.filter_by(role='organizer').count()
    total_events = Event.query.count()
    total_registrations = Registration.query.filter_by(status='Registered').count()

    # Chart 1: Events by Category
    category_counts = db.session.query(
        Event.category, func.count(Event.id)
    ).group_by(Event.category).all()
    
    chart_category_labels = [c[0] for c in category_counts]
    chart_category_data = [c[1] for c in category_counts]

    # Chart 2: Top Events by Registrations
    top_events = db.session.query(
        Event.title, func.count(Registration.id)
    ).join(Registration, Event.id == Registration.event_id)\
     .filter(Registration.status == 'Registered')\
     .group_by(Event.id)\
     .order_by(func.count(Registration.id).desc())\
     .limit(6).all()

    chart_event_labels = [e[0] for e in top_events]
    chart_event_data = [e[1] for e in top_events]

    # Chart 3: Registrations Trend (simulated monthly counts)
    monthly_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data = [12, 19, 15, 25, 32, 40, 35, 50, 45, 60, 55, 70]  # baseline data

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_organizers=total_organizers,
        total_events=total_events,
        total_registrations=total_registrations,
        chart_category_labels=chart_category_labels,
        chart_category_data=chart_category_data,
        chart_event_labels=chart_event_labels,
        chart_event_data=chart_event_data,
        monthly_labels=monthly_labels,
        monthly_data=monthly_data
    )

@admin_bp.route('/users')
@role_required('admin')
def users():
    search = request.args.get('q', '').strip()
    role_filter = request.args.get('role', 'All').strip()

    query = User.query

    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.department.ilike(f'%{search}%'))
        )

    if role_filter and role_filter != 'All':
        query = query.filter_by(role=role_filter)

    user_list = query.order_by(User.created_at.desc()).all()

    return render_template(
        'admin/users.html',
        users=user_list,
        search_query=search,
        selected_role=role_filter
    )

@admin_bp.route('/users/<int:user_id>')
@role_required('admin')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    registrations = Registration.query.filter_by(student_id=user_id).all() if user.role == 'student' else []
    created_events = Event.query.filter_by(organizer_id=user_id).all() if user.role == 'organizer' else []

    return render_template(
        'admin/user_detail.html',
        user=user,
        registrations=registrations,
        created_events=created_events
    )

@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@role_required('admin')
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role', '').strip()

    if new_role not in ['student', 'organizer', 'admin']:
        flash('Invalid role specified.', 'danger')
        return redirect(url_for('admin.users'))

    # Check if removing the last admin
    if user.role == 'admin' and new_role != 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            flash('Operation failed: Cannot change the role of the only remaining administrator account!', 'danger')
            return redirect(url_for('admin.users'))

    user.role = new_role
    db.session.commit()
    flash(f'Role for {user.name} changed to {new_role.capitalize()}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Protect current logged in admin
    if user.id == session.get('user_id'):
        flash('You cannot delete your own active administrator account!', 'danger')
        return redirect(url_for('admin.users'))

    # Protect last admin
    if user.role == 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            flash('Operation failed: Cannot delete the only remaining administrator account!', 'danger')
            return redirect(url_for('admin.users'))

    user_name = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user_name}" has been permanently deleted.', 'info')
    return redirect(url_for('admin.users'))

@admin_bp.route('/events')
@role_required('admin')
def events():
    search = request.args.get('q', '').strip()
    category = request.args.get('category', 'All').strip()
    status_filter = request.args.get('status', 'All').strip()

    query = Event.query

    if search:
        query = query.filter(
            (Event.title.ilike(f'%{search}%')) |
            (Event.venue.ilike(f'%{search}%'))
        )

    if category and category != 'All':
        query = query.filter_by(category=category)

    if status_filter and status_filter != 'All':
        query = query.filter_by(status=status_filter)

    event_list = query.order_by(Event.date.desc()).all()
    categories = ['All', 'Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']

    return render_template(
        'admin/events.html',
        events=event_list,
        categories=categories,
        search_query=search,
        selected_category=category,
        selected_status=status_filter
    )

@admin_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@role_required('admin')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    title = event.title
    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{title}" deleted by admin.', 'info')
    return redirect(url_for('admin.events'))

@admin_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
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
            return render_template('admin/edit_event.html', event=event, categories=categories, preset_images=CATEGORY_IMAGES)

        db.session.commit()
        flash(f'Event "{event.title}" updated successfully by admin.', 'success')
        return redirect(url_for('admin.events'))

    return render_template('admin/edit_event.html', event=event, categories=categories, preset_images=CATEGORY_IMAGES)

@admin_bp.route('/registrations')
@role_required('admin')
def registrations():
    regs = Registration.query.order_by(Registration.registered_at.desc()).all()
    return render_template('admin/registrations.html', registrations=regs)

@admin_bp.route('/reports')
@role_required('admin')
def reports():
    total_users = User.query.count()
    total_events = Event.query.count()
    total_registrations = Registration.query.count()
    total_attendance = Attendance.query.filter_by(status='Present').count()

    category_stats = db.session.query(
        Event.category,
        func.count(Event.id).label('event_count'),
        func.sum(Event.capacity).label('total_capacity')
    ).group_by(Event.category).all()

    department_stats = db.session.query(
        User.department,
        func.count(User.id).label('user_count')
    ).filter(User.role == 'student').group_by(User.department).all()

    return render_template(
        'admin/reports.html',
        total_users=total_users,
        total_events=total_events,
        total_registrations=total_registrations,
        total_attendance=total_attendance,
        category_stats=category_stats,
        department_stats=department_stats
    )

@admin_bp.route('/export/registrations-csv')
@role_required('admin')
def export_registrations_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Reg ID', 'Student Name', 'Student Email', 'Department', 'Event Title', 'Category', 'Registration Date', 'Status'])
    for reg in Registration.query.order_by(Registration.registered_at.desc()).all():
        writer.writerow([
            reg.id,
            reg.student.name,
            reg.student.email,
            reg.student.department or 'N/A',
            reg.event.title,
            reg.event.category,
            reg.registered_at.strftime('%Y-%m-%d %H:%M') if reg.registered_at else 'N/A',
            reg.status
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=all_registrations_report.csv"}
    )

