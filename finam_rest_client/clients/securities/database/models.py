"""Модели базы данных."""

from typing import Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для создания моделей таблиц."""

    def to_dict(self) -> dict[str, Any]:
        """Преобразование данных возвращенной модели в словарь."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore

    def __repr__(self) -> str:
        """Формирование отладочной информации."""
        res = ", ".join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"{type(self).__name__}({res})"


class Security(Base):
    """Информация об инструменте."""

    __tablename__ = "securities"

    code = Column(String, nullable=False, primary_key=True)
    board = Column(String, nullable=False, primary_key=True)
    market = Column(String, nullable=False)
    decimals = Column(Integer, nullable=False)
    lotSize = Column(Integer, nullable=False)
    minStep = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    shortName = Column(String, nullable=False)
    properties = Column(Integer, nullable=False)
    timeZoneName = Column(String, nullable=False)
    bpCost = Column(String, nullable=False)
    accruedInterest = Column(String, nullable=False)
    priceSign = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    lotDivider = Column(Integer, nullable=False)
