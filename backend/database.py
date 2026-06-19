import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load .env explicitly from the backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Fallback: also load from root directory if needed
load_dotenv()

# We get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please create backend/.env file.")

# Supabase Postgres database connection using asyncpg
engine = create_async_engine(DATABASE_URL, echo=False)

# Session factory for async sessions
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency for FastAPI to get a database session per request
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
