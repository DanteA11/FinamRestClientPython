"""Базовые классы для менеджера базы данных."""

from abc import ABC, abstractmethod
from logging import Logger

from ._database import (
    get_async_engine,
    get_async_session_maker,
    start_conn,
    stop_conn,
)


class DBManagerInterface(ABC):
    """Интерфейс для взаимодействия с базой данных."""

    @abstractmethod
    async def add_securities(self, *args, **kwargs):
        """Добавление информации об инструменте/ах в БД."""

    @abstractmethod
    async def get_securities(self, *args, **kwargs):
        """Получение информации об инструментах из БД."""

    @abstractmethod
    async def remove_securities(self, *args, **kwargs):
        """Удаление информации об инструментах из БД."""

    @abstractmethod
    async def start(self) -> None:
        """Функция выполняет действия, необходимые при подключении к БД."""

    @abstractmethod
    async def stop(self) -> None:
        """Функция выполняет действия, необходимые при отключении от БД."""


class AbstractDBManager(DBManagerInterface, ABC):
    """
    Абстрактный класс для взаимодействия с базой данных.

    :param db_url: Url базы данных.
    :param drop_all: Опциональный параметр.
        Указывает нужно ли удалять таблицы.
    """

    __slots__ = "engine", "session_maker", "drop_all"

    url: str
    logger: Logger

    def __init__(self, db_url: str = "", drop_all: bool = False) -> None:
        if db_url:
            self.url = db_url
        self.engine = engine = get_async_engine(self.url)
        self.session_maker = get_async_session_maker(engine)
        self.drop_all = drop_all

    async def start(self) -> None:
        """Функция выполняет действия, необходимые при подключении к БД."""
        self.logger.info("Подключение к базе данных.")
        return await start_conn(self.engine, self.drop_all)

    async def stop(self) -> None:
        """Функция выполняет действия, необходимые при отключении от БД."""
        self.logger.info("Отключение от базы данных.")
        return await stop_conn(self.engine)
