"""Общие типы."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class BuySell(str, Enum):
    """
    Определяет тип операции: покупка или продажа.

    Принимает следующие значения:

    - Buy - покупка;
    - Sell - продажа.
    """

    buy = "Buy"
    sell = "Sell"


class FinamDecimal(BaseModel):
    """
    Представляет десятичное число с плавающей запятой.

    Параметры:

    - num - Мантисса.
    - scale - Экспонента по основанию 10.

    Итоговое значение вычисляется по формуле:
    num * 10^(-scale). Где ^ оператор возведение в степень.

    Например: для num = 250655 и scale = 3,
    итоговое значение будет 250.655.
    """

    num: int
    scale: int


class Market(str, Enum):
    """
    Определяет рынок, на котором торгуется инструмент.

    Принимает следующие значения:

    - Stock - фондовый рынок Московской биржи;
    - Forts - срочный рынок Московской биржи;
    - Spbex - Санкт-Петербургская биржа;
    - Mma - фондовый рынок США;
    - Ets - валютный рынок Московской биржи;
    - Bonds - рынок облигаций Московской биржи;
    - Options - рынок опционов Московской биржи.
    """

    stock = "Stock"
    forts = "Forts"
    spbex = "Spbex"
    mma = "Mma"
    ets = "Ets"
    bonds = "Bonds"
    options = "Options"


class OrderValidBeforeType(str, Enum):
    """
    Обозначает время действия заявки.

    Тип условия определяет значение поля type,
    которое принимает следующие параметры:

    - TillEndSession - заявка действует до конца сессии;
    - TillCancelled - заявка действует, пока не будет отменена;
    - ExactTime - заявка действует до указанного времени.
      Параметр time должен быть задан.
    """

    till_end_session = "TillEndSession"
    till_cancelled = "TillCancelled"
    exact_time = "ExactTime"


class OrderValidBefore(BaseModel):
    """
    Условие по времени действия заявки.

    Параметры:

    - type - установка временных рамок действия заявки.
      Принимает значения:
        - TillEndSession - заявка действует до конца сессии;
        - TillCancelled - заявка действует, пока не будет отменена;
        - ExactTime - заявка действует до указанного времени.
          (Параметр time должен быть задан.)
    - time - Время, когда заявка будет отменена на сервере. В UTC.
    """

    type: OrderValidBeforeType
    time: datetime | None = None


class PriceSign(str, Enum):
    """
    Допустимая цена инструмента.

    Принимает следующие значения:

    - Unspecified — это поле используется, когда информация
      о цене не задана (новейшие IPO, которые еще не
      начали торговаться, последствия после "падения" сервера).
    - Positive — указывает на то, что цена акции положительна.
      Ticker с таким значением подразумевает, что стоимость
      акции выше нуля и органично подходит для биржевой
      торговли (акции, облигации, фонды).
    - NonNegative — обозначает, что цена может быть нулевой
      или положительной. Такое значение подразумевает отсутствие
      активной торговли по определённой цене или временное
      приостановление (криптовалюты, облигации с нулевым купоном).
    - Any — позволяет произвольное значение цены, как положительное,
      так и отрицательное (фьючерсы, опционы).
    """

    unspecified = "Unspecified"
    positive = "Positive"
    non_negative = "NonNegative"
    any = "Any"


class Property(str, Enum):
    """
    Свойства исполнения частично исполненных заявок.

    Принимает следующие значения:

    - PutInQueue - неисполненная часть заявки помещается в
      очередь заявок биржи;
    - CancelBalance - неисполненная часть заявки снимается с торгов;
    - ImmOrCancel - сделки совершаются только в том случае, если заявка
      может быть удовлетворена полностью и сразу при выставлении.
    """

    put_in_queue = "PutInQueue"
    cancel_balance = "CancelBalance"
    imm_or_cancel = "ImmOrCancel"


class OrderConditionType(str, Enum):
    """
    Типы условных ордеров.

    Параметры:

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
    """

    bid = "Bid"
    bid_or_last = "BidOrLast"
    ask = "Ask"
    ask_or_last = "AskOrLast"
    time = "Time"
    cov_down = "CovDown"
    cov_up = "CovUp"
    last_up = "LastUp"
    last_down = "LastDown"


class OrderStatus(str, Enum):
    """
    Статус заявки.

    Принимает следующие значения:

    - None - заявка принята сервером TRANSAQ, и заявке присвоен transactionId;
    - Active - заявка принята биржей, и заявке присвоен orderNo;
    - Matched - заявка полностью исполнилась (выполнилась);
    - Cancelled - заявка была отменена (снята) пользователем или биржей.
    """

    none = "None"
    active = "Active"
    cancelled = "Cancelled"
    matched = "Matched"


class StopStatus(str, Enum):
    """
    Статус стоп-заявки.

    Принимает следующие значения:

    - Active - заявка принята сервером TRANSAQ;
    - Executed - заявка исполнилась (выполнилась);
    - Cancelled - заявка была отменена (снята) пользователем или биржей.
    """

    active = "Active"
    executed = "Executed"
    cancelled = "Cancelled"


class QuantityUnits(str, Enum):
    """Единицы объема стоп-заявки."""

    percent = "Percent"
    lots = "Lots"


class StopQuantity(BaseModel):
    """
    Объем стоп заявки.

    Параметры:

    - value - значение;
    - units - единицы объема стоп-заявки:

        - Percent - проценты;
        - Lots - лоты.
    """

    value: Decimal
    units: QuantityUnits = QuantityUnits.lots


class StopPriceUnits(str, Enum):
    """Единицы цены стоп-заявки."""

    percent = "Percent"
    pips = "Pips"


class StopPrice(StopQuantity):
    """
    Цена стоп-заявки.

    Параметры:

    - value - значение цены;
    - units - единицы цены стоп-заявки:

        - Percent - проценты;
        - Pips - пипсы.
    """

    units: StopPriceUnits = StopPriceUnits.pips  # type: ignore
