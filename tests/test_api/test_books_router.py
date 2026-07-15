import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint,expected_status", [
    ("/books", 307),
    ("/books/", 200),
    ("/books/1", 200),
    ("/books/999", 404),
    ("/books/abc", 422),
])
async def test_books_endpoints(async_client, endpoint, expected_status):
    response = await async_client.get(endpoint)
    assert response.status_code == expected_status