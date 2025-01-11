from datetime import date, datetime

from pydantic import BaseModel

from ..base import BaseResponseModel
from .base import BaseCandle

__all__ = ("DayCandles", "IntraDayCandles")


class DayCandle(BaseCandle):
    date: date


class IntraDayCandle(BaseCandle):
    timestamp: datetime


class DayCandlesResponseData(BaseModel):
    candles: list[DayCandle]


class IntraDayCandlesResponseData(BaseModel):
    candles: list[IntraDayCandle]


class DayCandles(BaseResponseModel):
    """Свечи с интервалом от 1 дня."""

    data: DayCandlesResponseData | None = None


class IntraDayCandles(BaseResponseModel):
    """Свечи с внутридневным интервалом."""

    data: IntraDayCandlesResponseData | None = None
