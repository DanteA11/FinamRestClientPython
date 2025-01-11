"""Базовые модели ответа на запросы получения ордеров."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from finam_rest_client.models.common_types import (
    BuySell,
    Market,
    OrderValidBefore,
    StopQuantity,
)


class BaseOrder(BaseModel):
    """Базовая модель ордера из ответа."""

    client_id: str = Field(alias="clientId")
    security_board: str = Field(alias="securityBoard")
    security_code: str = Field(alias="securityCode")
    buy_sell: BuySell = Field(alias="buySell")
    valid_before: OrderValidBefore | None = Field(
        alias="validBefore", default=None
    )
    market: Market
    message: str | None = None
    order_no: int = Field(alias="orderNo")
    accepted_at: datetime | None = Field(alias="acceptedAt", default=None)
    currency: str | None = None


class BaseStopOrderResponseModel(BaseModel):
    """Базовая модель стоп-ордера для результата."""

    activation_price: Decimal = Field(alias="activationPrice")
    time: int = 0
    market_price: bool = Field(alias="marketPrice", default=False)
    quantity: StopQuantity
    use_credit: bool = Field(alias="useCredit", default=False)
