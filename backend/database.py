import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# We get the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

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
