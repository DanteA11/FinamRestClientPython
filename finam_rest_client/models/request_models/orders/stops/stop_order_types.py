"""Типы стоп-ордеров."""

from decimal import Decimal

from pydantic import Field

from finam_rest_client.models.common_types import StopPrice

from ..base import BaseStopOrderRequestModel


class StopLossRequest(BaseStopOrderRequestModel):
    """
    Модель для указания стоп-лосс в запросе.

    Параметры:

    - activation_price - цена активации;
    - price - цена условной заявки. В случае рыночной
      цены значение должно быть 0;
    - market_price - значение true указывает на то, что
      необходимо выставить рыночную заявку, иначе выставляется
      условная заявка с ценой price;
    - quantity - объем заявки. Тип StopQuantity;
    - time - защитное время (секунды);
    - use_credit - использование кредита (недоступно для срочного рынка).
      Указать значение true, если необходимо использовать кредит, иначе false.
    """

    price: Decimal = Decimal("0")


class TakeProfitRequest(BaseStopOrderRequestModel):
    """
    Модель для указания тейк-профит в запросе.

    Параметры:

    - activation_price - цена активации;
    - correction_price - коррекция. Тип StopPrice;
    - spread_price - защитный спред. В случае рыночной цены значение
      должно быть 0. Тип StopPrice;
    - market_price - значение true указывает на то, что необходимо выставить
      рыночную заявку, иначе выставляется условная заявка с ценой price;
    - quantity - объем заявки. Тип StopQuantity;
    - time - защитное время (секунды);
    - use_credit - использование кредита (недоступно для срочного рынка).
      Указать значение true, если использовать кредит, иначе false.
    """

    correction_price: StopPrice | None = Field(
        serialization_alias="correctionPrice", default=None
    )
    spread_price: StopPrice | None = Field(
        serialization_alias="spreadPrice", default=None
    )
