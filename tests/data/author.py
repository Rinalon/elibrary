without_books = {
    "author_name": "Сканави Марк Иванович",
    "author_info": "Cоветский математик, автор и редактор популярных сборников задач для поступающих в вузы, а также для старших классов средней общеобразовательной школы."
}

with_books = {
    "author_name": "Dr. Hopkins",
    "author_info": "Very very smart anthropologist",
    "books": [36]
}

CREATE_VALID_DATA = {
    "full_fill": with_books,
    "min_fill": without_books,
    "without_info": {k:v for k, v in with_books.items() if k != "author_info"},
}

CREATE_INVALID_DATA = {
    "missing_name": {k:v for k, v in with_books.items() if k != "author_name"},
    "unknown_fields": with_books | {"reward": "The Best Author of the World 3027"}
}