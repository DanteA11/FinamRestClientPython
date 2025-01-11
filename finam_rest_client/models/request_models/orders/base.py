"""Базовые классы для запросов с ордерами."""

from decimal import Decimal

from pydantic import BaseModel, Field, field_serializer

from finam_rest_client.models.common_types import (
    BuySell,
    OrderValidBefore,
    StopQuantity,
)


class BaseOrderRequest(BaseModel):
    """Базовый класс запроса ордера."""

    client_id: str = Field(serialization_alias="ClientId")


class BaseGetOrdersRequest(BaseOrderRequest):
    """Базовый класс для запроса списка ордеров."""

    include_canceled: bool = Field(
        serialization_alias="IncludeCanceled", default=False
    )
    include_active: bool = Field(
        serialization_alias="IncludeActive", default=False
    )

    @field_serializer("include_canceled", when_used="json")
    def __serialize_include_canceled(self, include_canceled: bool) -> str:
        return self._serialize_func(include_canceled)

    @field_serializer("include_active", when_used="json")
    def __serialize_include_active(self, include_active: bool) -> str:
        return self._serialize_func(include_active)

    @staticmethod
    def _serialize_func(elem: bool) -> str:
        return str(elem).lower()


class BaseCreateOrder(BaseModel):
    """Базовая модель создания ордера."""

    client_id: str = Field(serialization_alias="clientId")
    security_board: str = Field(serialization_alias="securityBoard")
    security_code: str = Field(serialization_alias="securityCode")
    buy_sell: BuySell = Field(serialization_alias="buySell")
    valid_before: OrderValidBefore | None = Field(
        serialization_alias="validBefore", default=None
    )


class BaseStopOrderRequestModel(BaseModel):
    """Базовая модель стоп-ордера для отправки запроса."""

    activation_price: Decimal = Field(serialization_alias="activationPrice")
    time: int = 0
    market_price: bool = Field(
        serialization_alias="marketPrice", default=False
    )
    quantity: StopQuantity
    use_credit: bool = Field(serialization_alias="useCredit", default=True)
