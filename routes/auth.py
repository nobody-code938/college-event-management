from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        role = session.get('user_role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'organizer':
            return redirect(url_for('organizer.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember')

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role
            
            if remember:
                session.permanent = True

            flash(f'Welcome back, {user.name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'organizer':
                return redirect(url_for('organizer.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'student')
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        phone = request.form.get('phone', '').strip()

        # Validation
        if not name or not email or not password:
            flash('Name, Email, and Password are required fields.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')

        # Limit self-registration roles to student or organizer
        if role not in ['student', 'organizer']:
            role = 'student'

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        new_user = User(
            name=name,
            email=email,
            role=role,
            department=department if department else 'Computer Science',
            year=year if year else '3rd Year',
            phone=phone
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration. Please try again.', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
