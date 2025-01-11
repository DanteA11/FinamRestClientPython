from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from finam_rest_client.models.common_types import StopStatus

from ...base import BaseResponseModel
from ..base import BaseOrder
from .stop_order_types import StopLoss, TakeProfit


class Stop(BaseOrder):
    """
    Стоп-заявка.

    Параметры:

    - stop_id - идентификатор стоп-заявки;
    - security_code - код инструмента;
    - security_board - основной режим торгов инструмента;
    - market - рынок инструмента. Тип Market;
    - client_id - торговый код клиента;
    - buy_sell - тип BuySell;
    - expiration_date - дата экспирации заявки FORTS;
    - link_order - биржевой номер связанной (активной) заявки;
    - valid_before - условие по времени действия заявки. Тип OrderValidBefore.
    - status - текущий статус стоп-заявки. Тип StopStatus;
    - message - содержит сообщение об ошибке, возникшей при обработке заявки.
      Заявка может быть отклонена по разным причинам сервером TRANSAQ или
      биржей с выставлением поля status;
    - order_no - номер заявки, полученной в результате исполнения стоп-заявки;
    - trade_no - номер сделки, которая привела к исполнению стоп-заявки;
    - accepted_at - время регистрации заявки на сервере TRANSAQ (UTC);
    - canceled_at - время отмены заявки на сервере TRANSAQ (UTC);
    - currency - валюта цены;
    - take_profit_extremum - текущий локальный экстремум для TP;
    - take_profit_level - текущий уровень коррекции для TP;
    - stop_loss - информация об stop-loss. Тип StopLoss;
    - take_profit - информация об take-profit. Тип TakeProfit.
    """

    status: StopStatus
    stop_id: int = Field(alias="stopId")
    trade_no: int = Field(alias="tradeNo")
    canceled_at: datetime | None = Field(alias="canceledAt", default=None)
    take_profit_extremum: Decimal = Field(alias="takeProfitExtremum")
    take_profit_level: Decimal = Field(alias="takeProfitLevel")
    link_order: int = Field(alias="linkOrder")
    expiration_date: datetime | None = Field(
        alias="expirationDate", default=None
    )
    stop_loss: StopLoss | None = Field(alias="stopLoss", default=None)
    take_profit: TakeProfit | None = Field(alias="takeProfit", default=None)


class StopsData(BaseModel):
    """Данные стоп-заявок."""

    client_id: str | None = Field(alias="clientId", default=None)
    stops: list[Stop]


class Stops(BaseResponseModel):
    """Модель ответа на запрос списка стоп-заявок."""

    data: StopsData | None = None


class CancelStopData(BaseModel):
    """Модель данных при отмене стоп-заявки."""

    client_id: str | None = Field(alias="clientId", default=None)
    stop_id: int = Field(alias="stopId")


class CancelStop(BaseResponseModel):
    """Ответ на отмену стоп-заявки."""

    data: CancelStopData | None = None


class NewStopData(CancelStopData):
    """Модель данных при выставлении новой стоп-заявки."""

    security_code: str | None = Field(alias="securityCode", default=None)
    security_board: str | None = Field(alias="securityBoard", default=None)


class NewStop(BaseResponseModel):
    """Ответ на выставление новой стоп-заявки."""

    data: NewStopData | None = None
