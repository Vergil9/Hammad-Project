# Project Structure

This document outlines the directory structure of the CampusConnect Student Management System. The project is strictly divided into frontend and backend components.

```text
Hammad Project/
│
├── backend/
│   ├── database.py       # SQLAlchemy engine, session maker, and DB dependency injection
│   ├── main.py           # FastAPI application instance, CORS setup, and all API routes
│   ├── models.py         # SQLAlchemy database models representing Postgres tables
│   ├── requirements.txt  # Python package dependencies
│   └── schemas.py        # Pydantic models for request validation and response serialization
│
├── frontend/
│   ├── about.html        # Information about the project, target audience, and tech stack
│   ├── dashboard.html    # Protected route displaying statistical analytics
│   ├── index.html        # Public landing page highlighting features
│   ├── login.html        # Authentication forms (login/register) saving JWT to localStorage
│   ├── manage.html       # Full CRUD interface for student records with advanced filters
│   └── style.css         # Shared stylesheet defining colors, typography, and glassmorphism UI
│
├── screenshots/          # Directory reserved for project demonstration screenshots
│   └── .keep             # Git keep file
│
├── .env.example          # Template for required environment variables
├── DATABASE_SCHEMA.md    # Documentation of the database tables and relations
├── PROJECT_STRUCTURE.md  # Detailed breakdown of files and their purposes (this file)
└── README.md             # Project overview, setup instructions, and API documentation
```

## Description of Files

### Backend
- **`main.py`**: The entry point for the FastAPI application. It includes global exception handlers, startup events that create database tables, security dependencies, and 12+ API endpoints covering auth, students, courses, and dashboard stats.
- **`database.py`**: Sets up `create_async_engine` and `async_sessionmaker` required for asynchronous database interactions via `asyncpg`.
- **`models.py`**: Contains SQLAlchemy declarative base classes (`User`, `Student`, `Course`, `Enrollment`). Defines schema structures and ORM relationships.
- **`schemas.py`**: Contains Pydantic models (e.g., `StudentCreate`, `UserResponse`) used extensively in `main.py` to auto-validate incoming JSON data and serialize outgoing responses.
- **`requirements.txt`**: Lists exact dependencies required, such as `fastapi`, `sqlalchemy[asyncio]`, `passlib[bcrypt]`, and `python-jose`.

### Frontend
- **`style.css`**: Utilizes CSS variables for theming, implementing a modern aesthetic with dark mode and glassmorphism (translucent backgrounds with blur effects).
- **`index.html` & `about.html`**: Static informational pages for public visitors.
- **`login.html`**: Uses `fetch()` to call the `/api/auth/register` and `/api/auth/login` endpoints. Stores the resulting JWT in `localStorage`.
- **`dashboard.html` & `manage.html`**: Protected pages. They read the JWT from `localStorage` and include it in the `Authorization: Bearer <token>` header of every API request. If unauthorized, they automatically redirect the user back to the login page.
