import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
from dotenv import load_dotenv

# Load .env from the backend directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc, func
import bcrypt
from jose import JWTError, jwt

# Import from our local modules
import database, models, schemas

# Initialize FastAPI app
app = FastAPI(
    title="CampusConnect API",
    description="Student Management System for OSSD-Y9 at UMT",
    version="1.0.0"
)

# Global DB status flag (set during startup)
db_connected: bool = False

# CORS — allow all origins for the deployed API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Authentication & Security Configuration ---

SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- Helper Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(models.User).where(models.User.email == token_data.email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    global db_connected
    try:
        async with database.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        db_connected = True
        print("INFO:     ✅ Connected to Supabase (Mumbai ap-south-1). Tables initialized.")
    except Exception as e:
        db_connected = False
        print(f"ERROR:    ❌ Database connection failed: {str(e)}")
        print("ERROR:    The app is running but database operations will fail.")

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "project": "CampusConnect API",
        "description": "Student Management System for OSSD-Y9 at UMT",
        "status": "Running",
        "docs": "/docs"
    }

@app.get("/health", tags=["Root"])
async def health_check():
    return {
        "status": "ok" if db_connected else "degraded",
        "database": "connected" if db_connected else "unreachable",
        "supabase_project": "vqoavyjepfjxrcxtrxkw",
        "region": "ap-south-1 (Mumbai)"
    }

# --- Auth Routes ---

@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    # Check if user exists
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token, tags=["Auth"])
async def login(form_data: schemas.UserLogin, db: AsyncSession = Depends(database.get_db)):
    # Authenticate user
    result = await db.execute(select(models.User).where(models.User.email == form_data.email))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Student Routes ---

@app.post("/api/students", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Check if student email exists
    result = await db.execute(select(models.Student).where(models.Student.email == student.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Student email already exists")

    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    # Check if the course already exists
    course_result = await db.execute(select(models.Course).where(models.Course.name == new_student.course))
    course = course_result.scalars().first()

    if not course:
        # Create a new course if it doesn't exist
        course_code = "".join(word[0].upper() for word in new_student.course.split())
        course = models.Course(name=new_student.course, code=course_code, description=f"{new_student.course} Degree Program")
        db.add(course)
        await db.commit()
        await db.refresh(course)

    # Enroll the student in the course
    enrollment = models.Enrollment(
        student_id=new_student.id,
        course_id=course.id,
        user_id=current_user.id,
        status="enrolled"
    )
    db.add(enrollment)
    await db.commit()

    return new_student

@app.get("/api/students", response_model=schemas.StudentPaginatedResponse, tags=["Students"])
async def get_students(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    skip = (page - 1) * limit
    
    # Get total count
    count_result = await db.execute(select(func.count(models.Student.id)))
    total_count = count_result.scalar_one()
    
    # Get paginated data
    result = await db.execute(select(models.Student).order_by(desc(models.Student.created_at)).offset(skip).limit(limit))
    students = result.scalars().all()
    
    return {"total": total_count, "page": page, "limit": limit, "students": students}

@app.get("/api/students/search", response_model=List[schemas.StudentResponse], tags=["Students"])
async def search_students(q: str = Query(..., min_length=1), db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    search_term = f"%{q}%"
    result = await db.execute(
        select(models.Student).where(
            or_(models.Student.name.ilike(search_term), models.Student.email.ilike(search_term))
        )
    )
    return result.scalars().all()

@app.get("/api/students/filter", response_model=List[schemas.StudentResponse], tags=["Students"])
async def filter_students(
    course: Optional[str] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = select(models.Student)
    if course:
        query = query.where(models.Student.course.ilike(f"%{course}%"))
    if year:
        query = query.where(models.Student.year == year)
    if status:
        query = query.where(models.Student.status == status)
        
    result = await db.execute(query.order_by(desc(models.Student.created_at)))
    return result.scalars().all()

@app.get("/api/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
async def get_student(student_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/api/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
async def update_student(student_id: int, student_update: schemas.StudentUpdate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student

@app.delete("/api/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
async def delete_student(student_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    await db.delete(student)
    await db.commit()
    return {"detail": "Student deleted successfully"}

# --- Dashboard Routes ---

@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats, tags=["Dashboard"])
async def get_dashboard_stats(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    students_count = await db.execute(select(func.count(models.Student.id)))
    courses_count = await db.execute(select(func.count(models.Course.id)))
    enrollments_count = await db.execute(select(func.count(models.Enrollment.id)))
    
    recent_result = await db.execute(select(models.Student).order_by(desc(models.Student.created_at)).limit(5))
    
    return {
        "total_students": students_count.scalar_one(),
        "total_courses": courses_count.scalar_one(),
        "total_enrollments": enrollments_count.scalar_one(),
        "recent_students": recent_result.scalars().all()
    }

# --- Course Routes ---

@app.post("/api/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Course).where(models.Course.code == course.code))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Course code already exists")
        
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@app.get("/api/courses", response_model=List[schemas.CourseResponse], tags=["Courses"])
async def get_courses(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Course).order_by(models.Course.name))
    return result.scalars().all()

# --- Exception Handler ---

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )