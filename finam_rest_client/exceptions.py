"""Исключения Api."""


class BaseApiException(Exception):
    """Базовая ошибка Api."""


class AuthenticationException(BaseApiException):
    """Исключение при ошибке проверки токена."""

    message = "Токен не прошел проверку подлинности."

    def __init__(self, message=None):
        message = message or self.message
        super().__init__(message)
