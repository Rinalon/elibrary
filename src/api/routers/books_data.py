from fastapi import APIRouter

from src.api.routers.factory import create_crud_router
from src.db.crud.books_data import *
from src.db.schemas.books_data import *

books_router = create_crud_router(
        prefix="/books",
        tag="books",
        crud_class=book_crud,
        response_schema=BookResponse,
        short_response_schema=BookShortResponse,
        create_schema=BookCreate,
        update_schema=BookUpdate,
        paginated=True,
)

authors_router = create_crud_router(
    prefix="/authors",
    tag="authors",
    crud_class=author_crud,
    response_schema=AuthorResponse,
    short_response_schema=AuthorShortResponse,
    create_schema=AuthorCreate,
    update_schema=AuthorUpdate,
    paginated=True,
)

genres_router = create_crud_router(
    prefix="/genres",
    tag="genres",
    crud_class=genre_crud,
    response_schema=GenreResponse,
    short_response_schema=GenreShortResponse,
    create_schema=GenreCreate,
    update_schema=GenreUpdate,
    paginated=False,
)

publishers_router = create_crud_router(
    prefix="/publishers",
    tag="publishers",
    crud_class=publisher_crud,
    response_schema=PublisherResponse,
    short_response_schema=PublisherShortResponse,
    create_schema=PublisherCreate,
    update_schema=PublisherUpdate,
    paginated=False,
)

language_router = create_crud_router(
    prefix="/languages",
    tag="languages",
    crud_class=language_crud,
    response_schema=LanguageResponse,
    short_response_schema=LanguageResponse,
    create_schema=LanguageCreate,
    update_schema=LanguageUpdate,
    paginated=False,
)

books_data_router = APIRouter()
books_data_router.include_router(books_router)
books_data_router.include_router(authors_router)
books_data_router.include_router(genres_router)
books_data_router.include_router(publishers_router)
books_data_router.include_router(language_router)