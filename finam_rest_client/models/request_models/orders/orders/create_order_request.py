"""Модель для отправки запроса на выставление новой заявки."""

from decimal import Decimal

from pydantic import Field

from finam_rest_client.models.common_types import Property

from ..base import BaseCreateOrder
from .order_condition import OrderCondition


class CreateOrderRequest(BaseCreateOrder):
    """
    Модель для отправки запроса на выставление новой заявки.

    Параметры:

    - client_id - торговый код клиента;
    - security_board - основной режим торгов для инструмента;
    - security_code - код инструмента;
    - buy_sell - тип BuySell;
    - quantity - объем заявки в лотах;
    - use_credit - использование кредита (недоступно для срочного рынка).
      Указать значение true, если необходимо использовать
      кредит, иначе false;
    - price - цена исполнения заявки. Для рыночной заявки указать
      значение null (или не передавать это поле). Для условной заявки
      необходимо указать цену исполнения;
    - property - свойства исполнения частично исполненных заявок;
    - condition - свойства выставления заявок. Тип OrderCondition;
    - valid_before - условие по времени действия заявки. Тип OrderValidBefore.
    """

    quantity: int
    use_credit: bool = Field(serialization_alias="useCredit", default=True)
    price: Decimal | None = None
    property: Property = Property.put_in_queue
    condition: OrderCondition | None = None
