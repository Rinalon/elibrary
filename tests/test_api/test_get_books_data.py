import pytest

@pytest.mark.parametrize(
    "base_url",
    [
        "/books",
        "/authors",
        "/genres",
        "/publishers",
        "/languages"
    ]
)
async def test_get_endpoints(async_client, base_url):
    endpoints = [
        ("", 307),
        ("/", 200),
        ("/99", 404), # на тестовой базе такого id ни у одной из таблиц нет
        ("/1", 200),
        ("/abc", 422),
    ]
    for endpoint, expected_status in endpoints:
        response = await async_client.get(f"{base_url}{endpoint}")
        assert response.status_code == expected_status