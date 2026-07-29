from db.crud.books_data.books import BookCRUD
from db.crud.books_data.authors import AuthorCRUD
from db.crud.books_data.genres import GenreCRUD

__all__ = [
    "BookCRUD",
    "AuthorCRUD",
    "GenreCRUD",
]