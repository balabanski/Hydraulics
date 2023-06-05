from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship, Column, DateTime, text, JSON



sqlite_url = f"sqlite:///"+ settings.SQLITE_FILE_NAME

engine = create_engine(sqlite_url, echo=True)

# надо переделать
'''
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=settings.POOL_SIZE,
    pool_pre_ping=True,
    max_overflow=settings.MAX_OVERFLOW,
)
'''




SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def add_postgresql_extension() -> None:
    async with SessionLocal() as db:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        await db.execute(query)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async with SessionLocal() as session:
        yield session
