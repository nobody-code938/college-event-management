import sys
import os
from datetime import datetime, date, time, timedelta

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models import db
from models.user import User
from models.event import Event
from models.registration import Registration
from models.attendance import Attendance

def populate_seed_data():
    """Populates users, events, registrations, and attendance safely if not already present."""
    print("Checking and seeding users...")
    user_definitions = [
        ("Chief System Administrator", "campusevent.admin@gmail.com", "admin", "Office of Student Affairs", "System Administrator", "9876543210", "Admin@2026"),
        ("Demo Admin", "admin@example.com", "admin", "Computer Science & Engineering", "Faculty", "9876543219", "Admin@123"),
        ("Dr. Rahul Sharma", "organizer@example.com", "organizer", "Computer Science & Engineering", "Faculty Coordinator", "9876543211", "Organizer@123"),
        ("Prof. Ananya Sen", "ananya.sen@example.com", "organizer", "Information Technology", "Faculty Coordinator", "9876543212", "Organizer@123"),
        ("Aarav Patel", "student@example.com", "student", "Computer Science & Engineering", "3rd Year", "9876543213", "Student@123"),
        ("Priya Verma", "priya@example.com", "student", "Information Technology", "3rd Year", "9876543214", "Student@123"),
        ("Rohan Gupta", "rohan@example.com", "student", "Electronics & Comm", "2nd Year", "9876543215", "Student@123"),
        ("Sneha Reddy", "sneha@example.com", "student", "Computer Science & Engineering", "4th Year", "9876543216", "Student@123")
    ]

    for name, email, role, dept, yr, ph, pwd in user_definitions:
        if not User.query.filter_by(email=email).first():
            u = User(name=name, email=email, role=role, department=dept, year=yr, phone=ph)
            u.set_password(pwd)
            db.session.add(u)
    db.session.commit()

    organizer1 = User.query.filter_by(email="organizer@example.com").first()
    organizer2 = User.query.filter_by(email="ananya.sen@example.com").first()
    student1 = User.query.filter_by(email="student@example.com").first()
    student2 = User.query.filter_by(email="priya@example.com").first()
    student3 = User.query.filter_by(email="rohan@example.com").first()
    student4 = User.query.filter_by(email="sneha@example.com").first()

    print("Checking and seeding events...")
    today = date.today()

    events_data = [
        {
            "title": "Innovate 2026 - Annual Tech Fest",
            "description": "The flagship annual technical symposium showcasing robotics, project expos, keynotes from industry pioneers, and coding hackathons.",
            "category": "Technical",
            "date": today + timedelta(days=15),
            "time": time(10, 0),
            "venue": "Main Auditorium & Tech Complex",
            "capacity": 250,
            "organizer_id": organizer1.id if organizer1 else 1,
            "image": "tech_fest.jpg",
            "status": "Upcoming"
        },
        {
            "title": "CodeSprint 24H Hackathon",
            "description": "24-hour non-stop hackathon where teams solve real-world industry challenges using Web3, AI, and Cloud technologies.",
            "category": "Hackathon",
            "date": today + timedelta(days=7),
            "time": time(9, 0),
            "venue": "CSE Innovation Lab 3",
            "capacity": 80,
            "organizer_id": organizer1.id if organizer1 else 1,
            "image": "hackathon.jpg",
            "status": "Upcoming"
        },
        {
            "title": "Algorithmic Supremacy Coding Battle",
            "description": "Competitive programming contest testing Data Structures, Dynamic Programming, and Graph Theory skills on HackerRank.",
            "category": "Technical",
            "date": today + timedelta(days=3),
            "time": time(14, 0),
            "venue": "Computer Center Lab 1 & 2",
            "capacity": 50,
            "organizer_id": organizer1.id if organizer1 else 1,
            "image": "coding.jpg",
            "status": "Upcoming"
        },
        {
            "title": "Annual Inter-College Sports Meet",
            "description": "Unleash your athletic prowess! Featuring football tournaments, basketball face-offs, track events, and badminton.",
            "category": "Sports",
            "date": today + timedelta(days=20),
            "time": time(8, 30),
            "venue": "College Sports Stadium & Courts",
            "capacity": 300,
            "organizer_id": organizer2.id if organizer2 else 1,
            "image": "sports.jpg",
            "status": "Upcoming"
        },
        {
            "title": "Euphoria Night Cultural Fest",
            "description": "A vibrant celebration of music, dance, fashion show, theatrical drama, and live musical band performances.",
            "category": "Cultural",
            "date": today + timedelta(days=25),
            "time": time(17, 30),
            "venue": "Open Air Amphitheatre",
            "capacity": 500,
            "organizer_id": organizer2.id if organizer2 else 1,
            "image": "cultural.jpg",
            "status": "Upcoming"
        },
        {
            "title": "Applied AI & Machine Learning Bootcamp",
            "description": "Hands-on workshop covering Python, PyTorch, Large Language Models, and deploying ML APIs using Flask.",
            "category": "Workshop",
            "date": today + timedelta(days=10),
            "time": time(11, 0),
            "venue": "Seminar Hall A",
            "capacity": 60,
            "organizer_id": organizer1.id if organizer1 else 1,
            "image": "workshop.jpg",
            "status": "Upcoming"
        },
        {
            "title": "LensCraft Photography Competition",
            "description": "Showcase your artistic lens. Theme: 'Campus Life & Micro Moments'. Exciting cash prizes for top 3 captures.",
            "category": "Cultural",
            "date": today + timedelta(days=5),
            "time": time(12, 0),
            "venue": "Media Art Gallery",
            "capacity": 40,
            "organizer_id": organizer2.id if organizer2 else 1,
            "image": "photography.jpg",
            "status": "Upcoming"
        },
        {
            "title": "Mastermind Tech & General Knowledge Quiz",
            "description": "Battle of the brains! Test your knowledge across technology trends, science, history, and current affairs.",
            "category": "Quiz",
            "date": today + timedelta(days=2),
            "time": time(15, 0),
            "venue": "Audi 2",
            "capacity": 100,
            "organizer_id": organizer2.id if organizer2 else 1,
            "image": "quiz.jpg",
            "status": "Upcoming"
        }
    ]

    for ed in events_data:
        if not Event.query.filter_by(title=ed["title"]).first():
            ev = Event(**ed)
            db.session.add(ev)
    db.session.commit()

    # Seed sample registrations if empty
    if Registration.query.count() == 0 and student1:
        evs = Event.query.all()
        if len(evs) >= 8:
            regs = [
                Registration(student_id=student1.id, event_id=evs[0].id, status='Registered'),
                Registration(student_id=student1.id, event_id=evs[1].id, status='Registered'),
                Registration(student_id=student1.id, event_id=evs[5].id, status='Registered'),
                Registration(student_id=student2.id, event_id=evs[0].id, status='Registered'),
                Registration(student_id=student2.id, event_id=evs[4].id, status='Registered'),
                Registration(student_id=student3.id, event_id=evs[2].id, status='Registered'),
                Registration(student_id=student3.id, event_id=evs[3].id, status='Registered'),
                Registration(student_id=student4.id, event_id=evs[1].id, status='Registered'),
                Registration(student_id=student4.id, event_id=evs[7].id, status='Registered'),
            ]
            db.session.add_all(regs)
            db.session.commit()

            if Attendance.query.count() == 0:
                att1 = Attendance(registration_id=regs[0].id, event_id=evs[0].id, student_id=student1.id, status='Present')
                att2 = Attendance(registration_id=regs[1].id, event_id=evs[1].id, student_id=student1.id, status='Present')
                att3 = Attendance(registration_id=regs[3].id, event_id=evs[0].id, student_id=student2.id, status='Absent')
                db.session.add_all([att1, att2, att3])
                db.session.commit()

    print("Database seeding verification complete.")


    print("\nDatabase Seeding Completed Successfully!")
    print("---------------------------------------")
    print("Demo Credentials:")
    print("  Admin:     campusevent.admin@gmail.com / Admin@2026")
    print("  Fallback:  admin@example.com / Admin@123")
    print("  Organizer: organizer@example.com / Organizer@123")
    print("  Student:   student@example.com / Student@123")
    print("---------------------------------------")

def seed_database():
    from app import create_app
    app = create_app()
    with app.app_context():
        print("Resetting database tables...")
        db.drop_all()
        db.create_all()
        populate_seed_data()

if __name__ == '__main__':
    seed_database()

