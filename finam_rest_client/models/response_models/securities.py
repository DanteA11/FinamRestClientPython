"""Модель запроса инструментов."""

from decimal import Decimal

from pydantic import BaseModel, Field

from finam_rest_client.models.common_types import Market, PriceSign

from .base import BaseResponseModel

__all__ = ("Securities",)


class Security(BaseModel):
    """
    Модель биржевого инструмента.

    Объект инструмент описывается следующими полями:

    - code - код инструмента;
    - board - основной режим торгов инструмента;
    - market - рынок инструмента. Тип Market;
    - decimals - количество знаков в дробной части цены;
    - lotSize - размер лота;
    - minStep - минимальный шаг цены;
    - currency - код валюты номинала цены;
    - shortName - название инструмента;
    - properties - параметры инструмента;
    - timeZoneName - имя тайм-зоны;
    - bpCost - стоимость пункта цены одного инструмента
      (не лота), без учета НКД;
    - accruedInterest - текущий НКД;
    - priceSign - допустимая цена инструмента;
    - ticker - тикер инструмента на биржевой площадке листинга;
    - lotDivider - коэффициент дробления ценной бумаги в
      одном стандартном лоте.
    """

    code: str
    board: str
    market: Market
    decimals: int
    lot_size: int = Field(alias="lotSize")
    min_step: int = Field(alias="minStep")
    currency: str
    short_name: str = Field(alias="shortName")
    properties: int
    time_zone_name: str = Field(alias="timeZoneName")
    bp_cost: Decimal = Field(alias="bpCost")
    accrued_interest: Decimal = Field(alias="accruedInterest")
    price_sign: PriceSign = Field(alias="priceSign")
    ticker: str
    lot_divider: int = Field(alias="lotDivider")


class SecuritiesData(BaseModel):
    """Данные инструментов."""

    securities: list[Security]


class Securities(BaseResponseModel):
    """Результат ответа на запрос инструментов."""

    data: SecuritiesData | None = None
