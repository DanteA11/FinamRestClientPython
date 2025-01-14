"""Модуль содержит базовые классы клиента и объекта."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Self, TypeVar

from aiohttp import ClientSession
from pydantic import BaseModel

from finam_rest_client.exceptions import BaseApiException
from finam_rest_client.models.response_models.base import BaseResponseModel

B = TypeVar("B", bound=BaseResponseModel)


class BaseapiClientInterface(ABC):
    """Интерфейс для клиента."""

    @abstractmethod
    async def check_token(self, *args, **kwargs):
        """Проверка токена на валидность."""

    @abstractmethod
    async def get_candles(self, *args, **kwargs):
        """Получение свечей."""

    @abstractmethod
    async def get_securities(self, *args, **kwargs):
        """Получение списка инструментов."""

    @abstractmethod
    async def get_portfolio(self, *args, **kwargs):
        """Получение информации о портфеле."""

    @abstractmethod
    async def get_orders(self, *args, **kwargs):
        """Получение списка заявок."""

    @abstractmethod
    async def create_order(self, *args, **kwargs):
        """Создание нового ордера."""

    @abstractmethod
    async def cancel_order(self, *args, **kwargs):
        """Отмена ордера."""

    @abstractmethod
    async def get_stops(self, *args, **kwargs):
        """Получение списка стоп-заявок."""

    @abstractmethod
    async def create_stop(self, *args, **kwargs):
        """Создание нового стоп-ордера."""

    @abstractmethod
    async def cancel_stop(self, *args, **kwargs):
        """Отмена стоп-ордера."""


class BaseApiClient(BaseapiClientInterface, ABC):
    """
    Базовый класс для реализации подключения к Api.

    :param url: Базовый url Api.
    :param headers: Заголовки для отправки на сервер.
    """

    __slots__ = "__url", "__headers", "__session"
    logger: logging.Logger

    def __init__(self, url: str, headers: dict):
        self.__url = url
        self.__headers = headers
        self.__session = None

    @property
    def url(self) -> str:
        """Базовый url."""
        return self.__url

    @property
    def headers(self) -> dict[str, Any]:
        """Заголовки."""
        return self.__headers

    @property
    def session(self) -> ClientSession:
        """Экземпляр сессии."""
        if not self.__session:
            raise BaseApiException(
                "Отсутствует клиентская сессия. "
                "Воспользуйтесь методом session_start "
                "или контекстным менеджером."
            )
        return self.__session

    async def __aenter__(self) -> Self:
        """Вход в менеджер контекста."""
        await self.session_start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из менеджера контекста."""
        await self.session_end()

    async def session_start(self):
        """
        Метод создает новый экземпляр сессии.

        Предыдущая сессия закрывается.
        """
        self.logger.info("Запущено создание сессии.")
        if self.__session:
            self.logger.info("Закрытие предыдущей сессии.")
            await self.__session.close()
        self.__session = ClientSession(
            base_url=self.__url, headers=self.__headers
        )
        self.logger.info("Сессия создана.")

    async def session_end(self):
        """Метод закрывает текущую сессию, если существует."""
        self.logger.info("Запущено закрытие сессии.")
        if not self.__session:
            self.logger.info("Сессия не существует. Выход.")
            return
        await self.__session.close()
        self.logger.info("Сессия закрыта.")

    async def execute_request(
        self,
        method: str,
        path: str,
        *,
        another_session: ClientSession | None = None,
        **kwargs,
    ) -> tuple[str, bool]:
        """
        Метод для отправки запросов к Api.

        В случае возникновения ошибки при выполнении
        запроса закрывает клиентскую сессию.

        :param method: Тип запроса.
        :param path: Uri запроса.
        :param another_session: Сессия для использования в запросе.
            Если не указано, то будет использоваться сессия
            внутри клиента. В большинстве случаев не передается.
        :param kwargs: Дополнительные аргументы для передачи в запрос.

        :raise BaseApiException: В случае появления ошибок.

        :return: Текст ответа в json и True(если вернулся код 200) | False.
        """
        self.logger.debug(
            "Метод вызван с параметрами: method=%s, "
            "path=%s, another_session=%s, %s.",
            method,
            path,
            another_session,
            kwargs,
        )
        session: ClientSession = another_session or self.session
        try:
            response, ok = await self._execute_request(
                method, session, path, **kwargs
            )
        except Exception as exc:
            self.logger.warning("Возникла ошибка: %s", exc)
            await self.session_end()
            raise BaseApiException(exc)
        self.logger.debug(
            "Метод вернул ответ: response=%s, ok=%s", response, ok
        )
        return response, ok

    @staticmethod
    async def _execute_request(
        method: str,
        session: ClientSession,
        path: str,
        **kwargs,
    ) -> tuple[str, bool]:
        async with session.request(method, path, **kwargs) as response:
            if response.status != 200:
                if response.content_type != "application/json":
                    response.raise_for_status()
                return await response.text(), False
            return await response.text(), True


ApiClient = TypeVar("ApiClient", bound=BaseApiClient)


class BaseObjClient(ABC):
    """
    Базовый класс для реализации объектов взаимодействия с Api.

    :param client: Экземпляр класса клиента.
    """

    __slots__ = "__client"
    logger: logging.Logger

    def __init__(self, client: ApiClient):
        self.__client = client

    @property
    def client(self):
        """Ссылка на экземпляр клиента."""
        return self.__client

    @property
    @abstractmethod
    def path(self) -> str:
        """Возвращает URL для передачи запроса."""

    @property
    @abstractmethod
    def method(self) -> str:
        """Возвращает метод запроса."""

    @classmethod
    def create_data(cls, data: BaseModel) -> dict[str, Any]:
        """
        Метод по подготовке данных.

        Переводит модели Pydantic в словарь.
        """
        cls.logger.debug("Запущена подготовка данных: data=%s.", data)
        result = data.model_dump(mode="json", by_alias=True, exclude_none=True)
        cls.logger.debug("Подготовка завершена: %s.", result)
        return result

    async def _execute_request(
        self,
        resp_model: type[B],
        *,
        path: str | None = None,
        **kwargs,
    ) -> B:
        """
        Метод отправляет запрос к Api.

        :param resp_model: Модель для ответа сервера.
        :param path: Пользовательский путь.

        :return: Ответ сервера.
        """
        self.logger.debug(
            "Метод запущен с параметрами: resp_model=%s, "
            "path=%s, kwargs=%s.",
            resp_model,
            path,
            kwargs,
        )
        path = path or self.path
        response, ok = await self.client.execute_request(
            self.method, path, **kwargs
        )
        result = resp_model.model_validate_json(response)
        if not ok:
            self.logger.warning(
                "Запрос %s вернулся с ошибкой: %s.",
                resp_model.__name__,
                result.error,
            )
        self.logger.debug("Метод вернул: %s.", result)
        return result
