import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load .env explicitly from the backend directory (must run before os.getenv)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Fallback: also try loading from the root project directory
load_dotenv()

# Read the DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Please create backend/.env with the correct Supabase URL."
    )

# Create async SQLAlchemy engine — no connect_args, no sslmode
# The Supabase Transaction Pooler (port 6543) handles SSL natively
try:
    engine = create_async_engine(DATABASE_URL, echo=False)
except Exception as e:
    raise RuntimeError(f"Failed to create database engine: {e}")

# Session factory for async database sessions
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all SQLAlchemy ORM models
Base = declarative_base()


# FastAPI dependency — yields a DB session per request
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
