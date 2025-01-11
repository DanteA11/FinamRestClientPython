"""Модель для запроса получения списка заявок."""

from pydantic import Field, field_serializer

from ..base import BaseGetOrdersRequest


class GetOrdersRequest(BaseGetOrdersRequest):
    """
    Модель для запроса получения списка заявок.

    Параметры:

    - client_id - торговый код клиента (обязательный);
    - include_matched - вернуть исполненные заявки;
    - include_canceled - вернуть отмененные заявки;
    - include_active - вернуть активные заявки.
    """

    include_matched: bool = Field(
        serialization_alias="IncludeMatched", default=False
    )

    @field_serializer("include_matched", when_used="json")
    def __serialize_include_matched(self, include_matched: bool) -> str:
        return self._serialize_func(include_matched)
