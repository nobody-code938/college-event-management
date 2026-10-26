from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student', 'organizer', 'admin'
    department = db.Column(db.String(100), nullable=True)
    year = db.Column(db.String(20), nullable=True)  # '1st Year', '2nd Year', '3rd Year', '4th Year'
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    created_events = db.relationship('Event', backref='organizer', lazy=True, foreign_keys='Event.organizer_id')
    registrations = db.relationship('Registration', backref='student', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_organizer(self):
        return self.role == 'organizer'

    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.name} ({self.email}) - {self.role}>'
