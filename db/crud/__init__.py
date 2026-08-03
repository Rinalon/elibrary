from db.models import (
    Language,
    Publisher,
    Book,
    Author,
    Genre
)
from db.crud.books_data import (
    BookCRUD,
    AuthorCRUD,
    GenreCRUD,
    PublisherCRUD
)
from db.crud.base import BaseCRUD

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