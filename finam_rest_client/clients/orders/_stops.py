import logging

from finam_rest_client.models.request_models import (
    CancelStopRequest,
    CreateStopRequest,
    GetStopsRequest,
)
from finam_rest_client.models.response_models import CancelStop, NewStop
from finam_rest_client.models.response_models import Stops as St

from .base import BaseOrders


class Stops(BaseOrders):
    """Класс для работы со стоп-ордерами."""

    path = "/public/api/v1/stops"
    _create_response_model = NewStop
    _cancel_response_model = CancelStop
    _get_response_model = St
    logger = logging.getLogger("finam_rest_client.Stops")

    async def get_stops(self, req_stops: GetStopsRequest) -> St:
        """
        Получение списка стоп-ордеров.

        :param req_stops: Модель запроса на получение списка стоп-ордеров.

        :return: Модель ответа на запрос списка стоп-ордеров.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_stops=}")
        result = await self._get(req_stops)
        self.logger.debug(f"Метод вернул: {result}")
        return result

    async def create_stop(self, req_stop: CreateStopRequest) -> NewStop:
        """
        Создание нового стоп-ордера.

        :param req_stop: Модель запроса на создание стоп-ордера.

        :return: Модель ответа на создание нового стоп-ордера.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_stop=}")
        result = await self._create(req_stop)
        self.logger.debug(f"Метод вернул: {result}")
        return result

    async def cancel_stop(self, req_stop: CancelStopRequest) -> CancelStop:
        """
        Отмена стоп-ордера.

        :param req_stop: Модель запроса на отмену стоп-ордера.

        :return: Модель ответа на отмену стоп-ордера.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_stop=}")
        result = await self._cancel(req_stop)
        self.logger.debug(f"Метод вернул: {result}")
        return result
