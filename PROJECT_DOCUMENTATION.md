# SOFTWARE ENGINEERING PROJECT DOCUMENTATION

## COLLEGE EVENT MANAGEMENT SYSTEM
**Degree:** B.Tech Computer Science & Engineering (3rd Year Capstone Project)  
**Document Version:** 1.0.0  
**Technology Stack:** Python, Flask, SQLite, HTML5, Bootstrap 5, Chart.js  

---

## TABLE OF CONTENTS
1. Problem Statement
2. Existing System
3. Proposed System
4. Objectives
5. Functional Requirements
6. Non-Functional Requirements
7. System Modules
8. Use Case Description
9. Database Design & Entity Relationship
10. Software Development Life Cycle (Waterfall Model)
11. Testing Strategy
12. Future Scope

---

## 1. PROBLEM STATEMENT
In academic institutions, organizing campus events (such as technical symposiums, hackathons, sports meets, and cultural festivals) involves extensive coordination among faculty coordinators, student organizers, and participants. Traditional manual processes reliance on paper notices, physical sign-up sheets, and disparate Google Forms leads to:
* High rates of duplicate registrations and attendance spoofing.
* Lack of centralized visibility into event capacities and student attendance records.
* Inefficient paper-based attendance tracking during live events.
* Inability for college administrators to view real-time participation analytics across departments.

---

## 2. EXISTING SYSTEM
The existing management workflow relies on manual paper records and basic static web forms.

### Disadvantages of Existing System:
* **Time Consuming:** Manual compilation of participant spreadsheets requires hours of administrative work.
* **Data Inconsistency:** Inability to validate student credentials or prevent overbooking beyond venue capacity.
* **Security Risks:** Unhashed stored records and lack of role-based access control.
* **No Real-Time Analytics:** Faculty coordinators cannot evaluate attendance turnout or departmental participation metrics.

---

## 3. PROPOSED SYSTEM
The **College Event Management System** is a web application built using Python Flask and SQLite that centralizes all campus event workflows. It provides role-tailored web interfaces for Students, Organizers, and System Administrators.

### Advantages of Proposed System:
* **Centralized Digital Platform:** Single portal for event creation, registration, and attendance tracking.
* **Automated Capacity Enforcement:** Automatically locks registration when event capacity is reached.
* **Role-Based Access Control (RBAC):** Strict separation of privileges between Students, Organizers, and Admins.
* **Digital Attendance Sheet:** Organizers can mark live attendance and evaluate turnout percentages instantly.
* **Interactive Admin Dashboards:** Chart.js visual analytics for category distribution and registration growth.

---

## 4. OBJECTIVES
1. To provide a user-friendly platform for students to browse and register for campus events.
2. To enable faculty organizers to manage events, inspect participant rosters, and mark attendance digitally.
3. To assist college administrators in monitoring system performance and departmental engagement through graphical charts.
4. To implement secure session authentication and Werkzeug password hashing to protect user data.

---

## 5. FUNCTIONAL REQUIREMENTS
Functional requirements describe the specific tasks the system must perform across user roles.

### A. Student Requirements (FR-01 to FR-11)
* **FR-01:** The system shall allow students to create an account with name, email, department, academic year, and phone number.
* **FR-02:** Students shall be able to log in securely and log out.
* **FR-03:** Students shall be able to view upcoming campus events.
* **FR-04:** Students shall be able to search and filter events by keywords, categories, and sort order.
* **FR-05:** Students shall be able to view event details, including date, time, venue, organizer, and available seats.
* **FR-06:** Students shall be able to register for an event with capacity validation.
* **FR-07:** The system shall prevent a student from registering twice for the same event.
* **FR-08:** The system shall prevent registrations when an event is full or registration has closed/passed deadline.
* **FR-09:** Students shall be able to view their registered events and event status.
* **FR-10:** Students shall be able to cancel an active event registration.
* **FR-11:** Students shall be able to view their attendance status (Present, Absent, or Pending).

