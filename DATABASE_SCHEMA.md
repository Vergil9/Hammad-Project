# Database Schema

The CampusConnect application relies on a robust PostgreSQL database hosted on Supabase. We use SQLAlchemy 2.0 ORM to define and manage our database structure asynchronously.

## Tables

### 1. `users`
Stores all system users including administrators, faculty, and students who have accounts.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `email` | String | Unique, Index, Not Null | User's email (used for login) |
| `hashed_password` | String | Not Null | bcrypt hashed password |
| `full_name` | String | Not Null | User's full name |
| `role` | Enum | Default: 'student' | admin, faculty, or student |
| `is_active` | Boolean | Default: True | Account status |
| `created_at` | DateTime | Default: func.now() | Timestamp of account creation |

### 2. `students`
Stores core student records. This is separate from `users` because a student record can exist in the system even if the student hasn't registered an account yet, and vice versa.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `name` | String | Not Null | Student's full name |
| `email` | String | Unique, Index, Not Null | Student's contact email |
| `course` | String | Not Null | Primary course/major |
| `year` | Integer | Not Null | Academic year (1-4) |
| `status` | Enum | Default: 'active' | active, inactive, graduated |
| `created_at` | DateTime | Default: func.now() | Record creation timestamp |
| `updated_at` | DateTime | OnUpdate: func.now()| Last modification timestamp |

### 3. `courses`
Stores the catalog of available courses.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `name` | String | Not Null | Full course name |
| `code` | String | Unique, Index, Not Null | Course identifier (e.g. CS101) |
| `description` | Text | Nullable | Detailed description |
| `created_at` | DateTime | Default: func.now() | Record creation timestamp |

### 4. `enrollments`
A junction/association table linking students to courses.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier |
| `student_id` | Integer | Foreign Key, Not Null| References `students.id` |
| `course_id` | Integer | Foreign Key, Not Null| References `courses.id` |
| `user_id` | Integer | Foreign Key, Nullable | Tracks the user who enrolled them |
| `enrollment_date` | DateTime| Default: func.now() | Date of enrollment |
| `status` | String | Default: 'enrolled' | Enrollment status |

## Relationships

- **User to Enrollments**: One-to-Many (`User.enrollments`). A user (admin/faculty) can process many enrollments.
- **Student to Enrollments**: One-to-Many (`Student.enrollments`). A student can be enrolled in multiple courses. When a student is deleted, their enrollments are cascade deleted (`delete-orphan`).
- **Course to Enrollments**: One-to-Many (`Course.enrollments`). A course has many enrollments. When a course is deleted, its enrollments are cascade deleted (`delete-orphan`).

## Indexes
Proper indexes are placed on primary keys (`id`) and frequently searched columns like `email` (in `users` and `students`) and `code` (in `courses`) to ensure fast query execution even as the database scales.
