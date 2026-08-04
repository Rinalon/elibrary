import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.config import settings
from db import Base


@pytest.fixture(scope="function")
async def db_session():
    """Создаёт тестовую сессию БД для CRUD-тестов."""

    engine = create_async_engine(
        settings.database_url_async,
        echo=False,
    )

    session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        yield session

    await engine.dispose()