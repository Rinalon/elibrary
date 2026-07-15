import sys
import asyncio
import platform
import pytest
from pathlib import Path

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
