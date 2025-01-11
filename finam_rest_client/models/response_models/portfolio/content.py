"""Наполнение портфеля."""

from pydantic import BaseModel, Field


class Content(BaseModel):
    """
    Наполнение портфеля.

    Параметры:

    - include_currencies - валютные позиции;
    - include_money - денежные позиции;
    - include_positions - позиции DEPO;
    - include_max_buy_sell - лимиты покупки и продажи.
    """

    include_currencies: bool = Field(alias="includeCurrencies")
    include_money: bool = Field(alias="includeMoney")
    include_positions: bool = Field(alias="includePositions")
    include_max_buy_sell: bool = Field(alias="includeMaxBuySell")
