from src.db.crud import book_crud
from src.db.schemas import BookCreate, BookUpdate
from tests.data.book import base_book

async def test_create_book_valid(db_session):
    data = BookCreate(**base_book)
    new_book = await book_crud.create(db_session, data)

    assert new_book is not None
    assert new_book.title == base_book["title"]

async def test_update_book(db_session):
    data = BookCreate(**base_book)
    book = await book_crud.create(db_session, data)
    book_id = book.book_id
    upd_data = BookUpdate(title="Сестра")

    book = await book_crud.update(db_session, book_id, upd_data)
    assert book is not None
    assert book_id == book.book_id
    assert book.title != base_book["title"]

