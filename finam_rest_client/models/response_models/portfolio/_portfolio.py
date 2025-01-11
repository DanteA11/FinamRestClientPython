from decimal import Decimal

from pydantic import BaseModel, Field

from ..base import BaseResponseModel
from .content import Content
from .currencies import Currency
from .money import Money
from .positions import Position


class PortfolioData(BaseModel):
    """
    Информация о портфеле.

    Параметры:

    - client_id - торговый код клиента;
    - content - наполнение портфеля;
    - equity - текущая оценка портфеля;
    - balance - входящая оценка стоимости портфеля;
    - positions - позиции портфеля. Список объектов типа Position.
      Запрашиваются выставлением флага include_positions равным true;
    - currencies - валюта портфеля. Список объектов типа CurrencyRow.
      Запрашивается выставлением флага include_currencies равным true;
    - money - денежные позиции. Список объектов типа Money.
      Запрашивается выставлением флага include_money равным true.
    """

    client_id: str = Field(alias="clientId", default="")
    content: Content
    equity: Decimal
    balance: Decimal
    positions: list[Position]
    currencies: list[Currency]
    money: list[Money]


class Portfolio(BaseResponseModel):
    """Результат запроса информации о портфеле."""

    data: PortfolioData | None = None
