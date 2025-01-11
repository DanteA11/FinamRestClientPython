"""Модель для выставления новой стоп-заявки."""

from datetime import datetime

from pydantic import Field

from ..base import BaseCreateOrder
from .stop_order_types import StopLossRequest, TakeProfitRequest


class CreateStopRequest(BaseCreateOrder):
    """
    Модель для выставления новой стоп-заявки.

    Параметры:

    - client_id - торговый код клиента;
    - security_board - основной режим торгов инструмента;
    - security_code - код инструмента;
    - buy_sell - тип BuySell;
    - stop_loss - информация о stop-loss. Тип StopLossRequest;
    - take_profit - информация о take-profit. Тип TakeProfitRequest;
    - expiration_date - дата экспирации заявки FORTS;
    - link_order - биржевой номер связанной (активной) заявки;
    - valid_before - условие по времени действия заявки. Тип OrderValidBefore;
    """

    stop_loss: StopLossRequest | None = Field(
        serialization_alias="stopLoss", default=None
    )
    take_profit: TakeProfitRequest | None = Field(
        serialization_alias="takeProfit", default=None
    )
    expiration_date: datetime | None = Field(
        serialization_alias="expirationDate", default=None
    )
    link_order: int = Field(serialization_alias="linkOrder")
