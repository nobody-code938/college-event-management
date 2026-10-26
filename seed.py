import sys
import os
from datetime import datetime, date, time, timedelta

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from models import db
from models.user import User
from models.event import Event
from models.registration import Registration
from models.attendance import Attendance

app = create_app()

def seed_database():
    with app.app_context():
        print("Resetting database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Users...")
        # 1. Admin Account
        admin = User(
            name="System Admin",
            email="admin@example.com",
            role="admin",
            department="Computer Science & Engineering",
            year="Faculty",
            phone="9876543210"
        )
        admin.set_password("Admin@123")

        # 2. Organizer Account
        organizer1 = User(
            name="Dr. Rahul Sharma",
            email="organizer@example.com",
            role="organizer",
            department="Computer Science & Engineering",
            year="Faculty Coordinator",
            phone="9876543211"
        )
        organizer1.set_password("Organizer@123")

        organizer2 = User(
            name="Prof. Ananya Sen",
            email="ananya.sen@example.com",
            role="organizer",
            department="Information Technology",
            year="Faculty Coordinator",
            phone="9876543212"
        )
        organizer2.set_password("Organizer@123")

        # 3. Primary Student Account
        student1 = User(
            name="Aarav Patel",
            email="student@example.com",
            role="student",
            department="Computer Science & Engineering",
            year="3rd Year",
            phone="9876543213"
        )
        student1.set_password("Student@123")

        # Additional Sample Students
        student2 = User(
            name="Priya Verma",
            email="priya@example.com",
            role="student",
            department="Information Technology",
            year="3rd Year",
            phone="9876543214"
        )
        student2.set_password("Student@123")

        student3 = User(
            name="Rohan Gupta",
            email="rohan@example.com",
            role="student",
            department="Electronics & Comm",
            year="2nd Year",
            phone="9876543215"
        )
        student3.set_password("Student@123")

        student4 = User(
            name="Sneha Reddy",
            email="sneha@example.com",
            role="student",
            department="Computer Science & Engineering",
            year="4th Year",
            phone="9876543216"
        )
        student4.set_password("Student@123")

        db.session.add_all([admin, organizer1, organizer2, student1, student2, student3, student4])
        db.session.commit()

        print("Seeding Events...")
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
                "organizer_id": organizer1.id,
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
                "organizer_id": organizer1.id,
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
                "organizer_id": organizer1.id,
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
                "organizer_id": organizer2.id,
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
                "organizer_id": organizer2.id,
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
                "organizer_id": organizer1.id,
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
                "organizer_id": organizer2.id,
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
                "organizer_id": organizer2.id,
                "image": "quiz.jpg",
                "status": "Upcoming"
            }
        ]

        created_events = []
        for ed in events_data:
            ev = Event(**ed)
            db.session.add(ev)
            created_events.append(ev)
        
        db.session.commit()

        print("Seeding Registrations...")
        # Add sample registrations for students
        regs = [
            Registration(student_id=student1.id, event_id=created_events[0].id, status='Registered'),
            Registration(student_id=student1.id, event_id=created_events[1].id, status='Registered'),
            Registration(student_id=student1.id, event_id=created_events[5].id, status='Registered'),
            Registration(student_id=student2.id, event_id=created_events[0].id, status='Registered'),
            Registration(student_id=student2.id, event_id=created_events[4].id, status='Registered'),
            Registration(student_id=student3.id, event_id=created_events[2].id, status='Registered'),
            Registration(student_id=student3.id, event_id=created_events[3].id, status='Registered'),
            Registration(student_id=student4.id, event_id=created_events[1].id, status='Registered'),
            Registration(student_id=student4.id, event_id=created_events[7].id, status='Registered'),
        ]
        
        db.session.add_all(regs)
        db.session.commit()

        print("Seeding Sample Attendance...")
        # Mark attendance for a few registrations
        att1 = Attendance(registration_id=regs[0].id, event_id=created_events[0].id, student_id=student1.id, status='Present')
        att2 = Attendance(registration_id=regs[1].id, event_id=created_events[1].id, student_id=student1.id, status='Present')
        att3 = Attendance(registration_id=regs[3].id, event_id=created_events[0].id, student_id=student2.id, status='Absent')
        
        db.session.add_all([att1, att2, att3])
        db.session.commit()

        print("\nDatabase Seeding Completed Successfully!")
        print("---------------------------------------")
        print("Demo Credentials:")
        print("  Admin:     admin@example.com / Admin@123")
        print("  Organizer: organizer@example.com / Organizer@123")
        print("  Student:   student@example.com / Student@123")
        print("---------------------------------------")

if __name__ == '__main__':
    seed_database()
