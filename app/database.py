from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./ai_agent.db"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class
Base = declarative_base()