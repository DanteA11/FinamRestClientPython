"""Модель запроса на получение портфеля."""

from pydantic import BaseModel, Field, field_serializer

__all__ = ("PortfolioRequest",)


class PortfolioRequest(BaseModel):
    """
    Модель запроса на получение портфеля.

    Параметры:

    - client_id - торговый код клиента (обязательный);
    - include_currencies - запросить информацию по валютам портфеля;
    - include_money - запросить информацию по денежным позициям портфеля;
    - include_positions - запросить информацию по позициям портфеля;
    - include_max_buy_sell - запросить информацию о максимальном
      доступном объеме на покупку/продажу.
    """

    client_id: str = Field(serialization_alias="clientId")
    include_currencies: bool = Field(
        serialization_alias="Content.IncludeCurrencies", default=False
    )
    include_money: bool = Field(
        serialization_alias="Content.IncludeMoney", default=False
    )
    include_positions: bool = Field(
        serialization_alias="Content.IncludePositions", default=False
    )
    include_max_buy_sell: bool = Field(
        serialization_alias="Content.IncludeMaxBuySell", default=False
    )

    @field_serializer("include_currencies", when_used="json")
    def __serialize_include_currencies(self, include_currencies: bool) -> str:
        return self.__serialize_func(include_currencies)

    @field_serializer("include_money", when_used="json")
    def __serialize_include_money(self, include_money: bool) -> str:
        return self.__serialize_func(include_money)

    @field_serializer("include_positions", when_used="json")
    def __serialize_include_positions(self, include_positions: bool) -> str:
        return self.__serialize_func(include_positions)

    @field_serializer("include_max_buy_sell", when_used="json")
    def __serialize_include_max_buy_sell(
        self, include_max_buy_sell: bool
    ) -> str:
        return self.__serialize_func(include_max_buy_sell)

    @staticmethod
    def __serialize_func(elem: bool) -> str:
        return str(elem).lower()
