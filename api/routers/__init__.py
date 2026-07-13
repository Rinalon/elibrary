from fastapi import APIRouter

from api.routers.books import books_router
from api.routers.authors import author_router
from api.routers.genres import genre_router
from api.routers.publishers import publisher_router


routers = APIRouter()
routers.include_router(books_router)
routers.include_router(author_router)
routers.include_router(genre_router)
routers.include_router(publisher_router)

__all__ = [
    'routers'
]