### B. Organizer Requirements (FR-12 to FR-19)
* **FR-12:** Organizers shall be able to log in securely to their dedicated Organizer Console.
* **FR-13:** Organizers shall be able to create new events with title, description, category, date, time, venue, and capacity.
* **FR-14:** Organizers shall be able to edit or cancel their own events, subject to past-date and system rules.
* **FR-15:** Organizers shall be able to view the list of registered participants with student details.
* **FR-16:** Organizers shall be able to see the total number of registrations and live capacity fill rates.
* **FR-17:** Organizers shall be able to mark participants as Present or Absent digitally.
* **FR-18:** Organizers shall be able to view basic statistics for their events (turnout percentage, total registrants).
* **FR-19:** Organizers shall be able to export participant lists as CSV spreadsheets (`export-participants`).

### C. Administrator Requirements (FR-20 to FR-25)
* **FR-20:** Admin shall be able to view and manage all user accounts (change roles, delete with protection for the last admin).
* **FR-21:** Admin shall be able to manage events across the system (moderation and deletion).
* **FR-22:** Admin shall be able to view all registrations system-wide.
* **FR-23:** Admin shall be able to view overall event and registration statistics with Chart.js charts.
* **FR-24:** Admin shall be able to search for users and events across the entire institution.
* **FR-25:** Admin shall be able to generate printable reports (`window.print()`) and export master registration logs to CSV (`export/registrations-csv`).

---

## 6. NON-FUNCTIONAL REQUIREMENTS
Non-functional requirements describe how well the system should perform its operations, focusing on usability, security, reliability, performance, and data integrity.

| Requirement | Description | System Implementation |
| :--- | :--- | :--- |
| **Usability** | The website should be easy to understand and use. | Clean Bootstrap 5 UI, intuitive navigation, badge indicators, and informative dismissible flash alerts for user feedback. |
| **Security** | Passwords must be hashed, and restricted pages must require authorization. | Passwords hashed using Werkzeug PBKDF2:SHA256 (`set_password()`). Route-level access controlled via `@login_required` and `@role_required` decorators. |
| **Performance** | Pages and common operations should respond within a reasonable time. | Lightweight Flask backend with indexed SQLite queries; average page response time under 50 milliseconds locally. |
| **Reliability** | The system should store registration data accurately and handle errors properly. | ACID-compliant SQLite transactions with automatic `db.session.rollback()` on error; capacity bounds checking preventing overbooking. |
| **Availability** | Users should be able to access the website when the application is running and available. | Self-contained local web service (`http://127.0.0.1:5000`) requiring no external cloud server dependencies or paid APIs. |
| **Compatibility** | The website should work on common modern browsers. | Cross-browser standards-compliant HTML5, CSS3, JavaScript (ES6), and Bootstrap 5 CDN tested on Chrome, Safari, Firefox, and Edge. |
| **Responsiveness** | The interface should adapt to mobile, tablet and desktop screens. | Fluid Bootstrap 5 grid layout, collapsible mobile navigation drawer, and `.table-responsive` containers for all tables. |
| **Maintainability** | The code should be organized so that errors and features can be managed easily. | Modular Flask Blueprints (`auth`, `student`, `organizer`, `admin`), decoupled ORM models (`models/`), and centralized configuration (`config.py`). |
| **Data integrity** | Registrations must refer to valid students and events. | Relational foreign-key constraints with cascade deletions and `UniqueConstraint('student_id', 'event_id')` preventing orphaned or duplicate records. |
| **Privacy** | Student information should only be accessible to authorized users. | Strict Role-Based Access Control (RBAC); students only access personal records, organizers access only their event rosters, and passwords are never exposed. |

---

## 6.1 SYSTEM BEHAVIORAL RULES
The system enforces strict operational and business logic rules across all modules:

1. **Authentication Rule:** Every user must log in before accessing role-restricted features (guarded by `@login_required` and `@role_required`).
2. **Email Uniqueness Rule:** Each email address must be unique across all accounts (`unique=True` index).
3. **Organizer Ownership Rule:** Only authorized organizers can edit, delete, or mark attendance for events they personally created.
4. **Duplicate Prevention Rule:** A student cannot register more than once for the same event (enforced via database unique constraint).
5. **Capacity Enforcement Rule:** An event cannot accept registrations beyond its venue capacity (`is_full` check).
6. **Deadline & Status Rule:** Registration is locked when the event deadline passes or the event becomes full.
7. **Validation Rule:** All required fields must be supplied, and event dates in the past are rejected.
8. **Attendance Integrity Rule:** Attendance can only be recorded for students with valid active registrations.
9. **Administrative Oversight Rule:** Only administrators can modify roles, delete system-wide entities, or access institution-wide metrics.
10. **Cancellation Notification Rule:** When an event is cancelled by an organizer, registered students receive an in-app cancellation notification banner on their dashboard.

