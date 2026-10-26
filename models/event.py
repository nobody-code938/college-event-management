from datetime import datetime
from models import db

CATEGORY_IMAGES = {
    'Technical': 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80',
    'Hackathon': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80',
    'Cultural': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=800&q=80',
    'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=800&q=80',
    'Workshop': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80',
    'Quiz': 'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?auto=format&fit=crop&w=800&q=80',
    'Gaming': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80',
    'Webinar': 'https://images.unsplash.com/photo-1588196749597-9ff075ee6b5b?auto=format&fit=crop&w=800&q=80',
}

DEFAULT_EVENT_IMAGE = 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80'

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
    def image_url(self):
        if self.image:
            img = self.image.strip()
            if img.startswith('http://') or img.startswith('https://'):
                return img
            for cat, url in CATEGORY_IMAGES.items():
                if img.lower().startswith(cat.lower()[:4]):
                    return url
        return CATEGORY_IMAGES.get(self.category, DEFAULT_EVENT_IMAGE)

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
