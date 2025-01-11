"""Модели для ответа на запросы лимитных и условных заявок."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from finam_rest_client.models.common_types import OrderStatus

from ..base import BaseResponseModel
from .base import BaseOrder

__all__ = ("NewOrder", "CancelOrder", "Orders")


class Order(BaseOrder):
    """
    Модель заявки.

    Параметры:

    - order_no - уникальный идентификатор заявки на бирже.
      Задается после того, как заявка будет принята биржей
      (см. поле status);
    - transaction_id - внутренний идентификатор заявки в
      системе TRANSAQ (для чужой заявки значение всегда равно 0);
    - security_code - код инструмента;
    - client_id - торговый код клиента;
    - status - текущий статус заявки. Тип OrderStatus;
    - buy_sell - тип BuySell;
    - created_at - время регистрации заявки на бирже (UTC);
    - price - цена исполнения условной заявки. Для рыночной
      заявки значение всегда равно 0;
    - quantity - объем заявки в лотах;
    - balance - неисполненный остаток, в лотах. Изначально равен quantity,
      но по мере исполнения заявки (совершения сделок) будет уменьшаться
      на объем сделки. Значение 0 будет соответствовать полностью
      исполненной заявке (см. поле status);
    - message - содержит сообщение об ошибке, возникшей при обработке заявки.
      Заявка может быть отклонена по разным причинам сервером TRANSAQ
      или биржей с выставлением поля status;
    - currency - код валюты цены;
    - condition - свойства выставления заявок. Тип OrderCondition;
    - valid_before - условие по времени действия заявки. Тип OrderValidBefore;
    - accepted_at - время регистрации заявки на сервере TRANSAQ (UTC);
    - security_board - основной режим торгов инструмента;
    - market - рынок инструмента. Тип Market.
    """

    status: OrderStatus
    transaction_id: int = Field(alias="transactionId")
    created_at: datetime | None = Field(alias="createdAt", default=None)
    price: Decimal | None = None
    quantity: int
    balance: int


class OrdersData(BaseModel):
    """Данные ордеров."""

    client_id: str | None = Field(alias="clientId", default=None)
    orders: list[Order]


class Orders(BaseResponseModel):
    """Модель ответа на запрос списка ордеров."""

    data: OrdersData | None = None


class CancelOrderData(BaseModel):
    """Данные ответа на отмену ордера."""

    client_id: str | None = Field(alias="clientId", default=None)
    transaction_id: int = Field(alias="transactionId")


class CancelOrder(BaseResponseModel):
    """Ответ на отмену ордера."""

    data: CancelOrderData | None = None


class NewOrderData(CancelOrderData):
    """Данные ответа на создание ордера."""

    security_code: str | None = Field(alias="securityCode", default=None)


class NewOrder(BaseResponseModel):
    """Ответ на создание ордера."""

    data: NewOrderData | None = None
