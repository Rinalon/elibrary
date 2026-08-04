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
    ("min_fill", {
        k: v for k, v in base_book.items() if k not in [
            "description", "age_rating", "text_url", "cover_url"
    ]}),
    ("without_description", {k: v for k, v in base_book.items() if k != "description"}),
    ("without_age_rating", {k: v for k, v in base_book.items() if k != "age_rating"}),
    ("without_text_url", {k: v for k, v in base_book.items() if k != "text_url"}),
    ("without_cover_url", {k: v for k, v in base_book.items() if k != "cover_url"})
]

BOOK_INVALID_CASES = [
    ("missing_title", {k: v for k, v in base_book.items() if k != "title"}),
    ("missing_year", {k: v for k, v in base_book.items() if k != "year_of_publish"}),
    ("missing_publisher", {k: v for k, v in base_book.items() if k != "publisher_id"}),
    ("missing_language", {k: v for k, v in base_book.items() if k != "language_id"}),
    ("missing_price", {k: v for k, v in base_book.items() if k != "price"}),
    ("missing_authors", {k: v for k, v in base_book.items() if k != "author_ids"}),
    ("missing_genres", {k: v for k, v in base_book.items() if k != "genre_ids"}),
]