# 🗓️ 2-WEEK PRACTICAL IMPLEMENTATION LOG
## COLLEGE EVENT MANAGEMENT SYSTEM
**Student Project Guide & Viva Practical Journal**  
**Methodology:** Waterfall SDLC Model (14 Days Breakdown)  
**Academic Degree:** B.Tech Computer Science & Engineering (3rd Year Capstone)

---

## 📌 WATERFALL MODEL PHASE MAP

| Phase | Days | Focus Areas | Key Output / Deliverable |
| :--- | :--- | :--- | :--- |
| **Phase 1: Requirement Analysis** | Days 1 – 3 | Problem study, role identification, tech stack selection, SRS | Software Requirement Specification |
| **Phase 2: System & DB Design** | Days 4 – 6 | ER Diagram, relational schema, Flask blueprints planning | Database Schema & Architecture Plan |
| **Phase 3: Module Implementation** | Days 7 – 11 | Authentication, Student portal, Organizer console, Admin & Chart.js | Source Code (`app.py`, `models/`, `routes/`, `templates/`) |
| **Phase 4: Testing & Integration** | Days 12 – 13| Boundary testing, overbooking check, seed data creation | Test Matrix & Initialized DB (`seed.py`) |
| **Phase 5: Deployment & Viva Prep** | Day 14 | Local server verification, 24/7 Render cloud deployment & viva documentation | Live Server ([Render](https://college-event-management-9gt4.onrender.com) & Local `5001`) |

---

## 📅 DAY-BY-DAY PROGRESS LOG

### 🔵 PHASE 1: REQUIREMENTS ANALYSIS & SPECIFICATION

#### 🔹 DAY 1: Problem Identification & Domain Research
* **Objective:** Study existing campus event coordination workflows and identify pain points.
* **Activities:**
  * Analyzed manual paper registration forms and Google Forms used in college technical/cultural fests.
  * Identified major issues: duplicate registrations, overbooking beyond hall capacity, lack of attendance tracking, and no centralized analytics.
  * Defined 3 primary user roles: **Student**, **Organizer (Faculty)**, and **Administrator**.
* **Deliverable:** Initial Project Synopsis & Problem Statement.

#### 🔹 DAY 2: Requirements Specification & Tech Stack Finalization
* **Objective:** Define Functional/Non-Functional Requirements and finalize modern, beginner-friendly technology stack.
* **Activities:**
  * Selected **Python 3** & **Flask** for backend framework (lightweight, modular blueprint routing).
  * Selected **SQLite** & **Flask-SQLAlchemy ORM** for database management.
  * Selected **HTML5**, **Bootstrap 5**, **Bootstrap Icons**, **Vanilla CSS**, and **Chart.js** for frontend UI.
  * Drafted Software Requirement Specification (SRS) covering access control, route protection, and database constraints.
* **Deliverable:** SRS Document & Stack Specification.

#### 🔹 DAY 3: Architectural Design & Wireframing
* **Objective:** Structure the application architecture and layout wireframes for key screens.
* **Activities:**
  * Designed Flask application directory structure following clean modular patterns (`models/`, `routes/`, `templates/`, `static/`, `utils/`).
  * Sketched UI wireframes for Landing Page, Student Dashboard, Event Listing, Organizer Attendance Sheet, and Admin Graphical Console.
* **Deliverable:** Directory structure blueprint & UI mockups.

---

### 🟢 PHASE 2: SYSTEM & DATABASE DESIGN

#### 🔹 DAY 4: Relational Schema & Entity-Relationship Modeling
* **Objective:** Design normalized database tables and foreign-key relationships.
* **Activities:**
  * Defined `users` table (`id`, `name`, `email`, `password_hash`, `role`, `department`, `year`, `phone`).
  * Defined `events` table (`id`, `title`, `description`, `category`, `date`, `time`, `venue`, `capacity`, `organizer_id`, `status`).
  * Defined `registrations` table (`id`, `student_id`, `event_id`, `registered_at`, `status`) with unique constraint `(student_id, event_id)`.
  * Defined `attendance` table (`id`, `registration_id`, `event_id`, `student_id`, `status`, `marked_at`).
* **Deliverable:** Database Relational Schema & ER Diagram mapping.

#### 🔹 DAY 5: Blueprint Routing & Auth Guard Strategy
* **Objective:** Map application routes and authorization decorators.
* **Activities:**
  * Designed Flask Blueprints: `auth_bp`, `student_bp`, `organizer_bp`, `admin_bp`.
  * Created custom session decorators `@login_required` and `@role_required(['student', 'organizer', 'admin'])`.
  * Configured Flask `config.py` (Secret Key, SQLite URI, Upload directory).
* **Deliverable:** Blueprint specifications & decorator utility code (`utils/decorators.py`).

#### 🔹 DAY 6: Database Model Creation (`models/`)
* **Objective:** Implement SQLAlchemy ORM classes in Python.
* **Activities:**
  * Implemented `models/user.py` with Werkzeug helper methods `set_password()` and `check_password()`.
  * Implemented `models/event.py` with calculated properties `registered_count`, `seats_left`, and `is_full`.
  * Implemented `models/registration.py` and `models/attendance.py`.
* **Deliverable:** Functional ORM Models python package.

---

### 🟡 PHASE 3: IMPLEMENTATION & MODULE DEVELOPMENT

#### 🔹 DAY 7: Authentication & Authorization Module (`routes/auth.py`)
* **Objective:** Build secure login, user registration, and logout flows.
* **Activities:**
  * Implemented `/auth/register` route with input validation, password confirmation, role selection, and hashing.
  * Implemented `/auth/login` route with email lookup, password verification, and session storage.
  * Implemented `/auth/logout` route clearing session state.
  * Created HTML views: `templates/auth/login.html` & `templates/auth/register.html`.
* **Deliverable:** Fully working user authentication system.

#### 🔹 DAY 8: Public Catalog & Student Module (`routes/student.py`)
* **Objective:** Develop student dashboard, event browsing, filtering, and registration engine.
* **Activities:**
  * Built public Landing Page (`templates/index.html`) with Hero section and event cards.
  * Built `/student/events` page with real-time keyword search, category dropdown filter, and sorting.
  * Implemented `/student/events/<id>/register` handling capacity validation, past-deadline locking, and duplicate registration prevention.
  * Built `/student/my-registrations` page supporting registration cancellation and event cancellation badges.
  * Implemented in-app cancellation notification alert banners on the student dashboard for cancelled events.
* **Deliverable:** Complete Student Portal functionality with automated alerts.

#### 🔹 DAY 9: Organizer Module (`routes/organizer.py`)
* **Objective:** Build event creation, management console, participant roster, and data export.
* **Activities:**
  * Built `/organizer/events/create` form with date-in-past validation and capacity checks.
  * Implemented `/organizer/my-events` dashboard listing created events with edit, cancel, and delete capabilities.
  * Implemented `/organizer/events/<id>/participants` roster with student contact details and search filtering.
  * Implemented `/organizer/events/<id>/export-participants` generating downloadable `.csv` spreadsheets.
* **Deliverable:** Organizer Management Module with CSV Export.

#### 🔹 DAY 10: Digital Attendance System
* **Objective:** Implement live attendance marking and turnout calculation.
* **Activities:**
  * Created `/organizer/events/<id>/attendance` interactive sheet.
  * Added radio toggles for marking student status as **Present** or **Absent**.
  * Calculated real-time turnout percentage statistics (`(presents / total_marked) * 100`).
* **Deliverable:** Attendance tracking system (`templates/organizer/attendance.html`).

#### 🔹 DAY 11: Admin Console & Chart.js Analytics (`routes/admin.py`)
* **Objective:** Develop system administrator portal with graphical charts and report views.
* **Activities:**
  * Created `/admin/dashboard` metric summary cards (Total Students, Organizers, Events, Registrations).
  * Integrated **Chart.js** library to render:
    1. Doughnut Chart: Events breakdown by Category.
    2. Bar Chart: Top registered events.
    3. Line Chart: Monthly registration growth trend.
  * Implemented `/admin/users` management (role modification, account deletion with guard against deleting the last admin).
  * Created `/admin/reports` printable summary page (`window.print()`).
  * Implemented `/admin/export/registrations-csv` for full registration audit exports.
* **Deliverable:** Comprehensive Admin Analytics Console.

---

### 🟠 PHASE 4: INTEGRATION & TESTING

#### 🔹 DAY 12: Comprehensive System & Security Testing
* **Objective:** Execute test cases to ensure data validation, route protection, and error handling.
* **Activities:**
  * Conducted boundary tests on event capacity overbooking.
  * Verified role authorization guards (preventing students from accessing `/admin/dashboard`).
  * Created friendly custom error templates: `404.html`, `403.html`, `500.html`.
* **Deliverable:** System Test Log & Error Handlers.

#### 🔹 DAY 13: Database Seeding & Mock Data Generation (`seed.py`)
* **Objective:** Populate system with realistic demo accounts and sample events for viva demonstration.
* **Activities:**
  * Authored `seed.py` generating:
    * 3 core accounts: Admin (`admin@example.com`), Organizer (`organizer@example.com`), Student (`student@example.com`).
    * 8 realistic events (Annual Tech Fest, CodeSprint Hackathon, Coding Contest, Sports Meet, Cultural Fest, AI Bootcamp, Photography, Quiz).
    * Sample student registrations and marked attendance records.
* **Deliverable:** Automated Seed Script (`python3 seed.py`).

---

### 🔴 PHASE 5: DEPLOYMENT & VIVA DOCUMENTATION

#### 🔹 DAY 14: Local Server Deployment & Presentation Preparation
* **Objective:** Finalize project report, verify local server, and prepare viva demonstration script.
* **Activities:**
  * Installed dependencies in `.venv` environment (`Flask`, `Flask-SQLAlchemy`, `Werkzeug`, `python-dotenv`).
  * Launched local development server on `http://127.0.0.1:5001`.
  * Implemented standardized design system with dark-mode tokens (`#0B1020` background, `#151C30` surfaces, `#1E293B` elevated, `#A78BFA` primary purple, `#8B5CF6` buttons, `#F8FAFC` main text, `#303A52` borders) and semantic status colors (`#15803D` success, `#92400E` pending, `#B91C1C` error, `#1D4ED8` info).
  * Added responsive Dark / Light Mode Switcher toggle button in the navigation bar with `localStorage` state persistence and real-time Chart.js adaptation.
  * Configured production cloud deployment stack: installed and verified `gunicorn` WSGI server, created `Procfile`, and defined Infrastructure-as-Code blueprint (`render.yaml`) for permanent 24/7 web hosting.
  * Initialized Git version control repository (`main` branch) and committed deployment assets.
  * Prepared comprehensive `README.md` and `PROJECT_DOCUMENTATION.md` for project submission.
* **Deliverable:** Working College Event Management System application live 24/7 at [https://college-event-management-9gt4.onrender.com](https://college-event-management-9gt4.onrender.com) and local `5001`.

---

## 🎯 SUMMARY OF PRACTICAL ACHIEVEMENTS

1. **Strict Adherence to SDLC:** Successfully moved from Requirement Analysis ➔ Design ➔ Implementation ➔ Testing ➔ Deployment in 14 structured days.
2. **Robust Multi-Role Architecture:** Full role separation with dedicated dashboards for Students, Organizers, and Admins.
3. **Real-time Analytics:** Visual Chart.js dashboards providing actionable data insights.
4. **Viva Preparedness:** Complete with demo credentials, database seeding script, SRS documentation, and practical progress log.
