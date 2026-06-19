from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models import UserRole, StudentStatus

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.student

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Student Schemas ---
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    course: str
    year: int = Field(ge=1, le=5)
    status: StudentStatus = StudentStatus.active

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[StudentStatus] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StudentPaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    students: List[StudentResponse]

# --- Course Schemas ---
class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Enrollment Schemas ---
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: str = "enrolled"

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrollment_date: datetime

    class Config:
        from_attributes = True

# --- Dashboard Stats Schema ---
class DashboardStats(BaseModel):
    total_students: int
    total_courses: int
    total_enrollments: int
    recent_students: List[StudentResponse]
