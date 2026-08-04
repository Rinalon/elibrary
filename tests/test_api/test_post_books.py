import pytest
from tests.data.book import BOOK_VALID_CASES, BOOK_INVALID_CASES

@pytest.mark.parametrize(
    "case_name,data",
    BOOK_VALID_CASES,
    ids=[case[0] for case in BOOK_VALID_CASES]
)
async def test_create_book_valid(async_client, case_name, data):
    response = await async_client.post("/books/", json=data)
    if response.status_code != 200:
        print(f"❌ Ошибка для {case_name}:")
        print(f"Статус: {response.status_code}")
        print(f"Тело ответа: {response.text}")
    assert response.status_code == 200

@pytest.mark.parametrize(
    "case_name,data",
    BOOK_INVALID_CASES,
    ids=[case[0] for case in BOOK_INVALID_CASES]
)
async def test_create_book_invalid(async_client, case_name, data):
    response = await async_client.post("/books/", json=data)
    assert response.status_code == 422