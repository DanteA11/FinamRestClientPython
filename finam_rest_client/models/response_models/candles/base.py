"""Базовая модель для ответа на запрос свечей."""

from pydantic import BaseModel

from finam_rest_client.models.common_types import FinamDecimal


class BaseCandle(BaseModel):
    """Базовая модель для ответа на запрос свечей."""

    open: FinamDecimal
    close: FinamDecimal
    high: FinamDecimal
    low: FinamDecimal
    volume: int
