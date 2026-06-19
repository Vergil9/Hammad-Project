# 🎓 CampusConnect — Student Management System

> **Final Semester Project | OSSD-Y9 | University of Management and Technology (UMT)**  
> Developer: Hammad | Session: 2026

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Technology Stack](#-technology-stack)
4. [Project Structure](#-project-structure)
5. [Database Schema](#-database-schema)
6. [API Documentation](#-api-documentation)
7. [Setup & Installation](#-setup--installation)
8. [Running the Project](#-running-the-project)
9. [Frontend Pages](#-frontend-pages)
10. [Security Architecture](#-security-architecture)
11. [Known Issues & Troubleshooting](#-known-issues--troubleshooting)
12. [Environment Variables](#-environment-variables)

---

## 📌 Project Overview

**CampusConnect** is a full-stack web application built as a centralized Student Management System for universities. It enables administrators and faculty to manage student records, course information, and enrollments through a modern, secure, and intuitive interface.

The system provides:
- 🔐 JWT-based authentication with role-based access (Admin, Faculty, Student)
- 📊 A real-time analytics dashboard
- 👨‍🎓 Full CRUD operations on student records
- 🔍 Search and filter capabilities
- 📚 Course management
- 🌐 RESTful API with interactive Swagger documentation

---

## 🎯 Problem Statement

Many universities rely on paper-based systems or fragmented legacy software that is:
- Slow and difficult to navigate
- Prone to data loss and errors
- Lacking in real-time analytics
- Insecure with no proper authentication

**CampusConnect** resolves these problems by providing a unified, secure, and modern web platform that streamlines all student data operations.

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6+) | UI — 5 responsive pages with glassmorphism design |
| **Backend** | Python 3 + FastAPI | Async REST API with automatic OpenAPI docs |
| **Database** | PostgreSQL (via Supabase) | Hosted relational database |
| **ORM** | SQLAlchemy 2.0 (async) + asyncpg | Database interaction |
| **Authentication** | JWT (python-jose) + bcrypt | Secure token-based auth + password hashing |
| **Hosting (DB)** | Supabase (Mumbai — ap-south-1) | Managed PostgreSQL with connection pooling |
| **Dev Server** | uvicorn | ASGI server for FastAPI |

---

## 📁 Project Structure

```
Hammad Project/
├── backend/
│   ├── main.py          # FastAPI app, all API routes, auth logic
│   ├── database.py      # SQLAlchemy engine, session factory, Base
│   ├── models.py        # ORM models: User, Student, Course, Enrollment
│   ├── schemas.py       # Pydantic schemas for request/response validation
│   ├── requirements.txt # Python dependencies
│   └── .env             # Environment variables (not committed to git)
│
├── frontend/
│   ├── index.html       # Home page — hero section, features
│   ├── about.html       # About page — project info, target users
│   ├── login.html       # Login + Register page (JWT auth)
│   ├── dashboard.html   # Analytics dashboard (protected)
│   ├── manage.html      # Student CRUD management (protected)
│   └── style.css        # Global styles — dark mode, glassmorphism
│
├── README.md            # This file — full project documentation
├── DATABASE_SCHEMA.md   # Detailed database table descriptions
├── PROJECT_STRUCTURE.md # Directory tree with explanations
└── .gitignore           # Git ignore rules
```

---

## 🗄 Database Schema

The system uses a **PostgreSQL** relational database with 4 tables:

### `users` — Authentication & Roles
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment primary key |
| `email` | String (unique) | User's email — used for login |
| `hashed_password` | String | bcrypt-hashed password |
| `full_name` | String | Display name |
| `role` | Enum | `admin`, `faculty`, or `student` |
| `is_active` | Boolean | Account active status |
| `created_at` | DateTime | Auto-set on creation |

### `students` — Student Records
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment primary key |
| `name` | String | Full name |
| `email` | String (unique) | Student email |
| `course` | String | Enrolled program (e.g., Computer Science) |
| `year` | Integer | Academic year (1–5) |
| `status` | Enum | `active`, `inactive`, or `graduated` |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on edit |

### `courses` — Course Catalog
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment primary key |
| `name` | String | Course full name |
| `code` | String (unique) | Course code (e.g., CS101) |
| `description` | Text | Optional course description |
| `created_at` | DateTime | Auto-set on creation |

### `enrollments` — Student-Course Links
| Column | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-increment primary key |
| `student_id` | FK → students.id | Enrolled student |
| `course_id` | FK → courses.id | Course enrolled in |
| `user_id` | FK → users.id | User who created enrollment |
| `enrollment_date` | DateTime | Auto-set on creation |
| `status` | String | `enrolled`, etc. |

---

## 📡 API Documentation

> Interactive docs available at: **http://127.0.0.1:8000/docs** (when backend is running)

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register a new user account | ❌ No |
| `POST` | `/api/auth/login` | Login and receive a JWT token | ❌ No |

**Register Request Body:**
```json
{
  "email": "hammad@umt.edu.pk",
  "full_name": "Hammad",
  "password": "yourpassword",
  "role": "admin"
}
```

**Login Request Body:**
```json
{
  "email": "hammad@umt.edu.pk",
  "password": "yourpassword"
}
```

**Login Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

---

### Student Endpoints

All student endpoints require the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/students` | Create a new student record |
| `GET` | `/api/students?page=1&limit=10` | List all students (paginated) |
| `GET` | `/api/students/{id}` | Get one student by ID |
| `PUT` | `/api/students/{id}` | Update student details |
| `DELETE` | `/api/students/{id}` | Delete a student record |
| `GET` | `/api/students/search?q=hammad` | Search by name or email |
| `GET` | `/api/students/filter?course=CS&year=2&status=active` | Filter students |

**Create/Update Student Body:**
```json
{
  "name": "Ali Raza",
  "email": "ali@umt.edu.pk",
  "course": "Computer Science",
  "year": 2,
  "status": "active"
}
```

---

### Dashboard & Course Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/dashboard/stats` | Returns total students, courses, enrollments + recent 5 students |
| `POST` | `/api/courses` | Create a new course |
| `GET` | `/api/courses` | List all courses |

---

### Utility Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and info |
| `GET` | `/health` | Database connection health check |

---

## ⚙ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- Git
- A modern browser (Chrome / Edge recommended)

---

### Step 1 — Clone the Repository

```powershell
git clone https://github.com/Vergil9/Hammad-Project.git
cd "Hammad-Project"
```

---

### Step 2 — Create & Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your prompt.

---

### Step 3 — Install Backend Dependencies

```powershell
pip install -r backend/requirements.txt
```

**Dependencies installed:**
- `fastapi` — Web framework
- `uvicorn[standard]` — ASGI server
- `sqlalchemy[asyncio]` — ORM
- `asyncpg` — Async PostgreSQL driver
- `pydantic` — Data validation
- `python-jose[cryptography]` — JWT tokens
- `bcrypt` — Password hashing
- `python-multipart` — Form data support
- `python-dotenv` — Environment variable loading

---

### Step 4 — Configure Environment Variables

The `backend/.env` file is already configured for the Supabase project. It contains:

```env
DATABASE_URL=postgresql+asyncpg://postgres.vqoavyjepfjxrcxtrxkw:Hammad%401122@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ Note: The `@` in the password is URL-encoded as `%40` in the DATABASE_URL.

---

## 🚀 Running the Project

### Terminal 1 — Start the Backend

```powershell
cd "d:\Work\antigravity\Hammad Project"
.\venv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     ✅ Connected to Supabase (Mumbai ap-south-1). Tables initialized.
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Terminal 2 — Start the Frontend

```powershell
cd "d:\Work\antigravity\Hammad Project\frontend"
python -m http.server 5500 --bind 127.0.0.1
```

Expected output:
```
Serving HTTP on 127.0.0.1 port 5500 (http://127.0.0.1:5500/) ...
```

---

### Access the Application

| URL | Page |
|---|---|
| http://127.0.0.1:5500 | Home Page |
| http://127.0.0.1:5500/login.html | Login / Register |
| http://127.0.0.1:5500/dashboard.html | Dashboard (requires login) |
| http://127.0.0.1:5500/manage.html | Manage Students (requires login) |
| http://127.0.0.1:8000/docs | API Swagger Documentation |
| http://127.0.0.1:8000/health | Database Health Check |

---

## 🖥 Frontend Pages

### 1. `index.html` — Home Page
- Project title and description
- Navigation to all pages
- Feature highlights (Dashboard, CRUD, Security, Design)
- Detects login state and shows Dashboard or Login link

### 2. `about.html` — About Page
- Project objective and problem statement
- Target users (administrators, faculty, students)
- Technology stack overview
- Developer information

### 3. `login.html` — Authentication Page
- Tab-based Login / Register UI
- Login: email + password → receives JWT token
- Register: full name, email, role, password → creates account
- JWT stored in `localStorage` on success
- Redirects to dashboard after login

### 4. `dashboard.html` — Analytics Dashboard *(Protected)*
- Requires JWT token (redirects to login if missing)
- Shows: Total Students, Total Courses, Total Enrollments, System Status
- Recently added students table
- Welcome message decoded from JWT payload

### 5. `manage.html` — Student CRUD *(Protected)*
- Full student management interface
- Add new student (modal form)
- Edit existing student (pre-filled modal)
- Delete student (confirmation dialog)
- Search by name/email (live debounced search)
- Filter by course, year, status
- Pagination (10 students per page)

---

## 🔐 Security Architecture

| Feature | Implementation |
|---|---|
| **Password Hashing** | `bcrypt` with salt rounds (industry standard) |
| **Authentication** | JWT tokens (HS256 algorithm, 30-min expiry) |
| **Route Protection** | FastAPI `Depends(get_current_user)` on all protected endpoints |
| **CORS** | Explicit origin whitelist for all local dev ports |
| **Environment Secrets** | Loaded from `.env` file, never hardcoded in source |
| **Input Validation** | Pydantic schemas validate all request bodies automatically |

### How Authentication Works

```
1. User registers → password hashed with bcrypt → stored in DB
2. User logs in → bcrypt verifies password → JWT token issued
3. Frontend stores JWT in localStorage
4. Every protected API request sends: Authorization: Bearer <token>
5. Backend decodes JWT → finds user → allows or denies request
```

---

## 🐛 Known Issues & Troubleshooting

### ❌ "Network error. Make sure the backend is running"
**Cause:** Backend not running, or wrong IP being used.  
**Fix:**
1. Start backend: `uvicorn main:app --reload --host 127.0.0.1 --port 8000`
2. Always use `http://127.0.0.1:5500` (not `localhost:5500`) to access frontend
3. Always use `http://127.0.0.1:8000` for the backend

---

### ❌ CORS Error in Browser Console
**Cause:** Frontend running on IPv6 (`::1`) instead of IPv4 (`127.0.0.1`).  
**Fix:** Always start the frontend server with `--bind 127.0.0.1`:
```powershell
python -m http.server 5500 --bind 127.0.0.1
```

---

### ❌ `ValueError: password cannot be longer than 72 bytes`
**Cause:** `passlib` library is incompatible with `bcrypt >= 4.0`.  
**Fix:** Already resolved — the project now uses `bcrypt` directly instead of `passlib`.

---

### ❌ `ImportError: attempted relative import with no known parent package`
**Cause:** Running `python main.py` instead of using uvicorn.  
**Fix:** Always run with uvicorn from inside the `backend/` directory:
```powershell
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

### ❌ `getaddrinfo failed` / DNS error on Supabase connection
**Cause:** The direct connection URL (`db.xxx.supabase.co:5432`) may be blocked on some networks.  
**Fix:** The project uses the **Transaction Pooler** URL (port `6543`) which works on all networks.

---

### ❌ Git merge conflicts after `git push`
**Cause:** Changes pushed via GitHub API create commits that don't exist locally.  
**Fix:** Run once to sync:
```powershell
git fetch origin
git reset --hard origin/main
```

---

## 🔧 Environment Variables

Create `backend/.env` with the following:

```env
# Supabase Transaction Pooler URL
# Note: @ in password must be URL-encoded as %40
DATABASE_URL=postgresql+asyncpg://postgres.PROJECT_REF:PASSWORD@aws-1-REGION.pooler.supabase.com:6543/postgres

# JWT Secret Key (generate a strong random key for production)
SECRET_KEY=your_strong_secret_key_here

# JWT Algorithm
ALGORITHM=HS256

# Token expiry in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 📊 Supabase Project Details

| Field | Value |
|---|---|
| **Project Name** | Campus Connect |
| **Project Ref** | `vqoavyjepfjxrcxtrxkw` |
| **Region** | ap-south-1 (Mumbai) |
| **Pooler Host** | `aws-1-ap-south-1.pooler.supabase.com` |
| **Pooler Port** | `6543` (Transaction Pooler) |
| **Database** | `postgres` |

---

## 👨‍💻 Developer Information

| Field | Details |
|---|---|
| **Developer** | Hammad |
| **University** | University of Management and Technology (UMT) |
| **Course** | OSSD-Y9 (Object-Oriented Software System Design) |
| **GitHub** | [Vergil9/Hammad-Project](https://github.com/Vergil9/Hammad-Project) |
| **Year** | 2026 |

---

*© 2026 CampusConnect. Built for OSSD-Y9 Final Semester Project at UMT.*
