from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.core.config import settings
from sqlmodel import text


engine = create_async_engine(settings.sqlite_url, echo=settings.DEBUG)

# надо переделать
'''
engine = create_engine(
    settings.postgresql_url,
    echo=settings.DEBUG,
    future=True,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    pool_pre_ping=True,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
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
