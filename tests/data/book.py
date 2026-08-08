from cytoolz import remove

from tests.data.utils import make_case

base_book = {
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

BOOK_VALID_CASES = [
    ("full_fill", base_book),
    ("min_fill", make_case(base_book, remove_keys=["description", "age_rating", "text_url", "cover_url"])),
    ("without_description", make_case(base_book, remove_keys=["description"])),
    ("without_age_rating",  make_case(base_book, remove_keys=["age_rating"])),
    ("without_text_url",  make_case(base_book, remove_keys=["text_url"])),
    ("without_cover_url",  make_case(base_book, remove_keys=["cover_url"]))
]

BOOK_INVALID_CASES = [
    ("missing_title", make_case(base_book, remove_keys=["title"])),
    ("missing_year", make_case(base_book, remove_keys=["year_of_publish"])),
    ("missing_publisher", make_case(base_book, remove_keys=["publisher_id"])),
    ("missing_language", make_case(base_book, remove_keys=["language_id"])),
    ("missing_price", make_case(base_book, remove_keys=["price"])),
    ("missing_authors", make_case(base_book, remove_keys=["author_ids"])),
    ("missing_genres", make_case(base_book, remove_keys=["genre_ids"])),

    ("short_title", make_case(base_book, updates={"title": ""})),
    ("big_title", make_case(base_book, updates={"title": "a" * 257})),
    ("big_description", make_case(base_book, updates={"description": "a" * 1025})),
    ("negative_year", make_case(base_book, updates={"year_of_publish": -1})),
    ("future_year", make_case(base_book, updates={"year_of_publish": 2116})),
    ("no_publisher", make_case(base_book, updates={"publisher_id": None})),
    ("no_language", make_case(base_book, updates={"language_id": None})),
    ("unknown_age_rating", make_case(base_book, updates={"age_rating": "21+"})),
    ("negative_price", make_case(base_book, updates={"price": -1})),
    ("too_long_cover_url", make_case(base_book, updates={"cover_url": "a" * 257})),
    ("too_long_text_url", make_case(base_book, updates={"text_url": "a" * 257})),
    ("void_authors", make_case(base_book, updates={"author_ids": []})),
    ("void_genres", make_case(base_book, updates={"genre_ids": []})),
]