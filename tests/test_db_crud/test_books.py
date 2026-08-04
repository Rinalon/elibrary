from db import book_crud
from db import BookCreate
from tests.data.book import base_book

async def test_create_book_valid(db_session):
    data = BookCreate(**base_book)
    new_book = await book_crud.create(db_session, data)

    assert new_book is not None
    assert new_book.title == base_book["title"]

