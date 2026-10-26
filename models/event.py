from datetime import datetime
from models import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=100)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image = db.Column(db.String(255), nullable=True, default='default_event.jpg')
    status = db.Column(db.String(20), nullable=False, default='Upcoming')  # 'Upcoming', 'Completed', 'Cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')

    @property
    def registered_count(self):
        from models.registration import Registration
        return Registration.query.filter_by(event_id=self.id, status='Registered').count()

    @property
    def seats_left(self):
        return max(0, self.capacity - self.registered_count)

    @property
    def is_full(self):
        return self.seats_left <= 0

    def __repr__(self):
        return f'<Event {self.title} - {self.category} ({self.status})>'