---

## 6.2 DESIGN SYSTEM & COLOR SPECIFICATIONS
The user interface follows a modern dark-mode aesthetic with strict, semantic color mapping:

### Dark-Mode Surface & Typography Tokens:
| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Page Background** | `#0B1020` | Primary app background |
| **Card / Surface** | `#151C30` | Cards, tables, and modal surface background |
| **Elevated Surface** | `#1E293B` | Inputs, dropdown menus, table headers, and hovering states |
| **Primary Purple** | `#A78BFA` | Accents, links, brand highlights |
| **Primary Button** | `#8B5CF6` | Consistent CTA & action buttons across views (hover: `#7C3AED`) |
| **Main Text** | `#F8FAFC` | Primary typography for maximum readability |
| **Secondary Text** | `#CBD5E1` | Subtitles, labels, and metadata |
| **Border** | `#303A52` | Clean divider borders across cards, forms, and tables |

### Light-Mode Surface & Typography Tokens:
| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Page Background** | `#F8FAFC` | Clean light background |
| **Card / Surface** | `#FFFFFF` | Crisp white cards, tables, and modal surface background |
| **Elevated Surface** | `#F1F5F9` | Inputs, dropdown menus, table headers |
| **Primary Purple** | `#7C3AED` | High-contrast purple accents and brand highlights |
| **Primary Button** | `#8B5CF6` | Consistent purple button across both modes |
| **Main Text** | `#0F172A` | Deep charcoal typography for high legibility |
| **Secondary Text** | `#64748B` | Subtle labels, timestamps, and metadata |
| **Border** | `#E2E8F0` | Subtle clean light borders |

### Dynamic Theme Switcher:
* **Interactive Toggle:** Navigation bar includes a dedicated Dark / Light mode toggle button with reactive moon (`bi-moon-stars-fill`) and sun (`bi-sun-fill`) icons.
* **Persistent Preferences:** User theme selection is stored in `localStorage`, maintaining continuity across page reloads and user sessions.
* **FOUC Prevention:** Immediate inline pre-render script prevents flash of unstyled content during transitions.
* **Chart.js Adaptation:** Admin charts automatically update grid line colors and axis label contrast upon theme change.

---

## 7. SYSTEM MODULES

1. **Authentication Module (`routes/auth.py`)**: Handles user login, registration, password hashing, and logout sessions.
2. **Student Module (`routes/student.py`)**: Manages event discovery, detail views, registration creation/cancellation, and profile updates.
3. **Organizer Module (`routes/organizer.py`)**: Handles event creation, updates, participant management, and attendance marking.
4. **Admin Module (`routes/admin.py`)**: Handles user management, overall event moderation, Chart.js analytics, and system reports.

---

## 8. USE CASE DESCRIPTION

### Use Case 1: Student Event Registration
* **Actor:** Student
* **Pre-condition:** Student is logged in.
* **Main Flow:**
  1. Student navigates to Explore Events page.
  2. Student selects an event and clicks "Register".
  3. System validates event capacity and checks for existing registration.
  4. System records registration in database and displays success notification.
* **Alternative Flow:** If event is full or student is already registered, system displays an informational alert.

### Use Case 2: Attendance Marking by Organizer
* **Actor:** Organizer
* **Pre-condition:** Event has registered students.
* **Main Flow:**
  1. Organizer selects "Attendance" from My Events page.
  2. System loads student list.
  3. Organizer toggles Present/Absent for each student and clicks "Save Attendance".
  4. System updates database and re-calculates turnout percentage.

---

## 9. DATABASE DESIGN

### Database Schema Tables:

