"""Функции для подключения к БД."""

import logging

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base

logger = logging.getLogger("finam_rest_client.Securities.database")


def get_async_engine(database_url: str) -> AsyncEngine:
    """
    Функция для получения асинхронного движка.

    :param database_url: Ссылка на БД.

    :return: Асинхронный движок.
    """
    logger.debug(f"Функция запущена с параметрами: {database_url=}.")
    engine = create_async_engine(database_url)
    logger.debug(f"Функция вернула: {engine}")
    return engine


def get_async_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Функция для получения конструктора асинхронной сессии.

    :param engine: Асинхронный движок.

    :return: Объект конструктора асинхронной сессии.
    """
    logger.debug(f"Функция запущена с параметрами: {engine=}.")
    result = async_sessionmaker(engine, expire_on_commit=False)
    logger.debug(f"Функция вернула: {result}")
    return result


async def start_conn(engine: AsyncEngine, drop_all: bool = False) -> None:
    """
    Функция выполняет действия, необходимые при подключении к БД.

    :param engine: Асинхронный движок.
    :param drop_all: Опциональный параметр.
    Указывает нужно ли удалять таблицы.
    """
    logger.debug(f"Функция запущена с параметрами: {engine=}, {drop_all=}")
    async with engine.begin() as conn:
        if drop_all:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def stop_conn(engine: AsyncEngine, drop_all: bool = False) -> None:
    """
    Функция выполняет действия, необходимые при отключении от БД.

    :param engine: Асинхронный движок.
    :param drop_all: Опциональный параметр.
    Указывает нужно ли удалять таблицы.
    """
    logger.debug(f"Функция запущена с параметрами: {engine=}, {drop_all=}")
    if drop_all:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
