from datetime import date, datetime
from typing import Self

from pydantic import Field, model_validator

from .base import BaseCandleRequest
from .timeframes import DayTimeFrames, IntraDayTimeFrames


class DayCandlesRequest(BaseCandleRequest):
    """
    Запрос свечей с интервалом от 1 дня.

    Параметры:

        - security_code - код инструмента;
        - security_board - код площадки;
        - time_frame - тайм-фрейм;
        - from_ - начало интервала;
        - to - конец интервала;
        - count - количество свечей.

    Необходимо указать security_code, security_board и time_frame.
    Запросить можно как определенное количество свечей, так и за интервал.
    Для запроса количества свечей в запросе необходимо указать count и
    либо from_ (начиная с указанной даты), либо to (до указанной даты).
    Для запроса за интервал необходимо указать from_ и to.

    Для дневных свечей в from_ и to указывается дата в формате
    yyyy-MM-dd в часовом поясе UTC.

    Ограничения на запрос:
     - Максимальное значение count 500 штук;
     - Для дневных свечей максимальный интервал 365 дней;
    """

    time_frame: DayTimeFrames = Field(serialization_alias="timeFrame")
    from_: date | None = Field(
        serialization_alias="Interval.From", default=None
    )
    to: date | None = Field(serialization_alias="Interval.To", default=None)

    @model_validator(mode="after")
    def __validate_interval(self) -> Self:
        if not self.from_ or not self.to:
            return self
        result = (self.to - self.from_).days
        if result > 365:
            raise ValueError(
                "The interval between from_ and to cannot exceed 365 days."
            )
        return self


class IntraDayCandlesRequest(BaseCandleRequest):
    """
    Запрос свечей с внутридневным интервалом.

    Параметры:

        - security_code - код инструмента;
        - security_board - код площадки;
        - time_frame - тайм-фрейм;
        - from_ - начало интервала;
        - to - конец интервала;
        - count - количество свечей.

    Необходимо указать security_code, security_board и time_frame.
    Запросить можно как определенное количество свечей, так и за интервал.
    Для запроса количества свечей в запросе необходимо указать count и
    либо from_ (начиная с указанной даты), либо to (до указанной даты).
    Для запроса за интервал необходимо указать from_ и to.

    Для внутридневных свечей from и to указываются в формате
    yyyy-MM-ddTHH:mm:ssZ в часовом поясе UTC.

    Ограничения на запрос:
     - Максимальное значение count 500 штук;
     - Для внутридневных свечей максимальный интервал 30 дней.
    """

    time_frame: IntraDayTimeFrames = Field(serialization_alias="timeFrame")
    from_: datetime | None = Field(
        serialization_alias="Interval.From", default=None
    )
    to: datetime | None = Field(
        serialization_alias="Interval.To", default=None
    )

    @model_validator(mode="after")
    def __validate_interval(self) -> Self:
        if not self.from_ or not self.to:
            return self
        result = (self.to - self.from_).days
        if result > 30:
            raise ValueError(
                "The interval between from_ and to cannot exceed 30 days."
            )
        return self
