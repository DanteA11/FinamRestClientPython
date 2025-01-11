"""Базовая модель ответа сервера."""

from pydantic import BaseModel

from .web_error import WebError


class BaseResponseModel(BaseModel):
    """Базовая модель ответа сервера."""

    error: WebError | None = None
