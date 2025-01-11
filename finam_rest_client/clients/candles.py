"""Логика работы со свечами."""

import logging

from finam_rest_client.models.request_models import (
    DayCandlesRequest,
    IntraDayCandlesRequest,
)
from finam_rest_client.models.response_models import (
    DayCandles,
    IntraDayCandles,
)

from .base import BaseObjClient


class Candles(BaseObjClient):
    """Класс для работы со свечами."""

    path = "/public/api/v1"
    method = "get"
    DAY, INTRADAY = (f"{path}/day-candles", f"{path}/intraday-candles")
    logger = logging.getLogger("finam_rest_client.Candles")

    async def get_day_candles(
        self, req_candles: DayCandlesRequest
    ) -> DayCandles:
        """
        Получение дневных свечей.

        :param req_candles: Модель запроса на получение дневных свечей.

        :return: Модель дневных свечей.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_candles=}")
        data = await self.create_data(req_candles)
        result = await self._execute_request(
            resp_model=DayCandles,
            params=data,
            path=self.DAY,
        )
        self.logger.debug(f"Метод вернул: {result}")
        return result

    async def get_intraday_candles(
        self, req_candles: IntraDayCandlesRequest
    ) -> IntraDayCandles:
        """
        Получение внутридневных свечей.

        :param req_candles: Модель запроса на получение дневных свечей.

        :return: Модель дневных свечей.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_candles=}")
        data = await self.create_data(req_candles)
        result = await self._execute_request(
            resp_model=IntraDayCandles,
            params=data,
            path=self.INTRADAY,
        )
        self.logger.debug(f"Метод вернул: {result}")
        return result
