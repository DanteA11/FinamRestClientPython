import logging

from finam_rest_client.models.request_models import (
    CancelOrderRequest,
    CreateOrderRequest,
    GetOrdersRequest,
)
from finam_rest_client.models.response_models import CancelOrder, NewOrder
from finam_rest_client.models.response_models import Orders as Ord

from .base import BaseOrders


class Orders(BaseOrders):
    """Класс работы с ордерами."""

    path = "/public/api/v1/orders"
    _create_response_model = NewOrder
    _cancel_response_model = CancelOrder
    _get_response_model = Ord
    logger = logging.getLogger("finam_rest_client.Orders")

    async def get_orders(self, req_orders: GetOrdersRequest) -> Ord:
        """
        Получение списка ордеров.

        :param req_orders: Модель запроса на получение списка ордеров.

        :return: Модель ответа на запрос списка ордеров.
        """
        self.logger.debug(
            "Метод запущен с параметрами: req_orders=%s", req_orders
        )
        result = await self._get(req_orders)
        self.logger.debug("Метод вернул: %s", result)
        return result

    async def create_order(self, req_order: CreateOrderRequest) -> NewOrder:
        """
        Создание нового ордера.

        :param req_order: Модель запроса на создание ордера.

        :return: Модель ответа на создание нового ордера.
        """
        self.logger.debug(
            "Метод запущен с параметрами: req_order=%s", req_order
        )
        result = await self._create(req_order)
        self.logger.debug("Метод вернул: %s", result)
        return result

    async def cancel_order(self, req_order: CancelOrderRequest) -> CancelOrder:
        """
        Отмена ордера.

        :param req_order: Модель запроса на отмену ордера.

        :return: Модель ответа на отмену ордера.
        """
        self.logger.debug(
            "Метод запущен с параметрами: req_order=%s", req_order
        )
        result = await self._cancel(req_order)
        self.logger.debug("Метод вернул: %s", result)
        return result
