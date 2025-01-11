"""Модель запроса инструментов."""

from pydantic import BaseModel

__all__ = ("SecuritiesRequest",)


class SecuritiesRequest(BaseModel):
    """
    Модель запроса инструментов.

    Параметры:

    - board - Режим торгов (необязательное поле для фильтрации).
    - seccode - Тикер инструмента (необязательное поле для фильтрации).
    """

    board: str | None = None
    seccode: str | None = None
