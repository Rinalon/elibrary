from fastapi import APIRouter

from api.routers.factory import create_crud_router
from db.crud import (
    book_crud,
    author_crud,
    genre_crud,
    publisher_crud,
    language_crud
)
from db.schemas import (
    BookCreate, BookShortResponse, BookResponse,
    AuthorCreate,  AuthorShortResponse, AuthorResponse,
    GenreCreate, GenreShortResponse, GenreResponse,
    PublisherCreate, PublisherShortResponse, PublisherResponse,
    LanguageCreate,  LanguageResponse
)

books_router = create_crud_router(
        prefix="/books",
        tag="books",
        crud_class=book_crud,
        response_schema=BookResponse,
        short_response_schema=BookShortResponse,
        create_schema=BookCreate,
        paginated=True,
)

authors_router = create_crud_router(
    prefix="/authors",
    tag="authors",
    crud_class=author_crud,
    response_schema=AuthorResponse,
    short_response_schema=AuthorShortResponse,
    create_schema=AuthorCreate,
    paginated=True,
)

genres_router = create_crud_router(
    prefix="/genres",
    tag="genres",
    crud_class=genre_crud,
    response_schema=GenreResponse,
    short_response_schema=GenreShortResponse,
    create_schema=GenreCreate,
    paginated=False,
)

publishers_router = create_crud_router(
    prefix="/publishers",
    tag="publishers",
    crud_class=publisher_crud,
    response_schema=PublisherResponse,
    short_response_schema=PublisherShortResponse,
    create_schema=PublisherCreate,
    paginated=False,
)

language_router = create_crud_router(
    prefix="/languages",
    tag="languages",
    crud_class=language_crud,
    response_schema=LanguageResponse,
    short_response_schema=LanguageResponse,
    create_schema=LanguageCreate,
    paginated=False,
)

books_data_router = APIRouter()
books_data_router.include_router(books_router)
books_data_router.include_router(authors_router)
books_data_router.include_router(genres_router)
books_data_router.include_router(publishers_router)
books_data_router.include_router(language_router)