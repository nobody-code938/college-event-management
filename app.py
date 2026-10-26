import os
from flask import Flask, render_template, session
from config import Config
from models import db
from models.user import User
from models.event import Event
from routes.auth import auth_bp
from routes.student import student_bp
from routes.organizer import organizer_bp
from routes.admin import admin_bp
from utils.helpers import get_current_user, format_date_str, format_time_str

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Ensure database tables are created on launch & auto-seeded if empty
    with app.app_context():
        db.create_all()
        try:
            from models.user import User
            if not User.query.filter_by(role='admin').first():
                from seed import populate_seed_data
                populate_seed_data()
        except Exception as e:
            app.logger.warning(f"Startup auto-seed note: {e}")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(organizer_bp)
    app.register_blueprint(admin_bp)

    # Global context processors & template filters
    @app.context_processor
    def inject_user():
        return {
            'current_user': get_current_user(),
            'session_role': session.get('user_role'),
            'session_name': session.get('user_name')
        }

    @app.template_filter('format_date')
    def filter_format_date(val):
        return format_date_str(val)

    @app.template_filter('format_time')
    def filter_format_time(val):
        return format_time_str(val)

    # Public Landing Page Route
    @app.route('/')
    def index():
        upcoming_events = Event.query.filter_by(status='Upcoming')\
            .order_by(Event.date.asc())\
            .limit(6).all()
            
        categories = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz']
        
        return render_template('index.html', upcoming_events=upcoming_events, categories=categories)

    # Public Event Catalog Page
    @app.route('/events')
    def public_events():
        from flask import request
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
        else:
            query = query.order_by(Event.date.asc(), Event.time.asc())

        events_list = query.all()
        categories = ['All', 'Technical', 'Cultural', 'Sports', 'Workshop', 'Hackathon', 'Quiz', 'Gaming', 'Webinar']

        registered_event_ids = []
        if session.get('user_id') and session.get('user_role') == 'student':
            from models.registration import Registration
            registered_event_ids = [
                r.event_id for r in Registration.query.filter_by(student_id=session['user_id'], status='Registered').all()
            ]

        return render_template(
            'student/events.html',
            events=events_list,
            categories=categories,
            search_query=search_query,
            selected_category=category,
            selected_sort=sort_by,
            registered_event_ids=registered_event_ids
        )

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Auto-create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
