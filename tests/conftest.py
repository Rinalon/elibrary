import sys
import asyncio
import platform
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture(scope="session")
def event_loop():
    """Создаёт новый event loop для тестовой сессии."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)  # Важно: установить loop как текущий
    yield loop
    loop.close()


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