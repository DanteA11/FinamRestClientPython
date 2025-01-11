"""Модель для отправки запроса на отмену стоп-заявки."""

from pydantic import Field

from ..base import BaseOrderRequest


class CancelStopRequest(BaseOrderRequest):
    """
    Модель для отправки запроса на отмену стоп-заявки.

    Параметры:

    - client_id - торговый код клиента;
    - stop_id - идентификатор отменяемой стоп-заявки.
    """

    stop_id: int = Field(serialization_alias="StopId")
