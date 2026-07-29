from db.models import Language, Publisher

from db.crud.books_data.books import BookCRUD
from db.crud.books_data.authors import AuthorCRUD
from db.crud.books_data.genres import GenreCRUD
from db.crud.base import BaseCRUD

# Экземпляры для моделей без специфической логики
language_crud = BaseCRUD(Language)
publisher_crud = BaseCRUD(Publisher)

# Экземпляры для моделей со специфической логикой
book_crud = BookCRUD()
author_crud = AuthorCRUD()
genre_crud = GenreCRUD()

__all__ = [
    'book_crud',
    'author_crud',
    'genre_crud',
    'language_crud',
    'publisher_crud',
]