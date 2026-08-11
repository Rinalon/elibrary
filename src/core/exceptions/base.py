class AppError(Exception):
    """Базовый класс для ошибок приложения"""
    def __init__(self, message: str = "An application error occurred"):
        self.message = message
        super().__init__(message)

class NotFoundError(AppError):
    """Ресурс не найден."""
    pass

class ConflictError(Exception):
    """Уже сущетсвует"""
    pass