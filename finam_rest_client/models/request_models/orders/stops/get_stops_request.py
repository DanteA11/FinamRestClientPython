"""Модель для запроса получения списка стоп-заявок."""

from pydantic import Field, field_serializer

from ..base import BaseGetOrdersRequest


class GetStopsRequest(BaseGetOrdersRequest):
    """
    Модель для запроса получения списка стоп-заявок.

    Параметры:

    - client_id - торговый код клиента (обязательный);
    - include_executed - вернуть исполненные стоп-заявки;
    - include_canceled - вернуть отмененные стоп-заявки;
    - include_active - вернуть активные стоп-заявки.
    """

    include_executed: bool = Field(
        serialization_alias="IncludeExecuted", default=False
    )

    @field_serializer("include_executed", when_used="json")
    def __serialize_include_executed(self, include_executed: bool) -> str:
        return self._serialize_func(include_executed)
