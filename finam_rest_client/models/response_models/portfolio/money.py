"""Денежная позиция."""

from decimal import Decimal

from pydantic import BaseModel

from finam_rest_client.models.common_types import Market


class Money(BaseModel):
    """
    Денежная позиция.

    Параметры:

    - market - рынок. Тип Market;
    - currency - код валюты;
    - balance - текущая позиция.
    """

    market: Market
    currency: str | None = None
    balance: Decimal
