from src.db.schemas.books_data.books import *
from tests.data.book import *
from pydantic import ValidationError
import pytest

def create_flat_cases(params: list[tuple]):
    flat = []
    for schema, cases in params:
        for case_name, data in cases:
            flat.append((schema, case_name, data))
    return flat

valid_cases_flat = create_flat_cases([
        (BookCreate, BOOK_CREATE_VALID_CASES),
        (BookUpdate, BOOK_UPDATE_VALID_CASES),
        (BookResponse, BOOK_RESPONSE_VALID_CASES),
        (BookShortResponse, BOOK_RESPONSE_VALID_CASES),
        (BookFilter, BOOK_FILTER_VALID_CASES),
])

invalid_cases_flat = create_flat_cases([
    (BookCreate, BOOK_CREATE_INVALID_CASES),
    (BookUpdate, BOOK_INVALID_CASES),
    (BookFilter, FILTER_INVALID_CASES),
])

@pytest.mark.parametrize("schema,case,data", valid_cases_flat)
def test_valid_book(schema, case, data):
    schema(**data)

@pytest.mark.parametrize("schema,case,data", invalid_cases_flat)
def test_invalid_book(schema, case, data):
    with pytest.raises(ValidationError) as exc_info:
        schema(**data)

