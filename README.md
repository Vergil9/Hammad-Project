# CampusConnect - Student Management System

CampusConnect is a modern, high-performance Student Management System built as a final semester project for OSSD-Y9 at the University of Management and Technology. It provides a centralized, secure platform for administrators and faculty to manage student records, courses, and enrollments.

## Problem Statement and Objective

Many universities rely on outdated paper-based systems or fragmented legacy digital tools that are slow, insecure, and hard to navigate. The objective of CampusConnect is to resolve these inefficiencies by offering a unified, robust, and user-friendly web application. The platform streamlines CRUD operations for student records while providing an analytical dashboard to track university metrics in real-time.

## Technology Stack

- **Frontend**: HTML5, CSS3 (Custom Variables, Flexbox/Grid, Glassmorphism), Vanilla JavaScript (ES6+). No external frontend frameworks were used.
- **Backend**: FastAPI (Python 3) for asynchronous, high-performance API endpoints.
- **Database**: PostgreSQL hosted on Supabase, interacting via SQLAlchemy 2.0 ORM and `asyncpg`.
- **Security**: JWT (JSON Web Tokens) for authentication, `passlib` (bcrypt) for password hashing.

## Setup Instructions (Local Development)

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- A modern web browser

### 1. Backend Setup
1. Open a terminal and navigate to the project directory: `cd "Hammad Project"`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Create a `.env` file in the root directory using the `.env.example` file as a template. Make sure to provide the actual `DATABASE_URL` for your Supabase Postgres database.
6. Run the FastAPI server: `uvicorn backend.main:app --reload`
   The backend will start at `http://localhost:8000`. 
   *Note: Upon first startup, SQLAlchemy will automatically create all necessary tables in the Supabase database.*

### 2. Frontend Setup
The frontend uses plain HTML/JS and doesn't require a build step.
1. You can simply open `frontend/index.html` directly in your browser.
2. Alternatively, serve it using a simple HTTP server:
   `cd frontend && python -m http.server 3000`
   Then visit `http://localhost:3000` in your browser.

## API Endpoint Documentation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | Root endpoint returning API status | No |
| `POST` | `/api/auth/register` | Register a new user | No |
| `POST` | `/api/auth/login` | Authenticate user & get JWT token | No |
| `POST` | `/api/students` | Create a new student record | Yes |
| `GET` | `/api/students` | View all students (paginated) | Yes |
| `GET` | `/api/students/{id}` | View a single student by ID | Yes |
| `PUT` | `/api/students/{id}` | Update an existing student | Yes |
| `DELETE` | `/api/students/{id}`| Delete a student record | Yes |
| `GET` | `/api/students/search`| Search students by name/email | Yes |
| `GET` | `/api/students/filter`| Filter students by course/year/status | Yes |
| `GET` | `/api/dashboard/stats`| Get overall statistics for dashboard | Yes |
| `POST` | `/api/courses` | Create a new course | Yes |
| `GET` | `/api/courses` | View all courses | Yes |

*Note: You can view the interactive Swagger documentation by running the backend and visiting `http://localhost:8000/docs`.*

## Database Schema Description

The system uses a relational PostgreSQL database.
- **users**: Stores authentication credentials, roles, and profile information.
- **students**: Stores core student demographic and academic data.
- **courses**: Stores course catalog data.
- **enrollments**: A junction table linking students and courses.

Please refer to `DATABASE_SCHEMA.md` for detailed table structures.

## Environment Variables Needed

Create a `.env` file in the root with the following:
```
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SECRET_KEY=your_strong_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
