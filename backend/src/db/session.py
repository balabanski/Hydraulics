from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.src.core.config import settings
from sqlmodel import text

if settings.DATABASE == "postgres":
    engine = create_async_engine(
        settings.POSTGRES_URL,
        echo=settings.DEBUG,
        future=True,
        pool_size=settings.POOL_SIZE,
        pool_pre_ping=True,
        max_overflow=settings.MAX_OVERFLOW,
    )
elif settings.DATABASE == "sqlite":
    engine = create_async_engine(settings.sqlite_url, echo=settings.DEBUG)


SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def add_postgresql_extension() -> None:
    async with SessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await db.execute(query)


"""
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async with SessionLocal() as session:
        return session
"""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        return db
    except:
        db.rollback()
    finally:
        await db.close()
