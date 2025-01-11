"""Базовая модель для отправки запросов на получение свечей."""

from pydantic import BaseModel, Field


class BaseCandleRequest(BaseModel):
    """Базовая модель для отправки запросов на получение свечей."""

    security_board: str = Field(serialization_alias="securityBoard")
    security_code: str = Field(serialization_alias="securityCode")
    count: int | None = Field(
        serialization_alias="Interval.Count", default=None, le=500, ge=1
    )
