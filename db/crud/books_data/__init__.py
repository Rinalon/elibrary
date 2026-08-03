from db.crud.books_data.books import BookCRUD
from db.crud.books_data.authors import AuthorCRUD
from db.crud.books_data.genres import GenreCRUD
from db.crud.books_data.publishers import PublisherCRUD
__all__ = [
    "BookCRUD",
    "AuthorCRUD",
    "GenreCRUD",
    "PublisherCRUD"
]