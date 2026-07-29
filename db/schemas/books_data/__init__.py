from db.schemas.books_data.books import (
    BookCreate,
    BookEdit,
    UserBookUpdate,
    BookResponse,
    BookFilter,
    BookShortResponse,
)

from db.schemas.books_data.reviews import (
    ReviewCreate,
    ReviewEdit,
    ReviewResponse
)

from db.schemas.books_data.dictionaries import (
    LanguageResponse,
    LanguageCreate,
    PublisherResponse,
    PublisherShortResponse,
    PublisherCreate
)

from db.schemas.books_data.genres import (
    GenreResponse,
    GenreShortResponse,
    GenreCreate,
)

from db.schemas.books_data.authors import (
    AuthorShortResponse,
    AuthorResponse,
    AuthorCreate
)


BookResponse.model_rebuild()
AuthorResponse.model_rebuild()
GenreResponse.model_rebuild()
PublisherResponse.model_rebuild()

__all__ = [
    'BookCreate',
    'BookEdit',
    'UserBookUpdate',
    'BookResponse',
    'BookFilter',
    'ReviewCreate',
    'ReviewEdit',
    'ReviewResponse',
    'GenreResponse',
    'AuthorResponse',
    'LanguageResponse',
    'PublisherResponse',
    'GenreShortResponse',
    'AuthorShortResponse',
    'BookShortResponse',
    'PublisherShortResponse',
    'AuthorCreate',
    'GenreCreate',
    'PublisherCreate',
    'LanguageCreate',
]

