from src.db.schemas import AuthorShortResponse, GenreShortResponse, ReviewResponse, BookUpdate
from tests.data.utils import make_case

# базовая для CREATE и UPDATE
base_cu_book = {
    "title": "Айвенго",
    "description": "Один из первых исторических романов",
    "year_of_publish": 2016,
    "publisher_id": 1,
    "language_id": 1,
    "age_rating": "12+",
    "price": 599.99,
    "text_url": "https://example.com/aivengo.pdf",
    "cover_url": "https://example.com/cover.jpg",
    "author_ids": [5],
    "genre_ids": [1, 2, 3, 9]
}

# базовая для RESPONSE
base_r_book = {
    "book_id": 2,
    "title": "Айвенго",
    "description": "Один из первых исторических романов",
    "year_of_publish": 2016,
    "age_rating": "12+",
    "publisher_name": "Эксмо",
    "language_name": "Русский",
    "price": 599.99,
    "text_url": "https://example.com/aivengo.pdf",
    "cover_url": "https://example.com/cover.jpg",
    "watched": 5,
    "rating": 3.7,
    "authors": [AuthorShortResponse(author_id=5, author_name="")],
    "genres": [GenreShortResponse(genre_id=4, title="")],
    "reviews": [ReviewResponse(user_name="", rating=4)],
}

# база для BookFilter
base_filter = {
        "title": "Война",
        "author_id": 1,
        "genre_id": 1,
        "publisher_id": 1,
        "language_id": 1,
        "age_rating": "16+",
        "min_price": 0,
        "max_price": 0,
        "limit": 10,
        "offset": 0,
}

BOOK_CREATE_VALID_CASES = [
    ("full_fill", base_cu_book),
    ("min_fill", make_case(base_cu_book, remove_keys=["description", "age_rating", "text_url", "cover_url"])),
    ("without_description", make_case(base_cu_book, remove_keys=["description"])),
    ("without_age_rating",  make_case(base_cu_book, remove_keys=["age_rating"])),
    ("without_text_url",  make_case(base_cu_book, remove_keys=["text_url"])),
    ("without_cover_url",  make_case(base_cu_book, remove_keys=["cover_url"]))
]

BOOK_UPDATE_VALID_CASES = BOOK_CREATE_VALID_CASES.copy()
BOOK_UPDATE_VALID_CASES.append(("void", {}))

BOOK_RESPONSE_VALID_CASES = [
    ("full_fill", base_r_book),
    ("min_fill", make_case(base_r_book, remove_keys=[
    "description", "age_rating", "text_url", "cover_url",
    "authors", "genres", "reviews", "rating"
    ])),
    ("without_description", make_case(base_r_book, remove_keys=["description"])),
    ("without_age_rating",  make_case(base_r_book, remove_keys=["age_rating"])),
    ("without_text_url",  make_case(base_r_book, remove_keys=["text_url"])),
    ("without_cover_url",  make_case(base_r_book, remove_keys=["cover_url"])),
    ("without_authors", make_case(base_r_book, remove_keys=["authors"])),
    ("without_genres", make_case(base_r_book, remove_keys=["genres"])),
    ("without_reviews", make_case(base_r_book, remove_keys=["reviews"])),
    ("without_rating", make_case(base_r_book, remove_keys=["rating"])),
]

BOOK_FILTER_VALID_CASES = [
    ("full_fill", base_filter),
    ("min_fill", {}),
    ("just_title", {"title":"Война"}),
    ("just_author", {"author_id": 1}),
    ("just_genre", {"genre_id": 1}),
    ("just_age_rating", {"age_rating": "12+"}),
    ("just_publisher", {"publisher_id": 1}),
    ("just_language", {"language_id": 1}),
    ("just_min_price", {"min_price": 0}),
    ("just_max_price", {"max_price": 0}),
    ("just_range", {"min_price": 0, "max_price": 1000}),
]

BOOK_INVALID_CASES = [
    ("short_title", make_case(base_cu_book, updates={"title": ""})),
    ("big_title", make_case(base_cu_book, updates={"title": "a" * 257})),
    ("big_description", make_case(base_cu_book, updates={"description": "a" * 1025})),
    ("negative_year", make_case(base_cu_book, updates={"year_of_publish": -1})),
    ("future_year", make_case(base_cu_book, updates={"year_of_publish": 2116})),
    ("unknown_age_rating", make_case(base_cu_book, updates={"age_rating": "21+"})),
    ("negative_price", make_case(base_cu_book, updates={"price": -1})),
    ("too_long_cover_url", make_case(base_cu_book, updates={"cover_url": "a" * 257})),
    ("too_long_text_url", make_case(base_cu_book, updates={"text_url": "a" * 257})),
]

BOOK_CREATE_INVALID_CASES = [
    ("missing_title", make_case(base_cu_book, remove_keys=["title"])),
    ("missing_year", make_case(base_cu_book, remove_keys=["year_of_publish"])),
    ("missing_publisher", make_case(base_cu_book, remove_keys=["publisher_id"])),
    ("missing_language", make_case(base_cu_book, remove_keys=["language_id"])),
    ("missing_price", make_case(base_cu_book, remove_keys=["price"])),
    ("no_publisher", make_case(base_cu_book, updates={"publisher_id": None})),
    ("no_language", make_case(base_cu_book, updates={"language_id": None})),
] + BOOK_INVALID_CASES

FILTER_INVALID_CASES = [
    ("short_title", {"title": ""}),
    ("big_title", {"title": "a"*257}),
    ("negative_min_price", {"min_price": -1}),
    ("negative_max_price", {"max_price": -1}),
    ("negative_range", {"min_price": 2, "max_price": 1}),
    ("negative_offset", {"offset": -1}),
    ("big_limit", {"limit": 21}),
    ("small_limit", {"limit": 4}),
]