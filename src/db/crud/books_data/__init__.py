from src.db.models import (
    Language,
    Publisher,
    Book,
    Author,
    Genre
)

from src.db.crud.books_data.books import BookCRUD
from src.db.crud.books_data.authors import AuthorCRUD
from src.db.crud.books_data.genres import GenreCRUD
from src.db.crud.books_data.publishers import PublisherCRUD
from src.db.crud.base import BaseCRUD

# Экземпляры для моделей без специфической логики
language_crud = BaseCRUD(Language)

# Экземпляры для моделей со специфической логикой
book_crud = BookCRUD(Book)
author_crud = AuthorCRUD(Author)
genre_crud = GenreCRUD(Genre)
publisher_crud = PublisherCRUD(Publisher)

__all__ = [
    'book_crud',
    'author_crud',
    'genre_crud',
    'language_crud',
    'publisher_crud',
]