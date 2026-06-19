import os
import socket
from pathlib import Path
from urllib.parse import urlparse
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

def is_postgres_reachable(url: str, timeout: int = 3) -> bool:
    try:
        # Strip scheme so urlparse handles it consistently
        clean_url = url.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://")
        parsed = urlparse(clean_url)
        host = parsed.hostname
        port = parsed.port or 5432
        if not host:
            return False
        # Try to resolve and connect
        with socket.create_connection((host, port), timeout=timeout):
            pass
        return True
    except Exception as e:
        print(f"Connection check failed: {e}")
        return False

# Auto-detect logic: try postgres, fallback to sqlite
if DATABASE_URL.startswith("postgresql"):
    if is_postgres_reachable(DATABASE_URL):
        print("INFO: Successfully reached PostgreSQL host. Using PostgreSQL.")
        engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"ssl": True})
    else:
        print("WARNING: PostgreSQL is unreachable. Falling back to local SQLite.")
        DATABASE_URL = "sqlite+aiosqlite:///./fallback.db"
        engine = create_async_engine(DATABASE_URL, echo=False)
else:
    # If explicitly set to sqlite or something else
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
