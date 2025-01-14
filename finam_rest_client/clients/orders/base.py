"""Базовые классы для работы с ордерами."""

import logging
from abc import ABC, abstractmethod
from typing import Literal

from finam_rest_client.clients.base import ApiClient, BaseObjClient


class BaseOrders(ABC):
    """
    Абстрактный класс для работы с ордерами.

    :param client: Экземпляр класса клиента.
    """

    logger: logging.Logger

    def __init__(self, client: ApiClient):
        self.__get_orders = GetOrders(client, self, self._get_response_model)
        self.__create_order = CreateOrder(
            client, self, self._create_response_model
        )
        self.__cancel_order = CancelOrder(
            client, self, self._cancel_response_model
        )

    @property
    @abstractmethod
    def path(self) -> str:
        """Возвращает URL для передачи запроса."""

    @property
    @abstractmethod
    def _get_response_model(self):
        """Модель для ответа на запрос ордеров."""

    @property
    @abstractmethod
    def _create_response_model(self):
        """Модель для ответа на создание нового ордера."""

    @property
    @abstractmethod
    def _cancel_response_model(self):
        """Модель для ответа отмену ордера."""

    async def _get(self, req):
        """
        Получение списка ордеров.

        :param req: Модель запроса на получение списка ордеров.

        :return: Модель ответа на запрос списка ордеров.
        """
        return await self.__get_orders.request_run(req)

    async def _create(self, req):
        """
        Создание нового ордера.

        :param req: Модель запроса на создание ордера.

        :return: Модель ответа на создание нового ордера.
        """
        return await self.__create_order.request_run(req)

    async def _cancel(self, req):
        """
        Отмена ордера.

        :param req: Модель запроса на отмену ордера.

        :return: Модель ответа на отмену ордера.
        """
        return await self.__cancel_order.request_run(req)


class BaseSubOrders(BaseObjClient, ABC):
    """Абстрактный класс для реализации классов ордеров."""

    def __new__(  # noqa
        cls, client, orders, *args, **kwargs
    ) -> "BaseSubOrders":
        cls.logger = orders.logger
        return super().__new__(cls)

    def __init__(
        self,
        client,
        orders,
        resp_model,
    ):
        super().__init__(client=client)
        self.__orders = orders
        self.__resp_model = resp_model

    @property
    def orders(self):
        """Экземпляр внешнего класса."""
        return self.__orders

    @property
    def path(self) -> str:
        """Путь для отправки запросов."""
        return self.orders.path  # type: ignore

    @property
    def _response_model(self):
        """Модель ответа."""
        return self.__resp_model

    async def _request_run(
        self,
        req,
        arg_type_name: Literal["json", "params"] = "params",
    ):
        """
        Отправка запроса.

        :param req: Модель запроса.
        :param arg_type_name: Имя типа аргумента для передачи.

        :return: Модель ответа на запрос.
        """
        data = self.create_data(req)
        my_kwargs = {arg_type_name: data}
        result = await self._execute_request(  # type: ignore
            resp_model=self._response_model,  # type: ignore
            path=self.path,
            **my_kwargs,
        )
        return result  # type: ignore

    async def request_run(self, req):
        """
        Отправка запроса.

        :param req: Модель запроса.

        :return: Модель ответа на запрос.
        """
        return await self._request_run(req=req)


class GetOrders(BaseSubOrders):
    """Класс для получения списка ордеров."""

    method = "get"


class CancelOrder(BaseSubOrders):
    """Класс для отмены ордера."""

    method = "delete"


class CreateOrder(BaseSubOrders):
    """Класс для создания нового ордера."""

    method = "post"

    async def request_run(self, req):
        """
        Отправка запроса.

        :param req: Модель запроса.

        :return: Модель ответа на запрос.
        """
        return await self._request_run(req=req, arg_type_name="json")
