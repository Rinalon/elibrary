import pytest

@pytest.mark.asyncio
async def test_get_books(async_client):
    response = await async_client.get("/books/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_book(async_client):
    response = await async_client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] is not None
