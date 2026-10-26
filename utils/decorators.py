from functools import wraps
from flask import session, flash, redirect, url_for, request, abort

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            user_role = session.get('user_role')
            if user_role not in roles:
                flash('You do not have permission to access this resource.', 'danger')
                # Redirect user to their appropriate dashboard if logged in
                if user_role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user_role == 'organizer':
                    return redirect(url_for('organizer.dashboard'))
                elif user_role == 'student':
                    return redirect(url_for('student.dashboard'))
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
