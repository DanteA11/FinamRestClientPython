"""Свойства выставления заявок."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from finam_rest_client.models.common_types import OrderConditionType


class OrderCondition(BaseModel):
    """
    Свойства выставления заявок.

    Параметры:

    - type - тип условия,
      которое принимает следующие значения:
        - Bid - лучшая цена покупки;
        - BidOrLast- лучшая цена покупки или сделка по заданной цене и выше;
        - Ask - лучшая цена продажи;
        - AskOrLast - лучшая цена продажи или сделка по заданной цене и ниже;
        - Time - время выставления заявки на Биржу
          (параметр time должен быть установлен);
        - CovDown - обеспеченность ниже заданной;
        - CovUp - обеспеченность выше заданной;
        - LastUp - сделка на рынке по заданной цене или выше;
        - LastDown- сделка на рынке по заданной цене или ниже;
    - price - значение цены для условия;
    - time - Время, когда заявка будет отменена на сервере. В UTC.
    """

    type: OrderConditionType
    price: Decimal
    time: datetime | None = None