1. **`users` Table:**
   - `id` (INTEGER, Primary Key)
   - `name` (VARCHAR)
   - `email` (VARCHAR, Unique)
   - `password_hash` (VARCHAR)
   - `role` (VARCHAR - student/organizer/admin)
   - `department` (VARCHAR)
   - `year` (VARCHAR)
   - `phone` (VARCHAR)
   - `created_at` (DATETIME)

2. **`events` Table:**
   - `id` (INTEGER, Primary Key)
   - `title` (VARCHAR)
   - `description` (TEXT)
   - `category` (VARCHAR)
   - `date` (DATE)
   - `time` (TIME)
   - `venue` (VARCHAR)
   - `capacity` (INTEGER)
   - `organizer_id` (INTEGER, Foreign Key -> `users.id`)
   - `image` (VARCHAR)
   - `status` (VARCHAR - Upcoming/Completed/Cancelled)
   - `created_at` (DATETIME)

3. **`registrations` Table:**
   - `id` (INTEGER, Primary Key)
   - `student_id` (INTEGER, Foreign Key -> `users.id`)
   - `event_id` (INTEGER, Foreign Key -> `events.id`)
   - `registered_at` (DATETIME)
   - `status` (VARCHAR - Registered/Cancelled)

4. **`attendance` Table:**
   - `id` (INTEGER, Primary Key)
   - `registration_id` (INTEGER, Foreign Key -> `registrations.id`)
   - `event_id` (INTEGER, Foreign Key -> `events.id`)
   - `student_id` (INTEGER, Foreign Key -> `users.id`)
   - `status` (VARCHAR - Present/Absent)
   - `marked_at` (DATETIME)

---

## 10. WATERFALL MODEL METHODOLOGY
The project followed a structured sequential Waterfall SDLC model:

```
[Requirements Analysis] ➔ [System Design] ➔ [Implementation] ➔ [Testing & Verification] ➔ [Deployment]
```

1. **Requirements Analysis:** Collected requirements for student registration, organizer tracking, and admin dashboards.
2. **System Design:** Designed database schema, route architecture, and Jinja2 templates.
3. **Implementation:** Developed Flask backend routes, SQLAlchemy models, and Bootstrap frontend interface.
4. **Testing:** Executed unit checks, authentication boundary tests, and registration capacity tests.
5. **Deployment:** Initialized local SQLite instance via automated seeding script (`seed.py`).

---

## 11. TESTING STRATEGY

| Test Case ID | Test Scenario | Expected Outcome | Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | User Registration with duplicate email | Block registration and flash warning alert | **PASS** |
| **TC-02** | Student registering for full capacity event | Block registration and display "Event Full" badge | **PASS** |
| **TC-03** | Organizer creating event with past date | Flash warning: "Event date cannot be in past" | **PASS** |
| **TC-04** | Student accessing Admin route `/admin/dashboard` | Redirect to student dashboard with 403 / warning | **PASS** |
| **TC-05** | Admin attempting to delete the only admin user | Action blocked with error alert | **PASS** |

---

## 12. FUTURE SCOPE
* Integration of QR Code scanning for instant venue check-in.
* Automated email notifications for event reminders.
* PDF Certificate generation for attendees.
* Integration with payment gateway for premium paid workshops.

---

## 13. PRODUCTION CLOUD DEPLOYMENT SPECIFICATION

The application is architected and configured for permanent 24/7 cloud hosting:

* **Live Production URL:** **[https://college-event-management-9gt4.onrender.com](https://college-event-management-9gt4.onrender.com)**
* **Production WSGI Server:** `gunicorn` (Python WSGI HTTP Server) configured via [`Procfile`](file:///Users/nex/Desktop/college-event-management/Procfile) (`web: gunicorn "app:create_app()"`).
* **Infrastructure as Code:** [`render.yaml`](file:///Users/nex/Desktop/college-event-management/render.yaml) blueprint defining build commands, auto-seeding (`python seed.py`), and environment variable generation.
* **Database Portability:** [`config.py`](file:///Users/nex/Desktop/college-event-management/config.py) automatically detects `DATABASE_URL` for managed PostgreSQL (transforming legacy `postgres://` to `postgresql://`) with seamless fallback to SQLite.
* **Auto-Schema Migration:** Application startup hook executes `db.create_all()` inside app context, guaranteeing table availability upon deployment.
