"""Менеджер для взаимодействия с БД."""

import logging
from pathlib import Path
from typing import Literal

from sqlalchemy import delete, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError

from finam_rest_client.clients.securities.database.models import Security
from finam_rest_client.models.response_models import Securities

from .base import AbstractDBManager

db_path = Path(__file__).parent.joinpath("securities.db")


class DBManager(AbstractDBManager):
    """
    Класс для взаимодействия с базой данных SQLite.

    В базе хранится информация по инструментам.
    Так как Finam отклоняет частые запросы,
    можно выгрузить результат в БД и запрашивать из нее.
    """

    url = f"sqlite+aiosqlite:///{db_path}"
    logger = logging.getLogger("finam_rest_client.Securities.DBManager")

    async def add_securities(self, securities: Securities) -> bool:
        """
        Добавление информации об инструменте/ах в БД.

        :param securities: Модель информации об инструментах.

        :return: True, если запрос успешен, иначе False.
        """
        self.logger.debug("Добавление данных в базу.")
        _securities = securities.model_dump(mode="json", by_alias=True)
        query = insert(Security)
        async with self.session_maker() as session:
            try:
                await session.execute(query, _securities["data"]["securities"])
                await session.commit()
                self.logger.debug("Данные добавлены.")
                return True
            except IntegrityError as exc:
                await session.rollback()
                self.logger.warning(
                    "Данные не добавлены. Произошла ошибка: %s.", exc
                )
            return False

    async def get_securities(
        self, seccode: str | None = None, board: str | None = None
    ) -> Securities | None:
        """
        Получение информации об инструментах из БД.

        :param seccode: Режим торгов (необязательное поле для фильтрации)
        :param board: Тикер инструмента (необязательное поле для фильтрации)

        :return: Модель информации об инструментах или None,
        если информации нет в базе.
        """
        self.logger.debug(
            "Поиск данных в БД. seccode=%s, board=%s", seccode, board
        )
        query = await self._generate_query("select", seccode, board)
        async with self.session_maker() as session:
            self.logger.debug("Создана сессия БД: %s.", session)
            result = await session.execute(query)
            res = result.scalars().all()
            if not res:
                self.logger.debug("Данные не найдены в базе.")
                return None
            data = {"data": {"securities": res}}
            self.logger.debug("Данные найдены в базе.")
            return Securities.model_validate(data, from_attributes=True)

    async def remove_securities(
        self, seccode: str | None = None, board: str | None = None
    ) -> int:
        """
        Удаление информации об инструментах из БД.

        :param seccode: Режим торгов (необязательное поле для фильтрации)
        :param board: Тикер инструмента (необязательное поле для фильтрации)

        :return: Количество удаленных значений.
        """
        self.logger.warning(
            "Удаление данных из БД. seccode=%s, board=%s", seccode, board
        )
        query = await self._generate_query("delete", seccode, board)
        async with self.session_maker() as session:
            result = await session.execute(query)
            res = result.rowcount
            await session.commit()
            self.logger.warning("Количество удаленных значений: %s.", res)
            return res  # type: ignore

    @staticmethod
    async def _generate_query(
        query_type: Literal["select", "delete"],
        seccode: str | None = None,
        board: str | None = None,
    ):
        types = {"select": select, "delete": delete}
        query = types[query_type](Security)  # type: ignore
        if seccode and board:
            query = query.where(
                Security.code == seccode, Security.board == board
            )
        elif seccode:
            query = query.where(Security.code == seccode)
        elif board:
            query = query.where(Security.board == board)
        return query
