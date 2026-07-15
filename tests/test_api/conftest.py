import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

@pytest.fixture(scope="function")
async def async_client():
    """Фикстура с переопределнием подключения к БД."""
    from main import app
    from core import get_db, settings

    test_engine = create_async_engine(
        url=settings.database_url_async,
        echo=False
    )

    test_session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with test_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000",
    ) as client:
        yield client


    app.dependency_overrides.clear()
    await test_engine.dispose()