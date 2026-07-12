from api.routers.book_pages import books_router
from api.routers.authors import author_router
from api.routers.genres import genre_router

__all__ = [
    "books_router",
    "author_router",
    "genre_router",
]