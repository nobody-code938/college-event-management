from datetime import datetime
from models import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registrations.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # 'Present', 'Absent', 'Pending'
    marked_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student_rel = db.relationship('User', foreign_keys=[student_id], backref='attendance_records')
    event_rel = db.relationship('Event', foreign_keys=[event_id], backref='attendance_records')

    __table_args__ = (
        db.UniqueConstraint('registration_id', name='unique_registration_attendance'),
    )

    def __repr__(self):
        return f'<Attendance Reg:{self.registration_id} Status:{self.status}>'
