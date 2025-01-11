"""Позиция по инструменту."""

from decimal import Decimal

from pydantic import BaseModel, Field

from finam_rest_client.models.common_types import Market


class Position(BaseModel):
    """
    Позиция по инструменту.

    Описывается следующими полями:

    - security_сode - код инструмента;
    - market - рынок инструмента. Тип Market;
    - balance - текущая позиция, шт.;
    - current_price - текущая цена в валюте цены инструмента.;
    - equity - оценка позиции по инструменту в валюте риска;
    - average_price - балансовая цена в валюте цены инструмента;
    - currency - код валюты риска;
    - accumulated_profit - прибыль/убыток по входящей позиции, в валюте риска;
    - today_profit - прибыль/убыток по сделкам за день, в валюте риска;
    - unrealized_profit - нереализованные прибыль/убытки по
      балансовой цене в валюте инструмента;
    - profit - прибыль/убытки в валюте цены инструмента;
    - max_buy/max_sell - максимально возможное количество лотов
      на покупку/продажу (вычисляется, если указать флаг
      includeMaxBuySell в true, иначе значение будет равно 0);
    - price_currency - код валюты цены;
    - average_price_currency - код валюты балансовой цены;
    - average_rate - кросс-курс валюты балансовой цены к валюте риска.
    """

    security_code: str = Field(alias="securityCode", default="")
    market: Market
    balance: int
    current_price: Decimal = Field(alias="currentPrice")
    equity: Decimal
    average_price: Decimal = Field(alias="averagePrice")
    currency: str = ""
    accumulated_profit: Decimal = Field(alias="accumulatedProfit")
    today_profit: Decimal = Field(alias="todayProfit")
    unrealized_profit: Decimal = Field(alias="unrealizedProfit")
    profit: Decimal
    max_buy: int = Field(alias="maxBuy")
    max_sell: int = Field(alias="maxSell")
    price_currency: str = Field(alias="priceCurrency", default="")
    average_price_currency: str = Field(
        alias="averagePriceCurrency", default=""
    )
    average_rate: Decimal = Field(alias="averageRate")
