# College Event Management System

A web-based **College Event Management System** designed for B.Tech CSE 3rd-year capstone projects. Built with **Python, Flask, SQLite, Bootstrap 5, and Chart.js**, this application enables students, faculty organizers, and administrators to seamlessly publish, discover, register, track attendance, and analyze campus events.

---

## 🌟 Key Features

### 👨‍🎓 Student Role
* **Event Discovery & Filtering:** Search events by keyword, category, date, and sorting options.
* **One-Click Event Registration:** Register for upcoming events with capacity checks, deadline enforcement, and duplicate prevention.
* **Cancellation Alert Banners:** Instant notification alert banner on dashboard when an organizer cancels an event.
* **My Registrations Dashboard:** Track registered events, status (`Registered`, `Event Cancelled`, `Cancelled by You`), and attendance history.
* **Registration Cancellation:** Students can cancel their event registration at any time.
* **Student Profile:** Update department, year, phone contact, and personal details.

### 👨‍🏫 Organizer Role
* **Event Creation & Management:** Create, edit, and delete events with date/time validation (prevents past dates).
* **Participant Roster & CSV Export:** View registered participants and download complete `.csv` participant spreadsheets.
* **Digital Attendance Marking:** Mark student attendance (Present/Absent) with real-time turnout percentages.
* **Organizer Console:** Quick metrics on created events, total registrations, and attendance statistics.

### 🛡️ Admin Role
* **System Dashboard & Chart.js Analytics:**
  * Doughnut Chart: Events by Category
  * Bar Chart: Top Registered Events
  * Line Chart: Monthly Registration Growth Trend
* **User Management:** Search users, filter by role, edit roles, and delete accounts (with protection for the last admin account).
* **Event & Registration Oversight:** View, moderate, or delete any event or registration in the system.
* **Reports & Master CSV Export:** Printable reports module (`window.print()`) and downloadable master registrations `.csv`.

### 🌓 UI & Accessibility
* **Dark / Light Mode Toggle:** Seamless one-click switcher in the top navigation bar with persistent `localStorage` preference and adaptive Chart.js data visualization.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons, JavaScript (ES6+), Chart.js (with Dark-Mode Tokens & Semantic Color Standards)
* **Backend:** Python 3, Flask Web Framework
* **Database:** SQLite (local instance)
* **ORM:** Flask-SQLAlchemy / SQLAlchemy
* **Authentication:** Flask session-based auth with Werkzeug password hashing

---

## 📁 Project Structure

```
college-event-management/
│
├── app.py                     # Flask Application Factory & Entry Point
├── config.py                  # App configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview & setup guide
├── PROJECT_DOCUMENTATION.md   # Software Engineering documentation & diagrams
├── .gitignore                 # Git ignore rules
├── .env.example               # Sample environment configuration
│
├── instance/                  # Database directory
│   └── event_management.db    # SQLite database file
│
├── models/                    # SQLAlchemy ORM Models
│   ├── __init__.py
│   ├── user.py                # User model & password hashing
│   ├── event.py               # Event model & capacity logic
│   ├── registration.py        # Registration model
│   └── attendance.py          # Attendance model
│
├── routes/                    # Flask Blueprints
│   ├── __init__.py
│   ├── auth.py                # Login, Register, Logout
│   ├── student.py             # Student dashboard, event registration, profile
│   ├── organizer.py           # Organizer console, event CRUD, attendance marking
│   └── admin.py               # Admin dashboard, user management, charts, reports
│
├── templates/                 # Jinja2 HTML Templates
│   ├── base.html              # Base layout with navbar & alerts
│   ├── index.html             # Public Landing Page
│   ├── auth/                  # login.html, register.html
│   ├── student/               # dashboard.html, events.html, event_detail.html, my_registrations.html, profile.html
│   ├── organizer/             # dashboard.html, my_events.html, create_event.html, edit_event.html, participants.html, attendance.html, profile.html
│   ├── admin/                 # dashboard.html, users.html, user_detail.html, events.html, registrations.html, reports.html
│   └── errors/                # 404.html, 403.html, 500.html
│
├── static/                    # Static Assets
│   ├── css/
│   │   └── style.css          # Custom styling & modern UI theme
│   ├── js/
│   │   └── script.js          # Interactive features & Chart.js renderer
│   └── images/                # Event images & default placeholders
│
├── utils/                     # Utility Decorators & Helpers
│   ├── __init__.py
│   ├── decorators.py          # @login_required, @role_required
│   └── helpers.py             # Current user & formatting helpers
│
└── seed.py                    # Database seeding script with sample data
```

---

## 🗄️ Database Structure

1. **USERS (`users`)**:
   - `id`, `name`, `email`, `password_hash`, `role` (`student`/`organizer`/`admin`), `department`, `year`, `phone`, `created_at`

2. **EVENTS (`events`)**:
   - `id`, `title`, `description`, `category`, `date`, `time`, `venue`, `capacity`, `organizer_id` (FK), `image`, `status`, `created_at`

3. **REGISTRATIONS (`registrations`)**:
   - `id`, `student_id` (FK), `event_id` (FK), `registered_at`, `status` (`Registered`/`Cancelled`)

4. **ATTENDANCE (`attendance`)**:
   - `id`, `registration_id` (FK), `event_id` (FK), `student_id` (FK), `status` (`Present`/`Absent`), `marked_at`

---

## 🔑 Demo Credentials

> **Note:** The credentials below are pre-configured by running `seed.py`.

* **Admin Account:**
  * Email: `admin@example.com`
  * Password: `Admin@123`
* **Organizer Account:**
  * Email: `organizer@example.com`
  * Password: `Organizer@123`
* **Student Account:**
  * Email: `student@example.com`
  * Password: `Student@123`

---

## 🚀 Quick Setup & Local Execution

### 1. Clone or Extract Project
Navigate to the project root directory:
```bash
cd college-event-management
```

### 2. Create Virtual Environment

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Seed Sample Data
```bash
python3 seed.py
```

### 5. Run Application
```bash
python3 app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🖼️ Screenshots Placeholder

| Landing Page | Student Dashboard |
| :---: | :---: |
| *![Landing Page Placeholder](https://via.placeholder.com/600x350.png?text=Landing+Page)* | *![Student Dashboard Placeholder](https://via.placeholder.com/600x350.png?text=Student+Dashboard)* |

| Organizer Attendance Sheet | Admin Analytics Dashboard |
| :---: | :---: |
| *![Attendance Sheet Placeholder](https://via.placeholder.com/600x350.png?text=Organizer+Attendance)* | *![Admin Dashboard Placeholder](https://via.placeholder.com/600x350.png?text=Admin+Analytics+Charts)* |

---

## 🔮 Future Improvements

1. **Email Notifications:** Automatic confirmation emails upon event registration and reminders 24 hours prior.
2. **QR Code Attendance Check-in:** Generate digital ticket QR codes for students to scan at venue entrances.
3. **Certificate Generation:** Automated PDF participation certificate downloads for present students.
4. **Online Payment Gateway:** Integration with Razorpay/Stripe for paid college workshops.

---

## 👨‍💻 Authors

* **B.Tech Computer Science & Engineering Student Team**
* **Project Module:** Capstone Web Application Project (CSE 3rd Year)
