"""Информация о биржевых инструментах."""

import logging

from finam_rest_client.clients.base import BaseApiClient, BaseObjClient
from finam_rest_client.models.request_models import SecuritiesRequest
from finam_rest_client.models.response_models import Securities as Sec

from .database import AbstractDBManager, DBManager


class Securities(BaseObjClient):
    """
    Класс для получения данных об инструменте.

    :param client: Клиент.
    :param drop_all: Опциональный параметр.
        Указывает нужно ли удалять таблицы.
    :param db_url: Url базы данных для SQLAlchemy.
     Если не установлен, будет использоваться sqlite+aiosqlite.
     Важно добавить асинхронный движок при подключении.
     Например, postgresql+psycopg_async.
    """

    path = "/public/api/v1/securities"
    method = "get"
    logger = logging.getLogger("finam_rest_api_client.Securities")
    _data_default_params = {"seccode": None, "board": None}

    def __init__(
        self, client: BaseApiClient, drop_all: bool, db_url: str = ""
    ):
        super().__init__(client)
        self.__db = DBManager(drop_all=drop_all, db_url=db_url)

    @property
    def db(self) -> AbstractDBManager:
        """Менеджер для запросов в БД."""
        return self.__db

    async def get_securities(
        self,
        req_securities: SecuritiesRequest | None = None,
        from_api: bool = False,
    ) -> Sec:
        """
        Получение списка инструментов.

        :param req_securities: Модель запроса на получение дневных свечей.
        :param from_api: Запросить данные из api. Если False,
          то данные сперва запрашиваются в БД.

        :return: Модель инструментов.
        """
        self.logger.debug(f"Метод запущен с параметрами: {req_securities=}.")
        data = None
        if req_securities:
            data = await self.create_data(req_securities)
        if not from_api:
            res = await self._get_securities_from_db(
                **data or self._data_default_params
            )
            if res:
                self.logger.info("Данные найдены в БД.")
                return res
        result = await self._execute_request(
            resp_model=Sec,
            params=data,
            path=self.path,
        )
        if result.error is None and result.data.securities:  # type: ignore
            await self._add_securities_to_db(result)
        self.logger.info("Данные получены из ответа Api.")
        return result

    async def _get_securities_from_db(
        self, seccode: str | None = None, board: str | None = None
    ) -> Sec | None:
        """
        Получение информации об инструментах из БД.

        :param seccode: Режим торгов (необязательное поле для фильтрации)
        :param board: Тикер инструмента (необязательное поле для фильтрации)

        :return: Модель информации об инструментах.
        """
        self.logger.debug("Поиск данных в БД.")
        return await self.db.get_securities(seccode=seccode, board=board)

    async def _add_securities_to_db(self, securities: Sec) -> bool:
        """
        Добавление информации об инструменте/ах в БД.

        :param securities: Модель информации об инструментах.

        :return: True, если запрос успешен, иначе False.
        """
        self.logger.debug("Добавление данных в БД.")
        return await self.db.add_securities(securities=securities)
