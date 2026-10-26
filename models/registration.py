from datetime import datetime
from models import db

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Registered')  # 'Registered', 'Cancelled'

    # Foreign key constraints & uniqueness
    __table_args__ = (
        db.UniqueConstraint('student_id', 'event_id', name='unique_student_event_registration'),
    )

    # Relationship to attendance
    attendance = db.relationship('Attendance', backref='registration', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Registration Student:{self.student_id} Event:{self.event_id} - {self.status}>'
