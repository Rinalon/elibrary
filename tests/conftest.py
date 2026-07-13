import sys
from pathlib import Path

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
from main import app

@pytest_asyncio.fixture
async def async_client():
    """Фикстура, предоставляющая асинхронный HTTP-клиент для тестов."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        yield client