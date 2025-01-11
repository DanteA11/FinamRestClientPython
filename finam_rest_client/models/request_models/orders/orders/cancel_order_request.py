"""Модель для отправки запроса на отмену заявки."""

from pydantic import Field

from ..base import BaseOrderRequest


class CancelOrderRequest(BaseOrderRequest):
    """
    Модель для отправки запроса на отмену заявки.

    Параметры:

    - client_id - торговый код клиента;
    - transaction_id - идентификатор отменяемой заявки.
    """

    transaction_id: int = Field(serialization_alias="TransactionId")
