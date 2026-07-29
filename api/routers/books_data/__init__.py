from fastapi import APIRouter

from api.routers.books_data.books import books_router
from api.routers.books_data.authors import author_router
from api.routers.books_data.genres import genre_router
from api.routers.books_data.dictionaries import publisher_router


books_data_router = APIRouter()
books_router.include_router(books_router, prefix="/books", tags=["books"])
books_router.include_router(author_router, prefix="/authors", tags=["authors"])
books_router.include_router(genre_router, prefix="/genres", tags=["genres"])
books_router.include_router(publisher_router, prefix="/publishers", tags=["publishers"])


__all__ = ['books_data_router']