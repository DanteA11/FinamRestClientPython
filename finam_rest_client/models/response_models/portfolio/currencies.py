"""Валюта портфеля."""

from decimal import Decimal

from pydantic import BaseModel, Field


class Currency(BaseModel):
    """
    Валюта портфеля.

    Параметры:

    - name - код валюты;
    - balance - текущая позиция;
    - cross_rate - курс валюты;
    - equity - оценка позиции;
    - unrealized_profit - нереализованная прибыль/убыток.
    """

    name: str = ""
    balance: Decimal
    cross_rate: Decimal = Field(alias="crossRate")
    equity: Decimal
    unrealized_profit: Decimal = Field(alias="unrealizedProfit")
