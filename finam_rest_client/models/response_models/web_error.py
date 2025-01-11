"""Ошибка запроса на сервер."""

from pydantic import BaseModel


class WebError(BaseModel):
    """
    Представление ошибки в ответе сервера.

    Возвращается в ответ на ошибочный запрос.
    """

    code: str | None = None
    message: str | None = None
    data: dict | None = None
